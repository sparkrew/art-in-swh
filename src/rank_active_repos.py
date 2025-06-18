"""
rank_active_repos.py

Ranking active repos based on interesting topics.

The repos's "score" created just reflect the percentage of the topics
we consider to be interesting (i.e., is in our list of topics).

Seems like a simple, yet fairly effective way prioritize the github repos.

Don't hesitate to suggest any improvement :)
"""

import json
import ast
import pandas as pd

topics_file = "data/github_art_topics_list.json"
raw_file = "data/github_art_repos_by_topic_parsed.txt"
active_repos_file = "data/alive_links.json"
output_file = "data/ranked_active_urls.csv"
TOPICS = [
    "art",
    "erc721",
    "artnet",
    "p5",
    "p5js",
    "openframeworks",
    "puredata",
    "processing",
    "livecoding",
    "osc",
    "dmx",
    "artnet",
    "generative-art",
    "digital-art",
    "nft",
    "nfts",
    "touchdesigner",
    "touchdesigner-components",
    "nodebox",
    "sound-art",
    "music-generation",
    "generative-music",
    "star",
    "midi",
    "creative-coding",
    "genuary",
    "ascii",
    "ascii-art",
    "braille-art",
    "vvvv",
    "algorave",
    "maxmsp",
    "faust",
    # new ones:
    "creative-coding",
    "hydra",
    "watercolor",
    # interesting file extensions:
    "pde",
    "scd",
    "pde",
    "ndbx",
    "toe",
    "tox",
    "v4p",
    "clj",
]

def select_urls_and_topics(input_file): # txt
    urls = {}
    
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
                urls = urls | {
                    url: {
                    "topics": topics,
                    "n_topics": len(topics)
                    }
                }
            except ValueError as e:
                print(f"Skipping line due to parsing error: {line}\nError: {e}")
    return urls

def quantify_interest(active_urls, selectec_topics):
    processed_urls = {}
    for key, value in active_urls.items():
        top_cnt = 0
        for topic in value["topics"]:
            if topic in selectec_topics:
                top_cnt += 1
        processed_urls = processed_urls | {
            key: value | {
                    "score": top_cnt / value["n_topics"],
                }
        }
    return processed_urls


def get_interesting_topics(topics_file):
    with open(topics_file, "r") as tf:
        topics = json.loads(tf.read())
        topics.sort()
    selectec_topics = []
    for word in TOPICS:
        selectec_topics += [topic for topic in topics if word == topic]
    return selectec_topics


if __name__ == "__main__":
    # Open all urls 
    all_urls_dict = select_urls_and_topics(raw_file)
    
    # Open active list of github repos
    with open(active_repos_file) as a_l:
        active_urls = json.loads(a_l.read())

    # Select only active github repos 
    active_urls_dict = {key: value for key,value in all_urls_dict.items() if key in active_urls}
    
    # Filter all topics to select the ones we find interesting
    selectec_topics = get_interesting_topics(topics_file)
    
    # Use selected topics to create rank
    processed_urls = quantify_interest(active_urls_dict, selectec_topics)

    # Dataframe to sort and save
    data = pd.DataFrame.from_dict(processed_urls).T.reset_index(names="url")
    data = data.sort_values(by="score", ascending=False).reset_index(drop=True)
    data.to_csv(output_file, index=False)