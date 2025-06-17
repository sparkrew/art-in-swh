import json
import ast

def remove_duplicate_lines(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Remove duplicates
        seen = set()
        unique_lines = []
        
        for line in lines:
            line_lower = line.lower()
            if line_lower not in seen:
                seen.add(line_lower)
                unique_lines.append(line)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(unique_lines)
        
        print(f"Original file had {len(lines)} lines")
        print(f"After removing duplicates: {len(unique_lines)} lines")
        print(f"Removed {len(lines) - len(unique_lines)} duplicate lines")
        
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
    except Exception as e:
        print(f"Error: {e}")
        
        
def generate_jsons(input_file):
    urls = []
    unique_topics = set()

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Split URL and tag list
            try:
                url_part, tags_part = line.split('\t')
                url = url_part.strip().strip('"')
                topics = ast.literal_eval(tags_part.strip())  
                urls.append(url)
                unique_topics.update(topics)
            except ValueError as e:
                print(f"Skipping line due to parsing error: {line}\nError: {e}")
     
    return urls, unique_topics
        
if __name__ == "__main__":
    input_file = '../data/source_data/github_art_repos_by_topic.txt'
    parsed_urls_topics_github = '../data/github_art_repos_by_topic_parsed.txt'
    
    remove_duplicate_lines(input_file, parsed_urls_topics_github)
    print(f"Deduplicated content saved to: {parsed_urls_topics_github}")
    
    github_url_json = '../data/github_art_repos_urls.json'
    github_topics_json = '../data/github_art_topics_list.json'

    url_list, unique_topics_set = generate_jsons(parsed_urls_topics_github)

    with open(github_url_json, 'w', encoding='utf-8') as f:
        json.dump(url_list, f, indent=2)
        print(f"number of URLs extracted: {len(url_list)}")
        print(f"URLs saved to: {github_url_json}")
        

    with open(github_topics_json, 'w', encoding='utf-8') as f:
        json.dump(list(unique_topics_set), f, indent=2)
        print(f"number of unique topics extracted: {len(unique_topics_set)}")
        print(f"Unique topics saved to: {github_topics_json}")
