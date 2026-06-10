import argparse
import json
import time
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# =========================
# PATH HELPERS
# =========================

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent


def resolve_path(path: str | Path, base_dir: Path = PROJECT_ROOT) -> Path:
    """
    Resolve relative paths from PROJECT_ROOT instead of the current terminal folder.

    Default assumption:
    - this script lives one folder below the project root
    - project root contains data/ and artworks/
    """
    path = Path(path).expanduser()
    if path.is_absolute():
        return path
    return (base_dir / path).resolve()


def read_json(file_path: Path):
    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(file_path: Path, data) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def save_figure(fig, file_path: Path) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(file_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def normalize_path(path) -> str:
    """
    Convert absolute artwork paths to the shared relative path.

    Example:
    /home/.../artworks/src/user/repo/sketch.js
    becomes:
    user/repo/sketch.js
    """
    path = str(path)

    marker = "/artworks/src/"
    if marker in path:
        return path.split(marker, 1)[-1].lstrip("/")

    return path.lstrip("/")


def ensure_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


# =========================
# DATA PROCESSING
# =========================

def load_files_to_remove(data_dir: Path) -> set[str]:
    files_to_rm = []

    for filename in ["empty_p5functions.json", "less_than_3_p5functions.json"]:
        file_path = data_dir / filename
        data = read_json(file_path)

        for item in data:
            if "artwork" in item:
                files_to_rm.append(normalize_path(item["artwork"]))

    return set(files_to_rm)


def load_predictions(predictions_file: Path) -> list[dict]:
    raw_preds = read_json(predictions_file)

    for artwork in raw_preds:
        artwork["file_path"] = normalize_path(artwork["file_path"])

    return raw_preds


def clean_predictions(raw_preds: list[dict], files_to_rm: set[str]) -> list[dict]:
    # Remove files with few or no functions
    preds = [
        pred for pred in raw_preds
        if normalize_path(pred["file_path"]) not in files_to_rm
    ]

    # Remove hallucinated labels in the entities
    for artwork in preds:
        predicted_labels = artwork.get("predicted_labels", {})

        predicted_labels["entities"] = ensure_list(predicted_labels.get("entities", []))
        predicted_labels["interaction"] = ensure_list(predicted_labels.get("interaction", []))
        predicted_labels["outcome"] = ensure_list(predicted_labels.get("outcome", []))

        for label in ["auditory", "visual", "time_based"]:
            while label in predicted_labels["entities"]:
                predicted_labels["entities"].remove(label)

    return preds


def add_label_combination(preds: list[dict]) -> None:
    for pred in preds:
        labels = pred["predicted_labels"]

        entities = labels.get("entities", [])
        interactions = labels.get("interaction", [])
        outcomes = labels.get("outcome", [])

        pred["label_combination"] = (
            f"entities={entities} | "
            f"interaction={interactions} | "
            f"outcome={outcomes}"
        )


def save_processed_json_outputs(preds: list[dict], experiment_dir: Path) -> None:
    write_json(
        experiment_dir / "clean_artworks_label_prediction.json",
        preds,
    )

    no_entities = [
        pred for pred in preds
        if not pred["predicted_labels"]["entities"]
    ]

    write_json(
        experiment_dir / "clean_artworks_label_prediction_no_entities.json",
        no_entities,
    )

    interactive_and_static = [
        pred for pred in preds
        if "yes" in pred["predicted_labels"]["interaction"]
        and "static" in pred["predicted_labels"]["outcome"]
    ]

    write_json(
        experiment_dir / "clean_artworks_label_prediction_interactive_static.json",
        interactive_and_static,
    )

    no_interaction_random_visual_time_based = [
        pred for pred in preds
        if (
            "entities=['synthesized_image'] | "
            "interaction=['no'] | "
            "outcome=['visual', 'time_based']"
        ) in pred["label_combination"]
    ]

    write_json(
        experiment_dir / "clean_artworks_label_prediction_no_intrand_visual_static.json",
        no_interaction_random_visual_time_based,
    )

    top9 = [
        pred for pred in preds
        if (
            "entities=['processed_image', 'processed_audio', 'randomness'] | "
            "interaction=['yes'] | "
            "outcome=['visual', 'auditory', 'time_based']"
        ) in pred["label_combination"]
    ]

    write_json(
        experiment_dir / "clean_artworks_label_prediction_top9.json",
        top9,
    )


# =========================
# PLOTS
# =========================

def plot_label_group_counts(preds: list[dict], figures_dir: Path) -> None:
    label_groups = ["entities", "interaction", "outcome"]
    counts = {}

    for group in label_groups:
        counter = Counter()
        for pred in preds:
            labels = pred.get("predicted_labels", {}).get(group, [])
            counter.update(labels)
        counts[group] = counter

    total_files = len(preds)
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    for ax, group in zip(axes, label_groups):
        counter = counts[group]
        labels = list(counter.keys())
        values = list(counter.values())

        ax.bar(labels, values)
        ax.set_title(group)
        ax.set_ylabel("Number of files")
        ax.tick_params(axis="x", rotation=45)

    fig.suptitle(f"Predicted Labels Count Across {total_files} Files", fontsize=16)
    fig.tight_layout()

    save_figure(fig, figures_dir / "predicted_label_counts.png")


def plot_label_combination_distribution(preds: list[dict], figures_dir: Path) -> None:
    label_counts = Counter(pred["label_combination"] for pred in preds)
    sorted_items = label_counts.most_common()

    labels = [item[0] for item in sorted_items]
    values = [item[1] for item in sorted_items]

    fig, ax = plt.subplots(figsize=(12, max(5, len(labels) * 0.35)))

    ax.barh(labels, values)
    ax.set_xlabel("Number of files")
    ax.set_ylabel("Label set")
    ax.set_title(f"Distribution of Concatenated Label Sets Across {len(preds)} Files")
    ax.invert_yaxis()

    fig.tight_layout()

    save_figure(fig, figures_dir / "label_combination_distribution.png")


def build_plot_data(preds: list[dict]) -> pd.DataFrame:
    rows = []

    for pred in preds:
        labels = pred["predicted_labels"]

        entities = labels.get("entities", [])
        interactions = labels.get("interaction", [])
        outcomes = labels.get("outcome", [])

        modality_outcomes = [
            x for x in outcomes
            if x in ["visual", "auditory"]
        ]

        axis_label = " | ".join([
            "entities=" + ", ".join(entities),
            "outcome=" + ", ".join(modality_outcomes),
        ])

        time_outcomes = [
            x for x in outcomes
            if x in ["static", "time_based"]
        ]

        for interaction in interactions:
            for time_outcome in time_outcomes:
                rows.append({
                    "axis_label": axis_label,
                    "color_group": f"interaction={interaction} | outcome={time_outcome}",
                })

    df_plot = pd.DataFrame(rows)

    if df_plot.empty:
        return pd.DataFrame()

    plot_data = pd.crosstab(
        df_plot["axis_label"],
        df_plot["color_group"],
    )

    plot_data["total"] = plot_data.sum(axis=1)

    plot_data = (
        plot_data
        .sort_values("total", ascending=False)
        .drop(columns="total")
    )

    return plot_data


def plot_full_stacked_distribution(
    plot_data: pd.DataFrame,
    total_files: int,
    figures_dir: Path,
) -> None:
    if plot_data.empty:
        return

    ax = plot_data.plot(
        kind="barh",
        stacked=True,
        figsize=(18, max(5, len(plot_data) * 0.35)),
    )

    fig = ax.get_figure()

    ax.set_xlabel("Number of files")
    ax.set_ylabel("Entity + visual/auditory outcome")
    ax.set_title(f"Distribution of Labels Across {total_files} Files")

    ax.legend(
        loc="upper right",
        bbox_to_anchor=(1, 0.90),
    )

    ax.invert_yaxis()
    fig.tight_layout()

    save_figure(fig, figures_dir / "label_distribution_stacked_full.png")


def plot_top_label_groups_with_others(
    plot_data: pd.DataFrame,
    total_files: int,
    figures_dir: Path,
    top_n: int = 25,
) -> None:
    if plot_data.empty:
        return

    plot_data_with_total = plot_data.copy()
    plot_data_with_total["total"] = plot_data_with_total.sum(axis=1)
    plot_data_with_total = plot_data_with_total.sort_values("total", ascending=False)

    top_data = plot_data_with_total.head(top_n).drop(columns="total")
    other_data = plot_data_with_total.iloc[top_n:].drop(columns="total")

    if len(other_data) > 0:
        other_row = other_data.sum(axis=0).to_frame().T
        other_row.index = ["Others"]
        plot_data_top = pd.concat([top_data, other_row])
    else:
        plot_data_top = top_data

    ax = plot_data_top.plot(
        kind="barh",
        stacked=True,
        figsize=(12, max(5, len(plot_data_top) * 0.35)),
    )

    fig = ax.get_figure()

    ax.set_xlabel("Number of files")
    ax.set_ylabel("Entity + visual/auditory outcome")
    ax.set_title(f"Top {top_n} Label Groups + Others Across {total_files} Files")

    ax.legend(
        loc="upper right",
        bbox_to_anchor=(1, 0.75),
    )

    ax.invert_yaxis()
    fig.tight_layout()

    save_figure(fig, figures_dir / f"top_{top_n}_label_groups_with_others_stacked.png")


def plot_top_label_groups_with_others_outline(
    plot_data: pd.DataFrame,
    total_files: int,
    figures_dir: Path,
    top_n: int = 25,
) -> None:
    if plot_data.empty:
        return

    plot_data_clean = plot_data.drop(columns=["total"], errors="ignore")

    totals = plot_data_clean.sum(axis=1)
    plot_data_sorted = plot_data_clean.loc[
        totals.sort_values(ascending=False).index
    ]

    top_data = plot_data_sorted.head(top_n)
    other_total = plot_data_sorted.iloc[top_n:].sum().sum()
    has_others = other_total > 0

    y_labels = list(top_data.index)
    if has_others:
        y_labels.append("Others")

    y = np.arange(len(y_labels))

    fig, ax = plt.subplots(
        figsize=(18, max(5, len(y_labels) * 0.35)),
    )

    left = np.zeros(len(top_data))

    for col in top_data.columns:
        values = top_data[col].values

        ax.barh(
            y[:len(top_data)],
            values,
            left=left,
            label=col,
        )

        left += values

    if has_others:
        ax.barh(
            y[-1],
            other_total,
            facecolor="none",
            edgecolor="black",
            linewidth=1.5,
        )

    ax.set_yticks(y)
    ax.set_yticklabels(y_labels)

    ax.set_xlabel("Number of files")
    ax.set_ylabel("Entity + visual/auditory outcome")
    ax.set_title(f"Top {top_n} Label Groups + Others Across {total_files} Files")

    ax.legend(
        loc="upper right",
        bbox_to_anchor=(1, 0.85),
    )

    ax.invert_yaxis()
    fig.tight_layout()

    save_figure(fig, figures_dir / f"top_{top_n}_label_groups_with_others_outline.png")


def save_all_prediction_plots(
    preds: list[dict],
    figures_dir: Path,
    top_n: int,
) -> None:
    plot_label_group_counts(preds, figures_dir)
    plot_label_combination_distribution(preds, figures_dir)

    plot_data = build_plot_data(preds)

    plot_full_stacked_distribution(
        plot_data=plot_data,
        total_files=len(preds),
        figures_dir=figures_dir,
    )

    plot_top_label_groups_with_others(
        plot_data=plot_data,
        total_files=len(preds),
        figures_dir=figures_dir,
        top_n=top_n,
    )

    plot_top_label_groups_with_others_outline(
        plot_data=plot_data,
        total_files=len(preds),
        figures_dir=figures_dir,
        top_n=top_n,
    )


# =========================
# MANUAL COMPARISON
# =========================

def compare_with_manual_labels(
    preds: list[dict],
    manual_path: Path,
    experiment_dir: Path,
    figures_dir: Path,
) -> None:
    if not manual_path.exists():
        print(f"Manual labels file not found, skipping manual comparison: {manual_path}")
        return

    manual_data = read_json(manual_path)

    preds_by_path = {
        normalize_path(item["file_path"]): item
        for item in preds
    }

    manual_by_path = {
        normalize_path(item["file_path"]): item
        for item in manual_data
        if "manual_labels" in item
    }

    rows = []
    label_groups = ["entities", "interaction", "outcome"]

    for file_path, manual_item in manual_by_path.items():
        pred_item = preds_by_path.get(file_path)

        if pred_item is None:
            continue

        manual_labels = manual_item["manual_labels"]
        predicted_labels = pred_item["predicted_labels"]

        missing_count = 0
        extra_count = 0

        missing_labels = []
        extra_labels = []

        for group in label_groups:
            manual_set = set(ensure_list(manual_labels.get(group, [])))
            predicted_set = set(ensure_list(predicted_labels.get(group, [])))

            missing = manual_set - predicted_set
            extra = predicted_set - manual_set

            missing_count += len(missing)
            extra_count += len(extra)

            missing_labels.extend([f"{group}: {label}" for label in sorted(missing)])
            extra_labels.extend([f"{group}: {label}" for label in sorted(extra)])

        rows.append({
            "file_path": file_path,
            "missing_errors": missing_count,
            "extra_errors": extra_count,
            "total_errors": missing_count + extra_count,
            "missing_labels": missing_labels,
            "extra_labels": extra_labels,
        })

    errors_df = pd.DataFrame(rows)

    if not errors_df.empty:
        write_json(
            experiment_dir / "manual_prediction_errors.json",
            errors_df.to_dict(orient="records"),
        )

        errors_plot = (
            errors_df
            .sort_values("total_errors", ascending=False)
            .set_index("file_path")[["missing_errors", "extra_errors"]]
        )

        ax = errors_plot.plot(
            kind="barh",
            stacked=True,
            figsize=(12, max(5, len(errors_plot) * 0.35)),
        )

        fig = ax.get_figure()
        ax.set_xlabel("Number of errors")
        ax.set_ylabel("File path")
        ax.set_title(f"Prediction Errors Across {len(errors_df)} Manual Files")
        fig.tight_layout()

        save_figure(fig, figures_dir / "manual_prediction_errors_stacked.png")

        fig, ax = plt.subplots(figsize=(8, 5))

        ax.hist(
            errors_df["total_errors"],
            bins=range(errors_df["total_errors"].max() + 2),
            align="left",
            edgecolor="black",
        )

        ax.set_xlabel("Number of errors per file")
        ax.set_ylabel("Number of files")
        ax.set_title(f"Histogram of Prediction Errors Across {len(errors_df)} Files")
        ax.set_xticks(range(errors_df["total_errors"].max() + 1))

        fig.tight_layout()

        save_figure(fig, figures_dir / "manual_prediction_errors_histogram.png")

    manual_paths = {
        normalize_path(item["file_path"])
        for item in manual_data
        if "manual_labels" in item
    }

    pred_paths = {
        normalize_path(item["file_path"])
        for item in preds
    }

    missing_in_preds = sorted(manual_paths - pred_paths)

    without_manual_labels = [
        normalize_path(item["file_path"])
        for item in manual_data
        if "manual_labels" not in item
    ]

    (experiment_dir / "manual_files_not_found_in_preds.txt").write_text(
        "\n".join(missing_in_preds) + ("\n" if missing_in_preds else ""),
        encoding="utf-8",
    )

    (experiment_dir / "manual_files_without_labels.txt").write_text(
        "\n".join(without_manual_labels) + ("\n" if without_manual_labels else ""),
        encoding="utf-8",
    )

    print("Manual files not found in preds:", len(missing_in_preds))
    print("Files without manual_labels:", len(without_manual_labels))


# =========================
# MAIN
# =========================

PROMPT_VERSION = "PROMPT_10f"
RUN_DATE = time.strftime("%Y%m%d")

DATA_DIR = resolve_path("data")
OUTPUT_ROOT_DIR = resolve_path("artworks")

EXPERIMENT_DIR = OUTPUT_ROOT_DIR / f"{PROMPT_VERSION}_{RUN_DATE}"
PREDICTIONS_FILE = EXPERIMENT_DIR / "predictions.json"
FIGURES_DIR = EXPERIMENT_DIR / "figures"
MANUAL_PATH = DATA_DIR / "manual-sampling-25-artworks.json"

TOP_N = 25


def main():
    if not PREDICTIONS_FILE.exists():
        raise FileNotFoundError(
            f"Predictions file not found: {PREDICTIONS_FILE}"
        )

    print(f"Experiment folder: {EXPERIMENT_DIR}")
    print(f"Predictions file: {PREDICTIONS_FILE}")
    print(f"Data folder: {DATA_DIR}")
    print(f"Figures folder: {FIGURES_DIR}")

    files_to_rm = load_files_to_remove(DATA_DIR)
    raw_preds = load_predictions(PREDICTIONS_FILE)

    preds = clean_predictions(
        raw_preds=raw_preds,
        files_to_rm=files_to_rm,
    )

    add_label_combination(preds)

    save_processed_json_outputs(
        preds=preds,
        experiment_dir=EXPERIMENT_DIR,
    )

    save_all_prediction_plots(
        preds=preds,
        figures_dir=FIGURES_DIR,
        top_n=TOP_N,
    )

    compare_with_manual_labels(
        preds=preds,
        manual_path=MANUAL_PATH,
        experiment_dir=EXPERIMENT_DIR,
        figures_dir=FIGURES_DIR,
    )

    print("\nDone.")
    print(f"Raw predictions: {len(raw_preds)}")
    print(f"Removed files: {len(raw_preds) - len(preds)}")
    print(f"Clean predictions: {len(preds)}")
    print(f"JSON outputs saved in: {EXPERIMENT_DIR}")
    print(f"PNG figures saved in: {FIGURES_DIR}")


if __name__ == "__main__":
    main()
