import os
import json
import time
import re
import fnmatch
import requests
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from collections import deque
import base64
import argparse
import logging
import urllib.parse

class Config:
    def __init__(self, p5_libraries_file: str = None, fetch_commits: bool = False):
        self.tokens = self._load_tokens()
        self.p5_libraries = self._load_p5_libraries(p5_libraries_file)
        self.fetch_commit_info = fetch_commits
        # These thresholds could be properly set. For now, just some reasonable numbers.
        self.max_retries = 3
        self.rate_limit_threshold = 10
        self.backoff_base = 2
        self.download_dir = 'downloads'
        self.checkpoint_file = 'checkpoint.json'
        self.found_output = 'found_artworks.json'
        self.not_found_output = 'not_found_artworks.json'
        self.error_log = 'errors.log'
    
    def _load_tokens(self) -> List[str]:
        tokens = []
        env_tokens = os.getenv('GITHUB_TOKENS', '')
        if env_tokens:  
            tokens.extend([t.strip() for t in env_tokens.split(',') if t.strip()])
        # tokens.append('token')
        if not tokens:
            print("No GitHub tokens found.  Set GITHUB_TOKENS environment variable.")
            print("Example: export GITHUB_TOKENS='token1,token2,token3'")
        return tokens
    
    def _load_p5_libraries(self, filepath: str) -> List[str]:
        libraries = []
        if not os.path.exists(filepath):
            print(f"p5 libraries file not found: {filepath}")
            print("Using default library patterns")
            return [
                'p5*.js',
                '*.min.js',
            ]
        try:  
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        libraries.append(line)
            return libraries
        except Exception as e: 
            print(f"Error loading p5 libraries file: {e}")
            return []


class TokenManager:
    def __init__(self, tokens: List[str]):
        self.tokens = deque(tokens)
        self.rate_limits = {}
        self.current_token = None
        if tokens:
            self.current_token = self.tokens[0]
    
    def get_headers(self) -> Dict[str, str]: 
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'artwork-downloader'
        }
        if self.current_token:
            headers['Authorization'] = f'token {self.current_token}'
        return headers
    
    def check_rate_limit(self, response:  requests.Response) -> bool:
        remaining = int(response.headers.get('X-RateLimit-Remaining', 1000))
        reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
        if self.current_token:
            self.rate_limits[self.current_token] = {
                'remaining': remaining,
                'reset':  reset_time
            }
        return remaining > 0
    
    def rotate_token(self) -> bool:
        if len(self.tokens) <= 1:
            return False
        self.tokens.rotate(-1)
        self.current_token = self.tokens[0]
        if self.current_token in self.rate_limits:
            remaining = self.rate_limits[self.current_token]['remaining']
            if remaining > 0:
                return True
        else:
            return True 
        for _ in range(len(self.tokens) - 1):
            self.tokens.rotate(-1)
            self.current_token = self.tokens[0]
            if self.current_token not in self.rate_limits:
                return True
            if self.rate_limits[self.current_token]['remaining'] > 0:
                return True
        return False
    
    def wait_for_reset(self):
        if not self. rate_limits:
            time.sleep(60)
            return
        earliest_reset = min(
            limit['reset'] for limit in self. rate_limits.values()
        )
        wait_time = max(0, earliest_reset - time.time() + 5)
        print(f"All tokens rate-limited. Waiting {wait_time:. 0f}s...")
        time.sleep(wait_time)
        self.rate_limits.clear()


