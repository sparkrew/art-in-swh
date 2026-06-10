import json
import random
from pathlib import Path


# =========================
# CONFIG
# =========================

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

PROMPT_VERSION = "PROMPT_10f"
RUN_DATE = "20260603"

EXPERIMENT_DIR = PROJECT_ROOT / "artworks" / f"{PROMPT_VERSION}_{RUN_DATE}"

SRC_ROOT_DIR = Path(
    "/home/rpinter/links/projects/def-baudry/shared/data/artworks/src"
)

OUTPUT_DIR = EXPERIMENT_DIR / "src_code_samples"

N_SAMPLES = 10
RANDOM_SEED = 42

JSON_FILES = [
    "clean_artworks_label_prediction_no_entities.json",
    "clean_artworks_label_prediction_interactive_static.json",
    "clean_artworks_label_prediction_no_intrand_visual_static.json",
    "clean_artworks_label_prediction_top9.json",
]


# =========================
# HELPERS
# =========================

def read_json(file_path: Path):
    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def normalize_path(path: str) -> str:
    """
    Convert absolute artwork paths to paths relative to SRC_ROOT_DIR.
    """
    path = str(path)

    marker = "/artworks/src/"
    if marker in path:
        return path.split(marker, 1)[-1].lstrip("/")

    return path.lstrip("/")


def format_labels(item: dict) -> str:
    predicted_labels = item.get("predicted_labels", {})

    return json.dumps(
        predicted_labels,
        indent=2,
        ensure_ascii=False,
    )


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


def write_sample_notebook(json_name: str, sampled_items: list[dict]) -> None:
    output_path = OUTPUT_DIR / f"{Path(json_name).stem}_10_random_src.ipynb"

    cells = []

    setup_cell = f"""
from pathlib import Path
from IPython.display import Markdown, display

SRC_ROOT_DIR = Path({str(SRC_ROOT_DIR)!r})

def print_code_file(relative_file_path, language="javascript"):
    file_path = SRC_ROOT_DIR / relative_file_path
    code = file_path.read_text(encoding="utf-8", errors="ignore")

    display(Markdown(f"```{{language}}\\n{{code}}\\n```"))
""".strip()

    cells.append(make_code_cell(setup_cell))

    cells.append(
        make_markdown_cell(
            f"# Source code samples\n\n"
            f"JSON file: `{json_name}`\n\n"
            f"Prompt version: `{PROMPT_VERSION}`\n\n"
            f"Run date: `{RUN_DATE}`"
        )
    )

    for i, item in enumerate(sampled_items, start=1):
        relative_file_path = normalize_path(item["file_path"])
        label_combination = item.get("label_combination", "")
        labels_text = format_labels(item)

        cells.append(
            make_markdown_cell(
                f"## Sample {i}\n\n"
                f"**File path:**\n\n"
                f"`{relative_file_path}`\n\n"
                f"**Label combination:**\n\n"
                f"`{label_combination}`\n\n"
                f"**Complete labels:**\n\n"
                f"```json\n{labels_text}\n```"
            )
        )

        cells.append(
            make_code_cell(
                f"print_code_file({relative_file_path!r})"
            )
        )

        cells.append(
            make_markdown_cell(
                f"### Notes for Sample {i}\n\n"
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

    print(f"Saved: {output_path}")


# =========================
# MAIN
# =========================

def main():
    random.seed(RANDOM_SEED)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Experiment folder: {EXPERIMENT_DIR}")
    print(f"Source root folder: {SRC_ROOT_DIR}")
    print(f"Output folder: {OUTPUT_DIR}")
    print()

    for json_name in JSON_FILES:
        json_path = EXPERIMENT_DIR / json_name

        if not json_path.exists():
            print(f"Skipping, file not found: {json_path}")
            continue

        data = read_json(json_path)

        if not data:
            print(f"Skipping, empty JSON: {json_path}")
            continue

        sample_size = min(N_SAMPLES, len(data))
        sampled_items = random.sample(data, sample_size)

        write_sample_notebook(
            json_name=json_name,
            sampled_items=sampled_items,
        )

    print("\nDone.")


if __name__ == "__main__":
    main()