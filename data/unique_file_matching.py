###
# jq -s '
#  [.[].matches_info[][0]] as $all
#  | {total: ($all | length), unique: ($all | unique | length)}
# ' matching_repos1.ndjson
# {
#   "total": 25138058,
#   "unique": 2337451
# }

# jq -s '
#   [.[].matches_info[][0]]
#   | group_by(.)
#   | map({id: .[0], count: length})
#   | sort_by(-.count)
# ' matching_repos1.ndjson > id_counts.json
# Information stored in id_counts.json

# Most frequent file: https://archive.softwareheritage.org/browse/content/sha1_git:6e9769c29c31b631a53b55eea0fca8065caa29a2/


import json
import matplotlib.pyplot as plt

# Load the JSON data
with open("counts.json", "r") as f:
    data = json.load(f)

# Filter out counts <= 1
filtered = [item for item in data if item["count"] > 100]

# Sort by count descending
filtered.sort(key=lambda x: x["count"], reverse=True)

# Extract counts only
counts = [item["count"] for item in filtered]

# Take only top N
top_n = 25
counts_top = counts[:top_n]

# Helper to format numbers
def human_format(num):
    if num >= 1000000:
        return f'{num//1000000}M'
    elif num >= 1_000:
        
        return f'{num//1000}K'
    else:
        return str(num)

# Plot
plt.figure(figsize=(12, 6))
bars = plt.bar(range(len(counts_top)), counts_top, color="pink")

# Add formatted counts on top of bars
for bar, val in zip(bars, counts_top):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height, human_format(val),
             ha='center', va='bottom', fontsize=8)

plt.ylabel("Occurrences")
plt.xlabel("Files (index)")
plt.title(f"Top 25")
# plt.tight_layout()
plt.show()
