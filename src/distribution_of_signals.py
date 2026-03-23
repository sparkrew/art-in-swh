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
import matplotlib.patches as mpatches
import numpy as np

# Data
extensions = ["p5", "processing", "openFrameworks", "supercollider", "touchDesigner", "vvvv", "nodebox"]
counts = [1140992, 430912, 80289, 21518, 8625, 1901, 335]
total = sum(counts)
pie_len = 3

palette = ["#4C72B0","#DD8452","#55A868","#C44E52","#8172B2","#937860","#DA8BC3","#8C8C8C","#CCB974"]

fig = plt.figure(figsize=(13, 5.5), facecolor="#f5f4f0")

# ── LEFT: Donut ──────────────────────────────────────────────────────────────
ax1 = fig.add_axes([0.01, 0.06, 0.38, 0.88])
ax1.set_facecolor("#f5f4f0")

other = sum(counts[pie_len:])
donut_vals   = counts[:pie_len] + [other]
donut_labels = extensions[:pie_len] + ["other"]
donut_colors = palette[:3] + ["#d0d0c8"]

wedges, _ = ax1.pie(
    donut_vals,
    labels=None,
    colors=donut_colors,
    startangle=90,
    wedgeprops=dict(width=0.55, edgecolor="#f5f4f0", linewidth=2),
    counterclock=False,
)

ax1.text(0, 0.08, "1.68M", ha="center", va="center", fontsize=16,
         fontweight="500", color="#2c2c2a")
ax1.text(0, -0.18, "total files", ha="center", va="center", fontsize=10,
         color="#73726c")

legend_patches = [
    mpatches.Patch(color=donut_colors[i], label=f"{donut_labels[i]} — {donut_vals[i]/total*100:.1f}%")
    for i in range(len(donut_labels))
]
ax1.legend(handles=legend_patches, loc="lower center", bbox_to_anchor=(0.5, -0.12),
           frameon=False, fontsize=10, labelcolor="#73726c", ncol=1,
           handlelength=1.2, handleheight=0.9, borderpad=0)

ax1.set_title("Share of total", fontsize=10, color="#73726c", pad=6, fontweight="normal")

# ── RIGHT: Horizontal bar (log scale) ────────────────────────────────────────
ax2 = fig.add_axes([0.42, 0.08, 0.56, 0.84])
ax2.set_facecolor("#f5f4f0")

y_pos = np.arange(len(extensions))
bars = ax2.barh(y_pos, counts, color=palette, height=0.62, edgecolor="none")

for bar, count in zip(bars, counts):
    pct = count / total * 100
    label = f"{count:,}  ({pct:.1f}%)"
    x = bar.get_width()
    ax2.text(x * 1.05, bar.get_y() + bar.get_height() / 2,
             label, va="center", ha="left", fontsize=9, color="#2c2c2a")

ax2.set_yticks(y_pos)
ax2.set_yticklabels(extensions, fontsize=11, fontfamily="monospace", color="#2c2c2a")
ax2.set_xscale("log")
ax2.set_xlim(100, 12_000_000)
ax2.xaxis.set_tick_params(labelsize=9, labelcolor="#73726c")

ax2.set_xticks([100, 1_000, 10_000, 100_000, 1_000_000])
ax2.set_xticklabels(["100", "1K", "10K", "100K", "1M"], fontsize=9, color="#73726c")

ax2.tick_params(axis="y", length=0)
ax2.tick_params(axis="x", length=3, color="#d3d1c7")
ax2.spines[["top", "right", "left"]].set_visible(False)
ax2.spines["bottom"].set_color("#d3d1c7")
ax2.spines["bottom"].set_linewidth(0.5)

for gridline in ax2.xaxis.get_gridlines():
    gridline.set_color("#d3d1c7")
    gridline.set_linewidth(0.5)
ax2.xaxis.grid(True, which="major", color="#d3d1c7", linewidth=0.5)
ax2.set_axisbelow(True)
ax2.invert_yaxis()
ax2.set_title("All extensions (log scale)", fontsize=10, color="#73726c",
              pad=6, fontweight="normal", loc="left")

plt.savefig("pie_bar_file_extensions.png", dpi=180, bbox_inches="tight", facecolor="#f5f4f0")
plt.show()