import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


# =========================
# CONFIG
# =========================

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

PROMPT_FOLDER_NAME = "PROMPT_10f_20260603"

PROMPT_DIR = PROJECT_ROOT / "artworks" / PROMPT_FOLDER_NAME

CLEAN_JSON_PATH = PROMPT_DIR / "clean_artworks_label_prediction.json"

SRC_ROOT_DIR = Path(
    "/home/rpinter/links/projects/def-baudry/shared/data/artworks/src"
)

OUTPUT_DIR = PROMPT_DIR / "label_distribution_manual_check"

TOP10_NOTEBOOK_DIR = OUTPUT_DIR / "top10_label_combinations_notebooks"

N_TOP_COMBINATIONS = 20
N_SAMPLES_PER_COMBINATION = 20
RANDOM_SEED = 8

EXCLUDE_TERMS = [
    "Coding Train",
    "Daniel Shiffman",
]


# =========================
# BASIC HELPERS
# =========================

def read_json(file_path: Path):
    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(data, file_path: Path):
    file_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def ensure_list(value):
    if value is None:
        return []

    if isinstance(value, list):
        return value

    return [value]


def sorted_join(values):
    values = ensure_list(values)
    values = [str(x) for x in values if x is not None]

    return " + ".join(sorted(values))


def normalize_path(path: str) -> str:
    """
    Convert absolute artwork paths to paths relative to SRC_ROOT_DIR.
    """
    path = str(path)

    marker = "/artworks/src/"
    if marker in path:
        return path.split(marker, 1)[-1].lstrip("/")

    return path.lstrip("/")


def slugify(text: str, max_length: int = 90) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = text.strip("_")

    if len(text) > max_length:
        text = text[:max_length].rstrip("_")

    return text or "label_combination"


# =========================
# LABEL HELPERS
# =========================

def labels_key(item: dict) -> dict:
    return item.get("predicted_labels", {})


def all_characteristics_combo(labels: dict) -> str:
    entities = sorted_join(labels.get("entities", [])) or "none"
    interaction = sorted_join(labels.get("interaction", [])) or "none"
    outcome = sorted_join(labels.get("outcome", [])) or "none"

    return f"{entities} | interaction={interaction} | {outcome}"


def entities_combo(labels: dict) -> str:
    entities = sorted_join(labels.get("entities", [])) or "none"

    return entities


def interaction_outcome_combo(labels: dict) -> str:
    interaction = sorted_join(labels.get("interaction", [])) or "none"
    outcome = sorted_join(labels.get("outcome", [])) or "none"

    return f"interaction={interaction} | {outcome}"


def add_label_combination(item: dict) -> dict:
    item = dict(item)
    item["label_combination"] = all_characteristics_combo(
        labels_key(item)
    )
    return item


# =========================
# SOURCE CODE FILTERING
# =========================

def read_source_code(item: dict) -> tuple[str | None, Path]:
    relative_file_path = normalize_path(item["file_path"])
    src_path = SRC_ROOT_DIR / relative_file_path

    if not src_path.exists():
        return None, src_path

    code = src_path.read_text(encoding="utf-8", errors="ignore")

    return code, src_path


def contains_excluded_term(code: str) -> bool:
    code_lower = code.lower()

    for term in EXCLUDE_TERMS:
        if term.lower() in code_lower:
            return True

    return False


def filter_items_by_source_code(data: list[dict]) -> tuple[list[dict], dict]:
    """
    Keep only items whose source code exists and does not contain excluded terms.
    """
    kept_items = []
    missing_source_files = []
    excluded_items = []

    for item in data:
        code, src_path = read_source_code(item)

        if code is None:
            missing_source_files.append(str(src_path))
            continue

        if contains_excluded_term(code):
            excluded_items.append(normalize_path(item["file_path"]))
            continue

        kept_items.append(item)

    summary = {
        "total_items_before_filter": len(data),
        "total_items_after_filter": len(kept_items),
        "total_missing_source_files": len(missing_source_files),
        "total_excluded_by_terms": len(excluded_items),
        "exclude_terms": EXCLUDE_TERMS,
        "missing_source_files": missing_source_files,
        "excluded_items": excluded_items,
    }

    return kept_items, summary


# =========================
# DISTRIBUTIONS
# =========================

