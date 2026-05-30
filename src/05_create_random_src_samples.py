import json
import random
import time
from pathlib import Path


# =========================
# CONFIG
# =========================

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

PROMPT_VERSION = "PROMPT_10a"
RUN_DATE = "20260528"

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


def read_src_code(relative_file_path: str) -> str:
    src_file_path = SRC_ROOT_DIR / relative_file_path

    if not src_file_path.exists():
        return f"[ERROR] Source file not found: {src_file_path}"

    try:
        return src_file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return f"[ERROR] Could not read source file: {src_file_path}\n{e}"


def format_labels(item: dict) -> str:
    predicted_labels = item.get("predicted_labels", {})

    return json.dumps(
        predicted_labels,
        indent=2,
        ensure_ascii=False,
    )


def write_sample_txt(json_name: str, sampled_items: list[dict]) -> None:
    output_path = OUTPUT_DIR / f"{Path(json_name).stem}_10_random_src.txt"

    blocks = []

    for i, item in enumerate(sampled_items, start=1):
        relative_file_path = normalize_path(item["file_path"])
        label_combination = item.get("label_combination", "")
        labels_text = format_labels(item)
        src_code = read_src_code(relative_file_path)

        block = f"""
================================================================================
SAMPLE {i}
FILE PATH:
{relative_file_path}

LABEL COMBINATION:
{label_combination}

COMPLETE LABELS:
{labels_text}
================================================================================

SOURCE CODE:
{src_code}
"""
        blocks.append(block)

    output_path.write_text("\n\n".join(blocks), encoding="utf-8")

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

        write_sample_txt(
            json_name=json_name,
            sampled_items=sampled_items,
        )

    print("\nDone.")


if __name__ == "__main__":
    main()