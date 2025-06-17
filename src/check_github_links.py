import json
import requests

with open("../data/github_art_repos_urls.json") as json_file:
    json_data = json.load(json_file)

def is_alive(url):
    try:
        response = requests.head(url, timeout=10)
        return response.status_code == 200
    except requests.RequestException:
        return False

def update_json_files(alive_links, dead_links):
    with open('alive_links.json', 'w') as f:
        json.dump(alive_links, f, indent=2)
    
    with open('dead_links.json', 'w') as f:
        json.dump(dead_links, f, indent=2)

alive_links = []
dead_links = []

count = 0
total_links = len(json_data)

for url in json_data:
    if is_alive(url):
        alive_links.append(url)
        print(f"Link {count + 1}/{total_links}: is alive")
    else:
        dead_links.append(url)
        print(f"Link {count + 1}/{total_links}: is dead")
    
    count += 1
    
    # Update JSON files after each check
    update_json_files(alive_links, dead_links)
    
    # Optional: print progress summary every 10 iterations
    if count % 10 == 0:
        print(f"Progress: {count}/{total_links} - Alive: {len(alive_links)}, Dead: {len(dead_links)}")

print(f"\nFinal Results:")
print(f"Total links checked: {total_links}")
print(f"Alive links: {len(alive_links)}")
print(f"Dead links: {len(dead_links)}")

print("\nAlive Links:")
print(alive_links)
print("\nDead Links:")
print(dead_links)