def counter_to_dataframe(counter: Counter, label_column: str) -> pd.DataFrame:
    total = sum(counter.values())

    rows = []

    for label, count in counter.most_common():
        percentage = count / total if total else 0

        rows.append(
            {
                label_column: label,
                "count": count,
                "percentage": percentage,
            }
        )

    return pd.DataFrame(rows)


def calculate_distributions(data: list[dict]) -> dict[str, pd.DataFrame]:
    labels = [labels_key(item) for item in data]

    all_combo_counts = Counter(
        all_characteristics_combo(x) for x in labels
    )

    entity_counts = Counter()

    for x in labels:
        entity_counts.update(ensure_list(x.get("entities", [])))

    entity_combo_counts = Counter(
        entities_combo(x) for x in labels
    )

    interaction_outcome_counts = Counter(
        interaction_outcome_combo(x) for x in labels
    )

    return {
        "all_characteristic_combinations": counter_to_dataframe(
            all_combo_counts,
            label_column="label_combination",
        ),
        "entities": counter_to_dataframe(
            entity_counts,
            label_column="entity",
        ),
        "entity_combinations": counter_to_dataframe(
            entity_combo_counts,
            label_column="entity_combination",
        ),
        "interaction_outcome_combinations": counter_to_dataframe(
            interaction_outcome_counts,
            label_column="interaction_outcome_combination",
        ),
    }


def save_distribution_tables(
    distributions: dict[str, pd.DataFrame],
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    for name, df in distributions.items():
        df.to_csv(output_dir / f"{name}.csv", index=False)


# =========================
# PLOTS
# =========================

# def plot_counts_vertical(
#     df: pd.DataFrame,
#     label_column: str,
#     title: str,
#     xlabel: str,
#     output_path: Path,
#     top_n: int | None = None,
# ) -> None:
#     plot_df = df.copy()

#     if top_n is not None:
#         plot_df = plot_df.head(top_n)

#     if plot_df.empty:
#         return

#     fig_width = max(8, min(24, len(plot_df) * 0.7))
#     fig_height = 6

#     plt.figure(figsize=(fig_width, fig_height))
#     plt.bar(plot_df[label_column], plot_df["count"])
#     plt.title(title)
#     plt.xlabel(xlabel)
#     plt.ylabel("count")
#     plt.xticks(rotation=45, ha="right")
#     plt.tight_layout()
#     plt.savefig(output_path, dpi=200)
#     plt.close()

def plot_counts_vertical(
    df: pd.DataFrame,
    label_column: str,
    title: str,
    xlabel: str,
    output_path: Path,
    top_n: int | None = None,
    show_percentages: bool = False,
) -> None:
    plot_df = df.copy()

    if top_n is not None:
        plot_df = plot_df.head(top_n)

    if plot_df.empty:
        return

    fig_width = max(8, min(24, len(plot_df) * 0.7))
    fig_height = 6

    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    bars = ax.bar(plot_df[label_column], plot_df["count"])

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("count")
    ax.tick_params(axis="x", rotation=45)

    for label in ax.get_xticklabels():
        label.set_ha("right")

    if show_percentages:
        max_count = plot_df["count"].max()
        ax.set_ylim(0, max_count * 1.15)

        for bar, percentage in zip(bars, plot_df["percentage"]):
            height = bar.get_height()

            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f"{percentage:.1%}",
                ha="center",
                va="bottom",
                fontsize=9,
            )

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=200,
        bbox_inches="tight",
        pad_inches=0.3,
    )

    plt.close()


def plot_counts_horizontal(
    df: pd.DataFrame,
    label_column: str,
    title: str,
    xlabel: str,
    output_path: Path,
    top_n: int | None = None,
) -> None:
    plot_df = df.copy()

    if top_n is not None:
        plot_df = plot_df.head(top_n)

    if plot_df.empty:
        return

    plot_df = plot_df.iloc[::-1]

    fig_width = 12
    fig_height = max(8, min(120, len(plot_df) * 0.45))

    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    ax.barh(plot_df[label_column], plot_df["count"])
    ax.set_title(title)
    ax.set_xlabel("count")
    ax.set_ylabel(xlabel)

    ax.tick_params(axis="y", labelsize=8)

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=200,
        bbox_inches="tight",
        pad_inches=0.4,
    )

    plt.close()


