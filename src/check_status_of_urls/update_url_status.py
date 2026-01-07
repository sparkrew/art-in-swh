import json
import requests
import time
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import sys

# Configuration
INPUT_FILE = "all_data_sources_array.json"
OUTPUT_FILE = "output_results.jsonl"  # JSONL for appending
CHECKPOINT_FILE = "checkpoint.json"
LOG_FILE = "live_check.log"

GITHUB_TOKENS = [
    "tokens_go_here"
]
REQUEST_TIMEOUT = 10  # seconds
RETRY_ATTEMPTS = 3
RATE_LIMIT_DELAY = 0.72

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class LiveStatusChecker:
    def __init__(self):
        self.github_tokens = GITHUB_TOKENS
        self.current_token_index = 0
        self.github_headers = {
            "Authorization": f"token {self. github_tokens[self.current_token_index]}",
            "Accept":   "application/vnd.github. v3+json"
        }
        self.session = requests.Session()
        self.stats = {
            "total_checked": 0,
            "live":   0,
            "dead":  0,
            "errors":  0
        }

    def is_github_url(self, url: str) -> bool:
        """Check if URL is a GitHub repository."""
        return "github.com" in url. lower()

    def rotate_token(self):
        """Rotate to the next available token."""
        self.current_token_index = (self.current_token_index + 1) % len(self.github_tokens)
        self.github_headers["Authorization"] = f"token {self.github_tokens[self. current_token_index]}"
        logger.info(f"Rotated to token {self.current_token_index + 1}/{len(self.github_tokens)}")

    def check_github_repo(self, url: str) -> Optional[bool]:
        """
        Check if GitHub repository is accessible.
        Returns:  True (live), False (dead), None (error/unknown)
        """
        try:
            # Extract owner/repo from URL
            # Handle formats:   https://github.com/owner/repo or github.com/owner/repo
            parts = url.rstrip('/').split('github.com/')
            if len(parts) < 2:
                logger.warning(f"Invalid GitHub URL format: {url}")
                return None

            repo_path = parts[1]. split('/')[0:2]
            if len(repo_path) < 2:
                logger.warning(f"Cannot extract owner/repo from: {url}")
                return None

            owner, repo = repo_path[0], repo_path[1]
            api_url = f"https://api.github.com/repos/{owner}/{repo}"

            for attempt in range(RETRY_ATTEMPTS):
                response = self.session.get(
                    api_url,
                    headers=self.github_headers,
                    timeout=REQUEST_TIMEOUT
                )

                if response.status_code == 200:
                    return True  # Repository is accessible
                elif response.status_code == 404:
                    return False  # Repository not found/deleted
                elif response.status_code == 403:
                    # Rate limited or forbidden
                    if 'X-RateLimit-Remaining' in response.headers:
                        remaining = int(response.headers['X-RateLimit-Remaining'])
                        if remaining == 0:
                            # Rotate token
                            if len(self.github_tokens) > 1:
                                logger.warning(f"Token {self.current_token_index + 1} rate limited.  Rotating token...")
                                self.rotate_token()
                                continue  # Retry with new token
                            else:
                                # Only one token, must sleep
                                reset_time = int(response.headers['X-RateLimit-Reset'])
                                sleep_time = reset_time - time.time() + 10
                                logger.warning(f"Rate limited. Sleeping for {sleep_time:. 0f} seconds")
                                time.sleep(max(sleep_time, 0))
                                continue
                    return False  # Private or access denied = treat as not accessible
                elif response.status_code == 451:
                    return False  # Repository blocked for legal reasons
                elif response.status_code >= 500:
                    # Server error, retry
                    logger.warning(f"Server error {response.status_code} for {url}, attempt {attempt+1}")
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    logger.warning(f"Unexpected status {response.status_code} for {url}")
                    return None

            return None  # Failed after retries

        except requests. exceptions. Timeout:
            logger.error(f"Timeout checking {url}")
            return None
        except requests.exceptions.RequestException as e:
            logger. error(f"Request error for {url}: {e}")
            return None

    def check_generic_url(self, url: str) -> Optional[bool]:
        """
        Check if non-GitHub URL is accessible via HEAD request.
        Returns: True (live), False (dead), None (error/unknown)
        """
        try:
            for attempt in range(RETRY_ATTEMPTS):
                response = self. session.head(
                    url,
                    timeout=REQUEST_TIMEOUT,
                    allow_redirects=True
                )

                if response.status_code < 400:
                    return True  # Accessible
                elif response.status_code == 404 or response.status_code == 410:
                    return False  # Not found or gone
                elif response.status_code >= 500:
                    # Server error, retry with GET
                    response = self.session.get(
                        url,
                        timeout=REQUEST_TIMEOUT,
                        allow_redirects=True,
                        stream=True  # Don't download content
                    )
                    response.close()
                    if response.status_code < 400:
                        return True
                    elif response.status_code == 404 or response.status_code == 410:
                        return False
                    time.sleep(2 ** attempt)
                    continue
                else:
                    return False  # Other client errors = not accessible

            return None  # Failed after retries

        except requests.exceptions.Timeout:
            logger.error(f"Timeout checking {url}")
            return None
        except requests. exceptions.RequestException as e:
            logger.error(f"Request error for {url}: {e}")
            return None

    def check_url(self, url: str) -> Optional[bool]:
        """Main URL checking logic with rate limiting."""
        if self.is_github_url(url):
            result = self.check_github_repo(url)
            time.sleep(RATE_LIMIT_DELAY)  # Rate limit for GitHub API
        else:
            result = self. check_generic_url(url)
            time.sleep(0.5)  # Be polite to other servers

        return result

    def load_checkpoint(self) -> int:
        """Load last processed index from checkpoint."""
        if Path(CHECKPOINT_FILE).exists():
            try:
                with open(CHECKPOINT_FILE, 'r') as f:
                    checkpoint = json.load(f)
                    logger.info(f"Resuming from index {checkpoint['last_index']}")
                    return checkpoint['last_index']
            except Exception as e:
                logger.error(f"Error loading checkpoint: {e}")
        return 0

    def save_checkpoint(self, index: int):
        """Save current progress to checkpoint file."""
        checkpoint = {
            "last_index": index,
            "timestamp": datetime.now().isoformat(),
            "stats": self.stats
        }
        with open(CHECKPOINT_FILE, 'w') as f:
            json.dump(checkpoint, f, indent=2)

    def append_result(self, entry: Dict[str, Any]):
        """Append single result to output file."""
        with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
            f.write(json. dumps(entry, ensure_ascii=False) + '\n')

    def process(self):
        """Main processing loop."""
        logger. info("Starting live status check...")
        logger.info(f"Using {len(self.github_tokens)} GitHub token(s)")

        # Load input data
        logger.info(f"Loading data from {INPUT_FILE}...")
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

        total_entries = len(data)
        logger.info(f"Loaded {total_entries} entries")

        # Resume from checkpoint
        start_index = self. load_checkpoint()

        # Process each entry
        for index, entry in enumerate(data):
            if index < start_index:
                continue  # Skip already processed

            url = entry. get("origin")
            if not url:
                logger.warning(f"Entry {index} has no origin URL, skipping")
                entry. setdefault("metadata", {})["live"] = None
                self.append_result(entry)
                self.save_checkpoint(index + 1)
                continue

            # Check live status
            live_status = self. check_url(url)

            # Update only the live status
            if "metadata" not in entry:
                entry["metadata"] = {}
            entry["metadata"]["live"] = live_status

            # Update stats
            self.stats["total_checked"] += 1
            if live_status is True:
                self.stats["live"] += 1
            elif live_status is False:
                self.stats["dead"] += 1
            else:
                self.stats["errors"] += 1

            # Save result
            self.append_result(entry)

            # Save checkpoint
            self. save_checkpoint(index + 1)

            # Log progress
            if (index + 1) % 100 == 0:
                progress = ((index + 1) / total_entries) * 100
                logger.info(
                    f"Progress:  {index + 1}/{total_entries} ({progress:.2f}%) | "
                    f"Live:  {self.stats['live']} | Dead: {self.stats['dead']} | "
                    f"Errors: {self.stats['errors']}"
                )

        logger.info("Processing complete!")
        logger.info(f"Final stats: {self.stats}")


def main():
    checker = LiveStatusChecker()

    try:
        checker. process()
    except KeyboardInterrupt:
        logger.info("Process interrupted by user.  Progress saved in checkpoint.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()