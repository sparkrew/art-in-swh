import asyncio
import json
import os
import re
import time
from pathlib import Path

import yaml
from openai import AsyncOpenAI
from tqdm import tqdm

from Prompts import *


# =========================
# CONFIG
# =========================

ROOT_DIR = Path("/home/rpinter/links/projects/def-baudry/shared/data/artworks/src")

CONFIG_PATH = Path("../config.yml")
PROMPT_VERSION = "PROMPT_10a"

OUTPUT_ROOT_DIR = Path("../artworks/")

RUN_TIMESTAMP = time.strftime("%Y%m%d")
EXPERIMENT_NAME = f"{PROMPT_VERSION}_{RUN_TIMESTAMP}"

OUTPUT_DIR = OUTPUT_ROOT_DIR / EXPERIMENT_NAME
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PARTS_DIR = OUTPUT_DIR / "prediction_parts"
PARTS_DIR.mkdir(parents=True, exist_ok=True)

FINAL_PREDICTIONS_FILE = OUTPUT_DIR / "predictions.json"
SUCCESS_FILE = OUTPUT_DIR / "successes.txt"
ERROR_FILE = OUTPUT_DIR / "errors.jsonl"

MAX_FILES_TO_RUN = None

# Start with 16. Then try 32.
CONCURRENCY = 16

# Keep this not too high while testing.
MAX_COMPLETION_TOKENS = 512

# Write/flush progress every N completed files.
FLUSH_EVERY = 50

TOTAL_FILES_AVAILABLE = 19798
COMPUTE_PERCENTAGES = True


# =========================
# HELPERS
# =========================

def get_prompt_template(prompt_version: str) -> str:
    return globals()[prompt_version].template


def load_success_paths() -> set[str]:
    if not SUCCESS_FILE.exists():
        return set()

    with SUCCESS_FILE.open("r", encoding="utf-8") as f:
        return {line.strip() for line in f if line.strip()}


def iter_source_files(root_dir: Path):
    for root, _, files in os.walk(root_dir):
        for name in files:
            yield Path(root) / name


def iter_pending_files(root_dir: Path, success_paths: set[str]):
    for path in iter_source_files(root_dir):
        path_str = str(path)

        if path_str not in success_paths:
            yield path


def collect_limited_pending_files(root_dir: Path, success_paths: set[str], max_files_to_run: int):
    selected = []

    for path in iter_pending_files(root_dir, success_paths):
        selected.append(path)

        if len(selected) >= max_files_to_run:
            break

    return selected


def try_parse_json(raw_output):
    if isinstance(raw_output, dict):
        return raw_output

    if not isinstance(raw_output, str):
        return None

    text = raw_output.strip()

    text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    try:
        return json.loads(text)
    except Exception:
        pass

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
    if isinstance(predicted_labels.get("interaction"), str):
        predicted_labels["interaction"] = [predicted_labels["interaction"]]

    return predicted_labels


def render_prompt(prompt_template: str, art_src_code: str) -> str:
    """
    Avoid .format(), because your prompt probably contains JSON examples with braces.

    This only replaces common source-code placeholders.
    If none are found, it appends the source code at the end.
    """
    replacements = {
        "{art_src_code}": art_src_code,
        "{{art_src_code}}": art_src_code,
        "{src_code}": art_src_code,
        "{{src_code}}": art_src_code,
        "{source_code}": art_src_code,
        "{{source_code}}": art_src_code,
        "{code}": art_src_code,
        "{{code}}": art_src_code,
    }

    rendered = prompt_template

    for placeholder, value in replacements.items():
        if placeholder in rendered:
            rendered = rendered.replace(placeholder, value)
            return rendered

    return (
        rendered
        + "\n\nSource code to classify:\n"
        + "```javascript\n"
        + art_src_code
        + "\n```"
    )


def append_jsonl_line(file_handle, item: dict) -> None:
    file_handle.write(json.dumps(item, ensure_ascii=False) + "\n")


def flush_and_fsync(file_handle) -> None:
    file_handle.flush()
    os.fsync(file_handle.fileno())


def atomic_write_json(file_path: Path, data) -> None:
    tmp_path = file_path.with_suffix(file_path.suffix + ".tmp")

    with tmp_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        flush_and_fsync(f)

    os.replace(tmp_path, file_path)


def format_seconds(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:.2f}s"

    minutes, sec = divmod(seconds, 60)

    if minutes < 60:
        return f"{int(minutes)}m {sec:.2f}s"

    hours, minutes = divmod(minutes, 60)
    return f"{int(hours)}h {int(minutes)}m {sec:.2f}s"