def save_distribution_plots(
    distributions: dict[str, pd.DataFrame],
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    plot_counts_horizontal(
        distributions["all_characteristic_combinations"],
        label_column="label_combination",
        title="Distribution of All Characteristic Combinations",
        xlabel="combination",
        output_path=output_dir / "all_characteristic_combinations_top50.png",
        top_n=50,
    )

    plot_counts_horizontal(
        distributions["all_characteristic_combinations"],
        label_column="label_combination",
        title="Distribution of All Characteristic Combinations - Top 8",
        xlabel="combination",
        output_path=output_dir / "all_characteristic_combinations_top8.png",
        top_n=8,
    )

    plot_counts_vertical(
        distributions["entities"],
        label_column="entity",
        title="Distribution of Entities",
        xlabel="entity",
        output_path=output_dir / "entities.png",
    )

    plot_counts_horizontal(
        distributions["entity_combinations"],
        label_column="entity_combination",
        title="Distribution of Entity Combinations",
        xlabel="entity combination",
        output_path=output_dir / "entity_combinations_top50.png",
        top_n=50,
    )

    plot_counts_horizontal(
        distributions["entity_combinations"],
        label_column="entity_combination",
        title="Distribution of Entity Combinations",
        xlabel="entity combination",
        output_path=output_dir / "entity_combinations_top10.png",
        top_n=10,
    )

    plot_counts_vertical(
        distributions["interaction_outcome_combinations"],
        label_column="interaction_outcome_combination",
        title="Distribution of Interaction + Outcome Combinations",
        xlabel="interaction + outcome",
        output_path=output_dir / "interaction_outcome_combinations.png",
        show_percentages=True
    )


# =========================
# NOTEBOOK HELPERS
# =========================

def make_markdown_cell(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source,
    }


def make_code_cell(source: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source,
    }


def create_notebook_for_label_combination(
    output_path: Path,
    rank: int,
    label_combination: str,
    count_in_clean_json: int,
    sampled_items: list[dict],
) -> None:
    cells = []

    setup_cell = f"""
from pathlib import Path
from IPython.display import Markdown, display
import json

SRC_ROOT_DIR = Path({str(SRC_ROOT_DIR)!r})

def print_code_file(relative_file_path, language="javascript"):
    file_path = SRC_ROOT_DIR / relative_file_path
    code = file_path.read_text(encoding="utf-8", errors="ignore")

    display(Markdown(f"```{{language}}\\n{{code}}\\n```"))
""".strip()

    cells.append(make_code_cell(setup_cell))

    cells.append(
        make_markdown_cell(
            f"# Manual check — Top label combination {rank}\n\n"
            f"Prompt folder: `{PROMPT_FOLDER_NAME}`\n\n"
            f"Rank: `{rank}`\n\n"
            f"Label combination:\n\n"
            f"`{label_combination}`\n\n"
            f"Count in clean JSON: `{count_in_clean_json}`\n\n"
            f"Samples in this notebook: `{len(sampled_items)}`\n\n"
            f"Excluded source-code terms: `{', '.join(EXCLUDE_TERMS)}`"
        )
    )

    if not sampled_items:
        cells.append(
            make_markdown_cell(
                "No valid samples were available after filtering."
            )
        )
    else:
        path_list = "\n".join(
            f"{i}. `{normalize_path(item['file_path'])}`"
            for i, item in enumerate(sampled_items, start=1)
        )

        cells.append(
            make_markdown_cell(
                f"## Sample paths\n\n{path_list}"
            )
        )

    for sample_index, item in enumerate(sampled_items, start=1):
        relative_file_path = normalize_path(item["file_path"])

        labels_text = json.dumps(
            item.get("predicted_labels", {}),
            indent=2,
            ensure_ascii=False,
        )

        cells.append(
            make_markdown_cell(
                f"## Sample {sample_index}\n\n"
                f"**File path:**\n\n"
                f"`{relative_file_path}`\n\n"
                f"**Predicted labels:**\n\n"
                f"```json\n{labels_text}\n```\n\n"
                f"### Manual notes\n\n"
            )
        )

        cells.append(
            make_code_cell(
                f"print_code_file({relative_file_path!r})"
            )
        )

    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "pygments_lexer": "ipython3",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }

    output_path.write_text(
        json.dumps(notebook, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def create_top10_notebooks(
    full_data: list[dict],
    filtered_data: list[dict],
    all_distributions: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    TOP10_NOTEBOOK_DIR.mkdir(parents=True, exist_ok=True)

    rng = random.Random(RANDOM_SEED)

    top_combinations_df = all_distributions[
        "all_characteristic_combinations"
    ].head(N_TOP_COMBINATIONS)

    filtered_items_by_combo = defaultdict(list)

    for item in filtered_data:
        combo = all_characteristics_combo(labels_key(item))
        filtered_items_by_combo[combo].append(item)

    summary_rows = []

    for rank, row in enumerate(top_combinations_df.itertuples(index=False), start=1):
        label_combination = row.label_combination
        count_in_clean_json = row.count

        available_items = filtered_items_by_combo.get(label_combination, [])
        sample_size = min(N_SAMPLES_PER_COMBINATION, len(available_items))
        sampled_items = rng.sample(available_items, sample_size)

        slug = slugify(label_combination)
        notebook_name = f"{rank:02d}_{slug}_15_random_src.ipynb"
        notebook_path = TOP10_NOTEBOOK_DIR / notebook_name

        create_notebook_for_label_combination(
            output_path=notebook_path,
            rank=rank,
            label_combination=label_combination,
            count_in_clean_json=count_in_clean_json,
            sampled_items=sampled_items,
        )

        summary_rows.append(
            {
                "rank": rank,
                "label_combination": label_combination,
                "count_in_clean_json": count_in_clean_json,
                "available_after_filter": len(available_items),
                "sampled": sample_size,
                "notebook_path": str(notebook_path),
            }
        )

        print(f"Saved notebook: {notebook_path}")

    return pd.DataFrame(summary_rows)


# =========================
# MAIN
# =========================

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    TOP10_NOTEBOOK_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Prompt folder: {PROMPT_DIR}")
    print(f"Clean JSON: {CLEAN_JSON_PATH}")
    print(f"Source root folder: {SRC_ROOT_DIR}")
    print(f"Output folder: {OUTPUT_DIR}")
    print(f"Top 10 notebook folder: {TOP10_NOTEBOOK_DIR}")
    print()

    if not CLEAN_JSON_PATH.exists():
        raise FileNotFoundError(
            f"Could not find clean JSON: {CLEAN_JSON_PATH}"
        )

    data = read_json(CLEAN_JSON_PATH)

    # -------------------------
    # Full clean JSON outputs
    # -------------------------

    print("Calculating distributions for all cleaned files...")

    all_distributions = calculate_distributions(data)

    save_distribution_tables(
        distributions=all_distributions,
        output_dir=OUTPUT_DIR / "tables_all_cleaned_files",
    )

    save_distribution_plots(
        distributions=all_distributions,
        output_dir=OUTPUT_DIR / "plots_all_cleaned_files",
    )

    # -------------------------
    # Filtered outputs
    # -------------------------

    print("Filtering files that contain Coding Train or Daniel Shiffman...")

    filtered_data, filtering_summary = filter_items_by_source_code(data)

    write_json(
        filtering_summary,
        OUTPUT_DIR / "filtering_summary.json",
    )

    print(
        f"Kept {len(filtered_data)} of {len(data)} items "
        f"after filtering."
    )

    print("Calculating distributions for filtered files...")

    filtered_distributions = calculate_distributions(filtered_data)

    save_distribution_tables(
        distributions=filtered_distributions,
        output_dir=OUTPUT_DIR / "tables_excluding_coding_train_daniel_shiffman",
    )

    save_distribution_plots(
        distributions=filtered_distributions,
        output_dir=OUTPUT_DIR / "plots_excluding_coding_train_daniel_shiffman",
    )

    # -------------------------
    # Top 10 notebooks
    # -------------------------

    print("Creating one notebook per top label combination...")

    top10_summary_df = create_top10_notebooks(
        full_data=data,
        filtered_data=filtered_data,
        all_distributions=all_distributions,
    )

    top10_summary_df.to_csv(
        OUTPUT_DIR / "top10_label_combination_notebook_summary.csv",
        index=False,
    )

    print()
    print("Done.")
    print(f"All outputs saved in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()