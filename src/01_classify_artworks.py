import json
import os
import re
import time
from pathlib import Path

import yaml
from tqdm import tqdm
from Model import LLM_Model
from Prompts import *


# =========================
# CONFIG
# =========================

# Root folder with all repositories / src files
ROOT_DIR = Path("/home/rpinter/links/projects/def-baudry/shared/data/artworks/src")

# Same style as your notebook
CONFIG_PATH = Path("../config.yml")
PROMPT_VERSION = "PROMPT_10a"

# Folder where output files will be saved
OUTPUT_ROOT_DIR = Path("../artworks/")

RUN_TIMESTAMP = time.strftime("%Y%m%d")
EXPERIMENT_NAME = f"{PROMPT_VERSION}_{RUN_TIMESTAMP}"

OUTPUT_DIR = OUTPUT_ROOT_DIR / EXPERIMENT_NAME
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Output files
PREDICTIONS_FILE = OUTPUT_DIR / "predictions.json"
SUCCESS_FILE = OUTPUT_DIR / "successes.txt"
ERROR_FILE = OUTPUT_DIR / "errors.txt"

# Number of new files to process in this run.
# Use an integer like 10 to test with a subset.
# Use None to process everything.
MAX_FILES_TO_RUN = None

# Hardcoded total number of files available
TOTAL_FILES_AVAILABLE = 19798

# If True, print percentages using the hardcoded total above
COMPUTE_PERCENTAGES = True


# =========================
# HELPERS
# =========================

def get_prompt_template(prompt_version: str) -> str:
    """Get the prompt template from Prompts.py."""
    return globals()[prompt_version].template


def append_line(file_path: Path, line: str) -> None:
    """
    Append one line to a txt file immediately.
    This avoids losing success/error info if the job fails.
    """
    with file_path.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
        f.flush()
        os.fsync(f.fileno())


def atomic_write_json(file_path: Path, data) -> None:
    """
    Write JSON atomically to reduce the chance of corrupting the file
    if the job dies during a write.
    """
    tmp_path = file_path.with_suffix(file_path.suffix + ".tmp")
    with tmp_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, file_path)


def load_json_file(file_path: Path):
    """Load a JSON file if it exists, otherwise return an empty list."""
    if not file_path.exists():
        return []

    try:
        with file_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def load_success_paths() -> set[str]:
    """
    Read successes.txt at the start so we skip files already processed
    in previous executions.
    """
    if not SUCCESS_FILE.exists():
        return set()

    with SUCCESS_FILE.open("r", encoding="utf-8") as f:
        return {line.strip() for line in f if line.strip()}


def append_prediction(file_path: str, predicted_labels: dict) -> None:
    """
    Append one prediction entry to predictions.json.
    We rewrite the JSON file every time so the result is always saved.
    """
    predictions = load_json_file(PREDICTIONS_FILE)

    # Extra safeguard against duplicates
    already_exists = any(item.get("file_path") == file_path for item in predictions)
    if not already_exists:
        predictions.append({
            "file_path": file_path,
            "predicted_labels": predicted_labels
        })
        atomic_write_json(PREDICTIONS_FILE, predictions)


def try_parse_json(raw_output):
    """
    Try to turn the LLM output into valid JSON.

    Accepts:
    - dict directly
    - JSON string
    - JSON wrapped in ```json ... ```
    - text with extra content around the JSON object
    """
    if isinstance(raw_output, dict):
        return raw_output

    if not isinstance(raw_output, str):
        return None

    text = raw_output.strip()

    # Remove markdown code fences if present
    text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    # First try: parse as-is
    try:
        return json.loads(text)
    except Exception:
        pass

    # Second try: extract the first JSON object from the text
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = text[start:end + 1]
        try:
            return json.loads(candidate)
        except Exception:
            pass

    return None


def normalize_prediction(predicted_labels: dict) -> dict:
    """
    Keep the small normalization you already had in the notebook.
    """
    if isinstance(predicted_labels.get("interaction"), str):
        predicted_labels["interaction"] = [predicted_labels["interaction"]]
    return predicted_labels


def predict_with_retries(llm_model, prompt: str, art_src_code: str, max_attempts: int = 3):
    """
    Call the LLM and validate JSON.
    Try up to 3 total attempts:
    - first try
    - 2 retries if JSON is invalid
    - if the API itself fails, return None so the caller adds the file to errors.txt
    """
    for _ in range(max_attempts):
        try:
            raw_output = llm_model.get_labels(
                prompt_template=prompt,
                art_src_code=art_src_code,
                system_prompt=llm_model.system_prompt
            )
        except Exception:
            return None

        parsed_output = try_parse_json(raw_output)
        if isinstance(parsed_output, dict):
            return normalize_prediction(parsed_output)

    return None


def iter_source_files(root_dir: Path):
    """
    Yield every file inside the root directory, recursively.
    Uses os.walk for better performance on large trees.
    """
    for root, _, files in os.walk(root_dir):
        for name in files:
            yield Path(root) / name


