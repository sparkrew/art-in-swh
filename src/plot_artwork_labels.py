import json
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt


# =========================
# CONFIG
# =========================

INPUT_FILE = Path("../artworks/predictions.json")
OUTPUT_FILE = Path("../artworks/predicted_labels_distribution.png")


# =========================
# HELPERS
# =========================

def load_predictions(file_path: Path):
    """Load the predictions JSON file."""
    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def count_labels(predictions):
    """
    Count labels for each dimension separately.
    Example dimensions: entities, interaction, outcome
    """
    counts = {
        "entities": Counter(),
        "interaction": Counter(),
        "outcome": Counter(),
    }

    for item in predictions:
        predicted_labels = item.get("predicted_labels", {})

        for dimension in counts.keys():
            labels = predicted_labels.get(dimension, [])

            if isinstance(labels, str):
                labels = [labels]

            for label in labels:
                counts[dimension][label] += 1

    return counts


def plot_distribution(counts, total_files: int, output_file: Path):
    """Create one subplot per dimension and save the figure."""
    dimensions = ["entities", "interaction", "outcome"]

    fig, axes = plt.subplots(3, 1, figsize=(12, 14))
    fig.suptitle(
        f"Predicted labels distribution\nTotal files read: {total_files}",
        fontsize=14
    )

    for ax, dimension in zip(axes, dimensions):
        counter = counts[dimension]

        if not counter:
            ax.set_title(dimension)
            ax.text(0.5, 0.5, "No data", ha="center", va="center")
            ax.axis("off")
            continue

        # Sort by count descending
        items = sorted(counter.items(), key=lambda x: x[1], reverse=True)
        labels = [item[0] for item in items]
        values = [item[1] for item in items]

        ax.bar(labels, values)
        ax.set_title(dimension)
        ax.set_ylabel("Count")
        ax.tick_params(axis="x", rotation=45)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close()


# =========================
# MAIN
# =========================

def main():
    predictions = load_predictions(INPUT_FILE)
    total_files = len(predictions)
    counts = count_labels(predictions)
    plot_distribution(counts, total_files, OUTPUT_FILE)

    print(f"Saved plot to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()