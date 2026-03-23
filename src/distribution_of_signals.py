###
# Command to extract all signals
#
# jq -r '
#   .[]?                                     # iterate over each object (if array)
#   | .metadata.SWH_signals.enum[]?           # extract each signal
# ' all_origins_final_version.json \
# | sort \
# | uniq -c \
# | sort -nr
#
# Results:
# 1140992 .js
#  430912 .pde
#   40352 .h
#   39937 .cpp
#   21518 .scd
#    5469 .toe
#    3156 .tox
#    1901 .v4p
#     335 .ndbx


import matplotlib.pyplot as plt

# Data
extensions = [".js", ".pde", ".h", ".cpp", ".scd", ".toe", ".tox", ".v4p", ".ndbx"]
counts = [1140992, 430912, 40352, 39937, 21518, 5469, 3156, 1901, 335]

# --- PIE CHART ---
plt.figure(figsize=(8, 8))

colors = plt.get_cmap("tab10").colors

def autopct_func(pct):
    return f"{pct:.1f}%" if pct >= 2 else ""

# Build legend labels
legend_labels = [
    f"{ext} ({c:,})"
    for ext, c in zip(extensions, counts)
]

wedges, _, _ = plt.pie(
    counts,
    colors=colors,
    autopct=autopct_func,
    startangle=140
)

plt.legend(
    wedges,
    legend_labels,
    title="Extensions",
    loc="center left",
    bbox_to_anchor=(1, 0.5)
)

plt.title("Distribution of signals")
plt.tight_layout()
plt.show()

# # --- HORIZONTAL BAR CHART ---
# import matplotlib.pyplot as plt

# data = sorted(zip(extensions, counts), key=lambda x: x[1], reverse=True)
# extensions, counts = zip(*data)

# # Percentages
# total = sum(counts)
# percentages = [(c / total) * 100 for c in counts]

# plt.figure(figsize=(10, 6))

# bars = plt.bar(extensions, counts)

# # plt.yscale("log")
# plt.ylabel("Count")
# plt.title("File Extension Distribution")

# # Rotate x labels for readability
# plt.xticks(rotation=45, ha="right")

# # Add labels on top of bars
# for i, (v, pct) in enumerate(zip(counts, percentages)):
#     plt.text(
#         i,
#         v,
#         f"{v:,}\n({pct:.1f}%)",
#         ha="center",
#         va="bottom",
#         fontsize=9
#     )

# plt.tight_layout()
# plt.show()