def iter_pending_files(root_dir: Path, success_paths: set[str]):
    """
    Yield only files that are not already in successes.txt.
    """
    for path in iter_source_files(root_dir):
        path_str = str(path)
        if path_str not in success_paths:
            yield path


def collect_limited_pending_files(root_dir: Path, success_paths: set[str], max_files_to_run: int):
    """
    Collect only the first N pending files.
    This avoids scanning the full tree when you're just testing with a small number.
    """
    files_to_process = []

    for path in iter_pending_files(root_dir, success_paths):
        files_to_process.append(path)
        if len(files_to_process) >= max_files_to_run:
            break

    return files_to_process


def format_seconds(seconds: float) -> str:
    """Format seconds in a simple human-readable way."""
    if seconds < 60:
        return f"{seconds:.2f}s"

    minutes, sec = divmod(seconds, 60)
    if minutes < 60:
        return f"{int(minutes)}m {sec:.2f}s"

    hours, minutes = divmod(minutes, 60)
    return f"{int(hours)}h {int(minutes)}m {sec:.2f}s"


# =========================
# MAIN
# =========================

def main():
    run_start_time = time.perf_counter()
    
    # Read config exactly like your notebook style
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        configs = yaml.safe_load(f)

    model_key = configs["chosen_config"]["model"]

    llm_model = LLM_Model(
        model_name=configs[model_key]["model_name"],
        base_url=configs[model_key]["base_url"],
        system_prompt=configs[model_key]["system_prompt"]
    )

    prompt = get_prompt_template(PROMPT_VERSION)

    # Read already successful files so reruns skip them
    success_paths = load_success_paths()
    classified_before_run = len(success_paths)

    # Build only what is needed for this run
    if MAX_FILES_TO_RUN is None:
        files_to_process = iter_pending_files(ROOT_DIR, success_paths)
        progress_bar = tqdm(
            files_to_process,
            desc="Classifying files",
            unit="file",
            dynamic_ncols=True,
        )
    else:
        files_to_process = collect_limited_pending_files(ROOT_DIR, success_paths, MAX_FILES_TO_RUN)
        progress_bar = tqdm(
            files_to_process,
            total=len(files_to_process),
            desc="Classifying files",
            unit="file",
            dynamic_ncols=True,
        )

    processed_this_run = 0
    total_success = 0
    total_error = 0

    for file_path in progress_bar:
        file_path_str = str(file_path)

        # Read source code
        try:
            art_src_code = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            append_line(ERROR_FILE, file_path_str)
            total_error += 1
            processed_this_run += 1
            progress_bar.set_postfix(success=total_success, errors=total_error)
            continue

        # Skip empty files
        if not art_src_code.strip():
            append_line(ERROR_FILE, file_path_str)
            total_error += 1
            processed_this_run += 1
            progress_bar.set_postfix(success=total_success, errors=total_error)
            continue

        # Predict and validate JSON
        predicted_labels = predict_with_retries(
            llm_model=llm_model,
            prompt=prompt,
            art_src_code=art_src_code,
            max_attempts=3
        )

        # If still invalid after retries, store the path in errors.txt
        if predicted_labels is None:
            append_line(ERROR_FILE, file_path_str)
            total_error += 1
            processed_this_run += 1
            progress_bar.set_postfix(success=total_success, errors=total_error)
            continue

        # Save prediction immediately
        relative_file_path = str(file_path.relative_to(ROOT_DIR))
        append_prediction(relative_file_path, predicted_labels)

        # Mark as success immediately
        append_line(SUCCESS_FILE, file_path_str)
        success_paths.add(file_path_str)

        total_success += 1
        processed_this_run += 1
        progress_bar.set_postfix(success=total_success, errors=total_error)

    total_classified_overall = len(success_paths)

    total_elapsed_seconds = time.perf_counter() - run_start_time
    avg_time_per_processed_script = (
        total_elapsed_seconds / processed_this_run if processed_this_run > 0 else 0
    )

    print("\nDone.")
    print(f"Already classified before this run: {classified_before_run}")
    print(f"Processed in this run: {processed_this_run}")
    print(f"Successfully classified in this run: {total_success}")
    print(f"Errors in this run: {total_error}")
    print(f"Total classified overall: {total_classified_overall}")
    print(f"Total runtime: {format_seconds(total_elapsed_seconds)}")
    print(f"Average time per processed script: {format_seconds(avg_time_per_processed_script)}")

    if COMPUTE_PERCENTAGES:
        overall_percentage = (
            total_classified_overall / TOTAL_FILES_AVAILABLE * 100
            if TOTAL_FILES_AVAILABLE > 0 else 0
        )
        run_percentage = (
            total_success / TOTAL_FILES_AVAILABLE * 100
            if TOTAL_FILES_AVAILABLE > 0 else 0
        )

        print(f"Total files available: {TOTAL_FILES_AVAILABLE}")
        print(f"Percentage classified overall: {overall_percentage:.2f}%")
        print(f"Percentage classified in this run: {run_percentage:.2f}%")


if __name__ == "__main__":
    main()