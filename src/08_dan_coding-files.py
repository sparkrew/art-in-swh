import json
from pathlib import Path


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

OUTPUT_PATH = PROMPT_DIR / "files_split_coding_train_or_dan_shiffman.json"

EXCLUDE_TERMS = [
    "Coding Train",
    "Daniel Shiffman",
]


# =========================
# HELPERS
# =========================

def read_json(file_path: Path):
    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(data, file_path: Path):
    file_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def normalize_path(path: str) -> str:
    """
    Convert absolute artwork paths to paths relative to SRC_ROOT_DIR.
    """
    path = str(path)

    marker = "/artworks/src/"
    if marker in path:
        return path.split(marker, 1)[-1].lstrip("/")

    return path.lstrip("/")


def source_code_contains_excluded_term(relative_file_path: str) -> bool:
    src_path = SRC_ROOT_DIR / relative_file_path

    if not src_path.exists():
        return False

    code = src_path.read_text(encoding="utf-8", errors="ignore")
    code_lower = code.lower()

    return any(term.lower() in code_lower for term in EXCLUDE_TERMS)


# =========================
# MAIN
# =========================

def main():
    data = read_json(CLEAN_JSON_PATH)

    files_with_coding_train_or_dan_shiffman = []
    others = []
    missing_source_files = []

    for item in data:
        relative_file_path = normalize_path(item["file_path"])
        src_path = SRC_ROOT_DIR / relative_file_path

        if not src_path.exists():
            missing_source_files.append(relative_file_path)
            others.append(relative_file_path)
            continue

        if source_code_contains_excluded_term(relative_file_path):
            files_with_coding_train_or_dan_shiffman.append(relative_file_path)
        else:
            others.append(relative_file_path)

    output = {
        "files_with_coding_train_or_dan_shiffman": sorted(
            files_with_coding_train_or_dan_shiffman
        ),
        "others": sorted(others),
    }

    write_json(output, OUTPUT_PATH)

    print(f"Saved: {OUTPUT_PATH}")
    print(f"files_with_coding_train_or_dan_shiffman: {len(files_with_coding_train_or_dan_shiffman)}")
    print(f"others: {len(others)}")
    print(f"missing_source_files added to others: {len(missing_source_files)}")


if __name__ == "__main__":
    main()