async def read_text_async(path: Path) -> str:
    return await asyncio.to_thread(
        path.read_text,
        encoding="utf-8",
        errors="ignore"
    )


async def classify_one_file(
    client: AsyncOpenAI,
    model_name: str,
    system_prompt: str,
    prompt_template: str,
    file_path: Path,
    max_attempts: int = 3,
):
    file_path_str = str(file_path)

    try:
        art_src_code = await read_text_async(file_path)
    except Exception as e:
        return {
            "status": "error",
            "file_path": file_path_str,
            "error": f"read_error: {e}"
        }

    if not art_src_code.strip():
        return {
            "status": "error",
            "file_path": file_path_str,
            "error": "empty_file"
        }

    user_prompt = render_prompt(prompt_template, art_src_code)

    for attempt in range(1, max_attempts + 1):
        try:
            response = await client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=MAX_COMPLETION_TOKENS,
                temperature=0,
            )

            raw_output = response.choices[0].message.content
            parsed_output = try_parse_json(raw_output)

            if isinstance(parsed_output, dict):
                return {
                    "status": "success",
                    "file_path": file_path_str,
                    "relative_file_path": str(file_path.relative_to(ROOT_DIR)),
                    "predicted_labels": normalize_prediction(parsed_output)
                }

        except Exception as e:
            last_error = str(e)

            # Small backoff so temporary overload does not destroy the run.
            await asyncio.sleep(min(2 * attempt, 10))

    return {
        "status": "error",
        "file_path": file_path_str,
        "error": f"prediction_failed_or_invalid_json: {locals().get('last_error', '')}"
    }


async def worker(
    worker_id: int,
    queue: asyncio.Queue,
    result_queue: asyncio.Queue,
    client: AsyncOpenAI,
    model_name: str,
    system_prompt: str,
    prompt_template: str,
):
    while True:
        file_path = await queue.get()

        if file_path is None:
            queue.task_done()
            break

        result = await classify_one_file(
            client=client,
            model_name=model_name,
            system_prompt=system_prompt,
            prompt_template=prompt_template,
            file_path=file_path,
        )

        await result_queue.put(result)
        queue.task_done()


async def write_results(
    result_queue: asyncio.Queue,
    total_files: int,
    success_paths: set[str],
):
    part_path = PARTS_DIR / f"predictions_part_{time.strftime('%Y%m%d_%H%M%S')}.jsonl"

    processed_this_run = 0
    total_success = 0
    total_error = 0

    with (
        part_path.open("a", encoding="utf-8") as pred_f,
        SUCCESS_FILE.open("a", encoding="utf-8") as success_f,
        ERROR_FILE.open("a", encoding="utf-8") as error_f,
    ):
        progress_bar = tqdm(
            total=total_files,
            desc="Classifying files",
            unit="file",
            dynamic_ncols=True,
        )

        while processed_this_run < total_files:
            result = await result_queue.get()
            processed_this_run += 1

            if result["status"] == "success":
                prediction_item = {
                    "file_path": result["relative_file_path"],
                    "predicted_labels": result["predicted_labels"]
                }

                append_jsonl_line(pred_f, prediction_item)

                # Store absolute path for rerun skipping.
                success_f.write(result["file_path"] + "\n")
                success_paths.add(result["file_path"])

                total_success += 1

            else:
                error_item = {
                    "file_path": result["file_path"],
                    "error": result["error"]
                }

                append_jsonl_line(error_f, error_item)
                total_error += 1

            if processed_this_run % FLUSH_EVERY == 0:
                flush_and_fsync(pred_f)
                flush_and_fsync(success_f)
                flush_and_fsync(error_f)

            progress_bar.update(1)
            progress_bar.set_postfix(
                success=total_success,
                errors=total_error
            )

            result_queue.task_done()

        flush_and_fsync(pred_f)
        flush_and_fsync(success_f)
        flush_and_fsync(error_f)

        progress_bar.close()

    return {
        "processed_this_run": processed_this_run,
        "total_success": total_success,
        "total_error": total_error,
        "part_path": str(part_path),
    }