class GitHubScraper:
    def __init__(self, config: Config):
        self.config = config
        self.token_manager = TokenManager(config. tokens)
        self.session = requests.Session()
        self.found_artworks = []
        self.not_found_artworks = []
        self.processed_repos = set()
        self.stats = {
            'library_files_disregarded': {},
        }
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(config.error_log),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def parse_repo_url(self, url:  str) -> Optional[Tuple[str, str]]:  
        # Handle format: https://github.com/username/repo
        match = re. match(r'https?://github\.com/([^/]+)/([^/]+)/?', url.strip())
        if match:
            owner = match.group(1)
            repo = match.group(2)
            repo = repo.rstrip('.git')
            return owner, repo
        if '/' in url and not url.startswith('http'):
            parts = url.strip().split('/')
            if len(parts) == 2:
                return parts[0], parts[1]
        return None
    
    def make_request(self, url: str, retry_count: int = 0) -> Optional[requests.Response]:  
        try:
            headers = self.token_manager.get_headers()
            self.logger.debug(f"Request URL: {url}")
            self.logger.debug(f"Request headers: {headers}")
            response = self.session.get(url, headers=headers, timeout=30)
            self.logger.debug(f"Response status: {response.status_code}")
            self.token_manager.check_rate_limit(response)
            
            if response.status_code == 403:
                if 'rate limit' in response.text.lower():
                    if self.token_manager.rotate_token():
                        self.logger. info("Rate limit reached, rotating token...")
                        return self.make_request(url, retry_count)
                    else:  
                        self.logger. warning("All tokens rate-limited")
                        self.token_manager.wait_for_reset()
                        return self.make_request(url, retry_count)
                else:
                    self.logger.error(f"403 Forbidden (not rate limit): {response.text[:200]}")
                    return None
            if response. status_code == 404:
                self.logger.warning(f"Not found: {url}")
                return None
            if response. status_code == 415:
                self.logger.error(f"415 Unsupported Media Type:  {url}")
                self.logger.error(f"Response: {response.text[:200]}")
                return None
            response.raise_for_status()
            return response
            
        except requests.exceptions.HTTPError as e:
            self. logger.error(f"HTTP Error {response.status_code}: {url}")
            self.logger.error(f"Response: {response.text[:500]}")
            
            if retry_count < self. config.max_retries:
                wait_time = self.config.backoff_base ** retry_count
                self.logger.warning(f"Retrying in {wait_time}s...")
                time.sleep(wait_time)
                return self.make_request(url, retry_count + 1)
            else:
                self.logger.error(f"Request failed after {self.config.max_retries} retries:  {e}")
                return None
                
        except requests.exceptions.RequestException as e:
            if retry_count < self.config. max_retries:
                wait_time = self.config.backoff_base ** retry_count
                self.logger.warning(f"Request failed, retrying in {wait_time}s:  {e}")
                time.sleep(wait_time)
                return self.make_request(url, retry_count + 1)
            else:
                self.logger.error(f"Request failed after {self.config.max_retries} retries: {e}")
                return None
    
    def get_repo_tree(self, owner: str, repo: str) -> Optional[List[Dict]]:
        repo_url = f"https://api.github.com/repos/{owner}/{repo}"
        response = self.make_request(repo_url)
        if not response:
            return None
        try:
            repo_data = response.json()
        except json.JSONDecodeError as e:
            self.logger. error(f"Failed to parse repo JSON: {e}")
            return None
        default_branch = repo_data.get('default_branch', 'main')
        tree_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{default_branch}?recursive=1"
        response = self. make_request(tree_url)
        if not response: 
            return None
        try:
            tree_data = response.json()
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse tree JSON:  {e}")
            return None
        
        return tree_data.get('tree', [])
    
    def get_file_content(self, url: str) -> Optional[str]:
        response = self.make_request(url)
        if not response:
            return None
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse file content JSON: {e}")
            return None
        if 'content' in data:  
            try:
                content = base64.b64decode(data['content']).decode('utf-8', errors='ignore')
                return content
            except Exception as e:  
                self.logger.error(f"Failed to decode content: {e}")
                return None
        
        return None
    
    def matches_library(self, filename: str) -> Optional[str]:
        for pattern in self.config.p5_libraries:
            if fnmatch.fnmatch(filename, pattern):
                return pattern
        return None
    
    def has_setup_function(self, content: str) -> bool:
        if not content:  
            return False
        # Look for various patterns of setup function. Apparently, there are other ways to define it rather than just setup().
        # Removed the last three patterns becuase they could match variable assignments that are not functions. But later we can reconsider them.
        patterns = [
            r'\bfunction\s+setup\s*\(',  # function setup()
            r'\bsetup\s*:\s*function\s*\(',  # setup:  function()
            r'\bsetup\s*=\s*function\s*\(',  # setup = function()
            r'\bsetup\s*\([^)]*\)\s*{',  # setup() {
            # r'\bconst\s+setup\s*=',  # const setup =
            # r'\blet\s+setup\s*=',  # let setup =
            # r'\bvar\s+setup\s*=',  # var setup =
        ]
        for pattern in patterns:
            if re.search(pattern, content, re. IGNORECASE):
                return True
        return False
    
    def organize_files_by_directory(self, tree:  List[Dict]) -> Dict[str, List[Dict]]:  
        directories = {}
        for item in tree:
            if item['type'] != 'blob':
                continue
            path = item['path']
            dir_path = str(Path(path).parent)
            if dir_path not in directories:
                directories[dir_path] = []
            directories[dir_path].append(item)
        return directories
    
    def get_file_commits(self, owner:   str, repo: str, file_path: str) -> Optional[Dict]:
        encoded_path = urllib.parse.quote(file_path)
        commits_url = f"https://api.github.com/repos/{owner}/{repo}/commits?path={encoded_path}&per_page=20"
        response = self.make_request(commits_url)
        if not response:
            return None
        try:   
            commits_data = response. json()
            if not commits_data or len(commits_data) == 0:
                return None
            latest_commit = commits_data[0]
            commit_date = latest_commit. get('commit', {}).get('author', {}).get('date')
            link_header = response.headers.get('Link', '')
            total_commits = len(commits_data)
            
            if 'rel="last"' in link_header:  
                last_page_match = re.search(r'page=(\d+)>; rel="last"', link_header)
                if last_page_match:   
                    last_page_num = int(last_page_match. group(1))
                    # Total = (last_page - 1) * per_page + commits on last page
                    # But we don't know commits on last page without fetching it
                    # We don't want to make another request just for that, so we approximate
                    # Approximation: last_page * per_page (will be slightly high)
                    total_commits = f"{(last_page_num - 1) * 20}+"
            return {
                'count': total_commits,
                'last_commit_date': commit_date
            }
        except (json.JSONDecodeError, KeyError) as e:
            self.logger.error(f"Failed to parse commit data: {e}")
            return None
    
    def process_directory(self, owner: str, repo: str, dir_path: str, files: List[Dict]) -> Optional[Dict]:
        html_files = [f for f in files if f['path'].endswith('.html')]
        js_files = [f for f in files if f['path'].endswith('.js')]
        # We consider two cases where a file is an artwork. 
        # Exactly one HTML file, no JS files
        if len(html_files) == 1 and len(js_files) == 0:
            html_file = html_files[0]
            content = self.get_file_content(html_file['url'])
            if content and self.has_setup_function(content):
                return self.create_found_entry(owner, repo, html_file, files, [])
        # One HTML file + multiple JS files
        elif len(html_files) == 1 and len(js_files) > 0:
            library_files = []
            non_library_files = []
            for js_file in js_files:  
                filename = Path(js_file['path']).name
                matched_pattern = self.matches_library(filename)
                if matched_pattern:
                    library_files.append(js_file)
                    if matched_pattern not in self.stats['library_files_disregarded']:
                        self.stats['library_files_disregarded'][matched_pattern] = 0
                    self.stats['library_files_disregarded'][matched_pattern] += 1
                else:  
                    non_library_files.append(js_file)
            # All except one are libraries
            if len(non_library_files) == 1:
                artwork_file = non_library_files[0]
                content = self.get_file_content(artwork_file['url'])
                if content and self.has_setup_function(content):
                    library_names = [Path(f['path']).name for f in library_files]
                    return self.create_found_entry(owner, repo, artwork_file, files, library_names)
            # Record as not found but with library info
            library_names = [Path(f['path']).name for f in library_files]
            if library_names:
                return self. create_not_found_entry(owner, repo, dir_path, files, library_names)
        
        return None
    
    def create_found_entry(self, owner: str, repo: str, artwork_file: Dict, 
                      all_files: List[Dict], libraries: List[str]) -> Dict:
        file_path = artwork_file['path']
        file_url = f"https://github.com/{owner}/{repo}/blob/main/{file_path}"
        local_path = Path(self.config.download_dir) / owner / repo / file_path
        local_path.parent.mkdir(parents=True, exist_ok=True)
        content = self.get_file_content(artwork_file['url'])
        if content:
            with open(local_path, 'w', encoding='utf-8') as f:
                f.write(content)
        dir_path = str(Path(file_path).parent)
        other_files = []
        for f in all_files: 
            if str(Path(f['path']).parent) == dir_path and f['path'] != file_path:
                filename = Path(f['path']).name
                if not self.matches_library(filename):
                    other_files.append(filename)
        commits_count = None
        last_commit_date = None
        if self.config.fetch_commit_info:
            commit_info = self.get_file_commits(owner, repo, file_path)
            if commit_info:
                commits_count = commit_info['count']
                last_commit_date = commit_info['last_commit_date']
                self.logger.debug(f"Commit info for {file_path}: {commits_count} commits, last:  {last_commit_date}")
        entry = {
            'filename': f"{owner}/{repo}/{file_path}",
            'url': file_url,
            'commits': commits_count,
            'date': last_commit_date if last_commit_date else None,
            'libraries': libraries,
            'other': other_files
        }
        self.logger.info(f"Found artwork: {entry['filename']}")
        return entry
    
    # Here, we also track the cases where there are library files but no artwork found, or more than one js files are not libraries.
    # This is to keep a record of what we missed, and later maybe we can adjust it or just report them.
    def create_not_found_entry(self, owner: str, repo: str, dir_path: str,
                               all_files: List[Dict], libraries: List[str]) -> Dict:
        folder_url = f"https://github.com/{owner}/{repo}/tree/main/{dir_path}"
        other_files = []
        for f in all_files:
            if str(Path(f['path']).parent) == dir_path:
                filename = Path(f['path']).name
                if not self.matches_library(filename):
                    other_files.append(filename)
        entry = {
            'url': folder_url,
            'libraries': libraries,
            'other': other_files
        }
        return entry
    
    def process_repo(self, repo_url: str):
        parsed = self.parse_repo_url(repo_url)
        if not parsed:
            self.logger.error(f"Invalid repo URL format: {repo_url}")
            return
        owner, repo = parsed
        self.logger.info(f"Processing {owner}/{repo}...")
        tree = self.get_repo_tree(owner, repo)
        # Using the tree should limit the token usage.
        if not tree:  
            self.logger.warning(f"Could not get tree for {owner}/{repo}")
            return
        directories = self.organize_files_by_directory(tree)
        for dir_path, files in directories.items():
            result = self.process_directory(owner, repo, dir_path, files)
            if result:
                if result. get('filename'):  
                    self.found_artworks.append(result)
                    self.logger.debug(f"Added to found_artworks: {result['filename']}")
                else:
                    self.not_found_artworks.append(result)
                    self.logger.debug(f"Added to not_found_artworks: {result. get('url')}")
        self.logger.info(f"Total found: {len(self.found_artworks)}, Total not-found: {len(self.not_found_artworks)}")
        self.processed_repos.add(repo_url)
        
    def save_results(self):
        with open(self.config. found_output, 'w', encoding='utf-8') as f:
            json.dump(self.found_artworks, f, indent=2)
        with open(self.config. not_found_output, 'w', encoding='utf-8') as f:
            json.dump(self.not_found_artworks, f, indent=2)
        self.logger.info(f"Saved {len(self.found_artworks)} found artworks to {self.config.found_output}")
        self.logger.info(f"Saved {len(self.not_found_artworks)} not-found entries to {self.config.not_found_output}")

    def save_checkpoint(self):
        checkpoint = {
            'processed_repos': list(self.processed_repos),
            'found_count': len(self.found_artworks),
            'not_found_count': len(self.not_found_artworks),
            'found_artworks': self.found_artworks,
            'not_found_artworks': self.not_found_artworks
        }
        with open(self.config.checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(checkpoint, f, indent=2)

    def load_checkpoint(self) -> set:
        if os.path.exists(self. config.checkpoint_file):
            try:
                with open(self. config.checkpoint_file, 'r', encoding='utf-8') as f:
                    checkpoint = json.load(f)
                    self.found_artworks = checkpoint.get('found_artworks', [])
                    self. not_found_artworks = checkpoint.get('not_found_artworks', [])
                    self.logger.info(f"Restored {len(self.found_artworks)} found artworks")
                    self.logger.info(f"Restored {len(self.not_found_artworks)} not-found entries")
                    return set(checkpoint.get('processed_repos', []))
            except Exception as e:
                self.logger.error(f"Failed to load checkpoint: {e}")
                return set()
        return set()
    
    def run(self, repo_list_file: str, resume: bool = False):
        if not os.path.exists(repo_list_file):
            self.logger.error(f"Repository list file not found: {repo_list_file}")
            return
        with open(repo_list_file, 'r', encoding='utf-8') as f:
            repos = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        self.logger. info(f"Loaded {len(repos)} repositories")
        if resume:
            # Checkpoints could be useful if we run this on the server for a long time. Just loading the checkpoints from the file should work. 
            # But this is not tested.
            self.processed_repos = self.load_checkpoint()
            self.logger.info(f"Resuming from checkpoint ({len(self.processed_repos)} already processed)")
        for i, repo in enumerate(repos, 1):
            if repo in self.processed_repos:
                continue
            self.logger. info(f"[{i}/{len(repos)}] Processing {repo}")
            self.process_repo(repo)
            if i % 10 == 0:
                self.save_checkpoint()
                self.save_results()
        self.save_results()
        self.save_checkpoint()
        
        print("\n" + "="*60)
        print(f"Total repositories processed: {len(self.processed_repos)}")
        print(f"Artworks found: {len(self. found_artworks)}")
        print(f"Folders with libraries (no artwork): {len(self.not_found_artworks)}")
        print("\nLibrary files disregarded:")
        for lib, count in sorted(self.stats['library_files_disregarded'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {lib}: {count}")


def main():
    parser = argparse.ArgumentParser(description='Scrape p5.js artworks from GitHub repositories')
    # The links should be changed if we run this on the server. Or pass them as arguments.
    parser.add_argument('--repos', '-r',
                       default='repos.txt',
                       help='Path to repository list file')
    parser.add_argument('--libraries', '-l',
                       default='p5libraries.txt',
                       help='Path to p5.js libraries list file')
    parser.add_argument('--resume', action='store_true',
                       help='Resume from checkpoint')
    parser.add_argument('--tokens', '-t',
                       help='Comma-separated list of GitHub tokens (or use GITHUB_TOKENS env var)')
    parser.add_argument('--debug', '-d', action='store_true',
                       help='Enable debug logging')
    parser.add_argument('--fetch-commits', '-c', action='store_true',
                       help='Fetch commit information for found artworks (uses more API tokens)')
    
    args = parser.parse_args()
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    if args.tokens:  
        os.environ['GITHUB_TOKENS'] = args.tokens
    config = Config(p5_libraries_file=args.libraries, fetch_commits=args.fetch_commits)
    scraper = GitHubScraper(config)
    scraper.run(args.repos, resume=args.resume)


if __name__ == '__main__':
    main()
