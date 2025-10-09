###
# Command to extract all signals: get extensions in matches_info[] and the repetition count
#
# jq -r '.matches_info[]? 
#        | select(type=="array") 
#        | .[1] 
#        | capture("\\.(?<ext>[^.]+)$").ext' matching_repos1.ndjson \
#   | sort \
#   | uniq -c \
#   | sort -nr


# Results:
# - 10653580 pde
# - 10398976 clj
# - 1959222 js
# - 723298 h
# - 609888 cpp
# - 463888 scd
# - 172269 v4p
# - 84096 toe
# - 61005 tox
# - 11836 ndbx   


import matplotlib.pyplot as plt

# Data
extensions = ["pde", "clj", "js", "h", "cpp", "scd", "v4p", "toe", "tox", "ndbx"]
counts = [10653580, 10398976, 1959222, 723298, 609888, 463888, 172269, 84096, 61005, 11836]

# # --- PIE CHART ---
# plt.figure(figsize=(8, 8))
# plt.pie(
#     counts,
#     labels=extensions,
#     autopct="%1.1f%%",
#     startangle=140
# )
# plt.title("File Extension Distribution - Pie Chart")
# plt.tight_layout()
# plt.show()

# --- HORIZONTAL BAR CHART ---
plt.figure(figsize=(10, 6))
plt.barh(extensions, counts, color="purple")
plt.xlabel("Count")
plt.title("File Extension Distribution")
plt.gca().invert_yaxis()  # Largest at the top

# Add labels at the end of each bar
for i, v in enumerate(counts):
    plt.text(v + max(counts) * 0.01, i, f"{v:,}", va="center")

plt.tight_layout()
plt.show()