def build_final_predictions_json() -> int:
    """
    Merge all prediction_parts/*.jsonl files into predictions.json.

    Deduplicates by file_path.
    """
    predictions_by_path = {}

    for part_file in sorted(PARTS_DIR.glob("predictions_part_*.jsonl")):
        with part_file.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                if not line:
                    continue

                try:
                    item = json.loads(line)
                except Exception:
                    continue

                file_path = item.get("file_path")
                predicted_labels = item.get("predicted_labels")

                if file_path and predicted_labels is not None:
                    predictions_by_path[file_path] = {
                        "file_path": file_path,
                        "predicted_labels": predicted_labels
                    }

    final_predictions = list(predictions_by_path.values())
    atomic_write_json(FINAL_PREDICTIONS_FILE, final_predictions)

    return len(final_predictions)


async def async_main():
    run_start_time = time.perf_counter()

    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        configs = yaml.safe_load(f)

    model_key = configs["chosen_config"]["model"]

    model_name = configs[model_key]["model_name"]
    base_url = configs[model_key]["base_url"]
    system_prompt = configs[model_key]["system_prompt"]

    prompt_template = get_prompt_template(PROMPT_VERSION)

    success_paths = load_success_paths()
    classified_before_run = len(success_paths)

    if MAX_FILES_TO_RUN is None:
        files_to_process = list(iter_pending_files(ROOT_DIR, success_paths))
    else:
        files_to_process = collect_limited_pending_files(
            ROOT_DIR,
            success_paths,
            MAX_FILES_TO_RUN
        )

    print(f"Model: {model_name}")
    print(f"Base URL: {base_url}")
    print(f"Pending files selected for this run: {len(files_to_process)}")
    print(f"Already classified before this run: {classified_before_run}")
    print(f"Concurrency: {CONCURRENCY}")
    print(f"Output directory: {OUTPUT_DIR}")

    if not files_to_process:
        print("No pending files to process.")
        final_count = build_final_predictions_json()
        print(f"Final predictions.json entries: {final_count}")
        return

    client = AsyncOpenAI(
        base_url=base_url,
        api_key="EMPTY",
        timeout=120,
    )

    queue = asyncio.Queue()
    result_queue = asyncio.Queue()

    for file_path in files_to_process:
        await queue.put(file_path)

    workers = [
        asyncio.create_task(
            worker(
                worker_id=i,
                queue=queue,
                result_queue=result_queue,
                client=client,
                model_name=model_name,
                system_prompt=system_prompt,
                prompt_template=prompt_template,
            )
        )
        for i in range(CONCURRENCY)
    ]

    writer_task = asyncio.create_task(
        write_results(
            result_queue=result_queue,
            total_files=len(files_to_process),
            success_paths=success_paths,
        )
    )

    for _ in workers:
        await queue.put(None)

    await queue.join()
    await asyncio.gather(*workers)

    run_stats = await writer_task

    print("\nBuilding final predictions.json...")
    final_prediction_count = build_final_predictions_json()

    total_elapsed_seconds = time.perf_counter() - run_start_time

    processed_this_run = run_stats["processed_this_run"]
    total_success = run_stats["total_success"]
    total_error = run_stats["total_error"]

    avg_time_per_processed_script = (
        total_elapsed_seconds / processed_this_run
        if processed_this_run > 0
        else 0
    )

    total_classified_overall = len(success_paths)

    print("\nDone.")
    print(f"Partial predictions file: {run_stats['part_path']}")
    print(f"Already classified before this run: {classified_before_run}")
    print(f"Processed in this run: {processed_this_run}")
    print(f"Successfully classified in this run: {total_success}")
    print(f"Errors in this run: {total_error}")
    print(f"Total classified overall according to successes.txt: {total_classified_overall}")
    print(f"Final predictions.json entries: {final_prediction_count}")
    print(f"Final predictions file: {FINAL_PREDICTIONS_FILE}")
    print(f"Total runtime: {format_seconds(total_elapsed_seconds)}")
    print(f"Average time per processed script: {format_seconds(avg_time_per_processed_script)}")

    if COMPUTE_PERCENTAGES:
        overall_percentage = (
            total_classified_overall / TOTAL_FILES_AVAILABLE * 100
            if TOTAL_FILES_AVAILABLE > 0
            else 0
        )

        run_percentage = (
            total_success / TOTAL_FILES_AVAILABLE * 100
            if TOTAL_FILES_AVAILABLE > 0
            else 0
        )

        print(f"Total files available: {TOTAL_FILES_AVAILABLE}")
        print(f"Percentage classified overall: {overall_percentage:.2f}%")
        print(f"Percentage classified in this run: {run_percentage:.2f}%")


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()