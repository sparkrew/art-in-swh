import json
import re
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt


# =========================
# CONFIG
# =========================

# JSON file containing the examples with:
# - classification
# - predicted_classification
INPUT_JSON = Path("../artworks/examples_prompt10.json")

# Folder where plots will be saved
OUTPUT_DIR = Path("../artworks/plots")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =========================
# HELPERS
# =========================

def count_labels(examples, classification_key):
    """Count labels like entities_randomness, interaction_yes, etc."""
    counter = Counter()

    for ex in examples:
        classification = ex.get(classification_key, {})

        for dimension, labels in classification.items():
            if isinstance(labels, str):
                labels = [labels]

            for label in labels:
                counter[f"{dimension}_{label}"] += 1

    return counter


def safe_stem(path: Path) -> str:
    """Create a safe name from the input file stem."""
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", path.stem)


def plot_all_distributions(examples, output_path: Path):
    """Plot all label distributions together and save the figure."""
    true_counts = count_labels(examples, "classification")
    pred_counts = count_labels(examples, "predicted_classification")

    all_labels = sorted(set(true_counts) | set(pred_counts))
    x = range(len(all_labels))
    width = 0.4

    plt.figure(figsize=(12, 5))
    plt.bar(
        [i - width / 2 for i in x],
        [true_counts.get(label, 0) for label in all_labels],
        width=width,
        label="classification",
    )
    plt.bar(
        [i + width / 2 for i in x],
        [pred_counts.get(label, 0) for label in all_labels],
        width=width,
        label="predicted_classification",
    )

    plt.xticks(x, all_labels, rotation=45, ha="right")
    plt.ylabel("Count")
    plt.title("Classification vs Predicted Classification")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


def plot_distributions_by_dimension(examples, output_dir: Path, base_name: str):
    """Plot one figure per dimension and save each one."""
    true_counts = count_labels(examples, "classification")
    pred_counts = count_labels(examples, "predicted_classification")

    for dimension in ["entities", "interaction", "outcome"]:
        labels = sorted([
            key.split("_", 1)[1]
            for key in set(true_counts) | set(pred_counts)
            if key.startswith(f"{dimension}_")
        ])

        if not labels:
            continue

        x = range(len(labels))
        width = 0.4

        plt.figure(figsize=(8, 4))
        plt.bar(
            [i - width / 2 for i in x],
            [true_counts.get(f"{dimension}_{label}", 0) for label in labels],
            width=width,
            label="classification",
        )
        plt.bar(
            [i + width / 2 for i in x],
            [pred_counts.get(f"{dimension}_{label}", 0) for label in labels],
            width=width,
            label="predicted_classification",
        )

        plt.xticks(x, labels, rotation=45, ha="right")
        plt.ylabel("Count")
        plt.title(f"{dimension}: classification vs predicted")
        plt.legend()
        plt.tight_layout()
        plt.savefig(output_dir / f"{base_name}_{dimension}.png", dpi=300, bbox_inches="tight")
        plt.close()


# =========================
# MAIN
# =========================

def main():
    with INPUT_JSON.open("r", encoding="utf-8") as f:
        examples = json.load(f)

    base_name = safe_stem(INPUT_JSON)

    plot_all_distributions(
        examples,
        OUTPUT_DIR / f"{base_name}_all.png",
    )

    plot_distributions_by_dimension(
        examples,
        OUTPUT_DIR,
        base_name,
    )

    print(f"Plots saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()