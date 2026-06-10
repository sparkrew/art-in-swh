import json
import random
import re
from collections import Counter
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

OUTPUT_DIR = PROMPT_DIR / "paper_combination_samples_exact_labels"

NOTEBOOK_DIR = OUTPUT_DIR / "notebooks"

N_SAMPLES = 30
RANDOM_SEED = 1

SOURCE_CODE_EXCLUDE_TERMS = [
    "Coding Train",
    "Daniel Shiffman",
]

PATH_EXCLUDE_TERMS = [
    "Tutorials",
    "Coursera",
    "CodingChallenges",
    "Rainbow-Code",
    "Courses",
    "p5.js",
    "week",
]

RARE_ENTITY_COMBO_MAX_COUNT = 10


# =========================
# REQUESTED COMBINATIONS
# =========================

REQUESTED_COMBINATIONS = [
    {
        "name": "entities_synthesized_image_randomness_non_interactive_any_outcome",
        "title": "Entities = synthesized_image + randomness, non-interactive, any outcome",
        "description": (
            "Entities must be exactly [synthesized_image, randomness]. "
            "Interaction must be no. Outcome can be anything."
        ),
        "entities_exact": ["synthesized_image", "randomness"],
        "interaction_exact": ["no"],
    },
    {
        "name": "entities_processed_image_synthesized_image_any_interaction_any_outcome",
        "title": "Entities = processed_image + synthesized_image, any interaction, any outcome",
        "description": (
            "Entities must be exactly [processed_image, synthesized_image]. "
            "Interaction and outcome can be anything."
        ),
        "entities_exact": ["processed_image", "synthesized_image"],
    },
    {
        "name": "static_image_no_interaction_no_sound_image_synth_exact",
        "title": "Static image, no interaction, no sound, image synth",
        "description": (
            "Exactly: static visual image, interaction = no, no sound, synthesized image. "
            "Entities can be synthesized_image alone, or synthesized_image with randomness, "
            "processed_image, or both."
        ),
        "special": "static_image_no_interaction_no_sound_image_synth",
    },
    {
        "name": "entities_processed_audio_synthesized_image_any_interaction_any_outcome",
        "title": "Entities = processed_audio + synthesized_image, any interaction, any outcome",
        "description": (
            "Entities must be exactly [processed_audio, synthesized_image]. "
            "Interaction and outcome can be anything."
        ),
        "entities_exact": ["processed_audio", "synthesized_image"],
    },
    {
        "name": "any_entity_any_interaction_only_auditory_time_based",
        "title": "Any entity, any interaction, only auditory, time-based outcome",
        "description": (
            "Entities can be anything. Interaction can be anything. "
            "Outcome must be exactly [auditory, time_based]."
        ),
        "outcome_exact": ["auditory", "time_based"],
    },
    {
        "name": "interactive_time_based_visual_any_entity",
        "title": "Interactive, time-based visual, any entity",
        "description": (
            "Entities can be anything. Interaction must be yes. "
            "Outcome must be exactly [visual, time_based]."
        ),
        "interaction_exact": ["yes"],
        "outcome_exact": ["visual", "time_based"],
    },
    {
        "name": "rare_entity_combinations",
        "title": "Rare combinations of entities",
        "description": (
            "Samples from entity combinations whose total count is less than or equal "
            f"to {RARE_ENTITY_COMBO_MAX_COUNT}."
        ),
        "special": "rare_entity_combinations",
    },
    {
        "name": "with_synthesized_text",
        "title": "With synthesized_text",
        "description": (
            "Entities must contain synthesized_text. "
            "Other entities, interaction, and outcome can be anything."
        ),
        "entities_contains": ["synthesized_text"],
    },
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


def normalize_path(path: str) -> str:
    """
    Convert absolute artwork paths to paths relative to SRC_ROOT_DIR.
    """
    path = str(path)

    marker = "/artworks/src/"
    if marker in path:
        return path.split(marker, 1)[-1].lstrip("/")

    return path.lstrip("/")


def slugify(text: str, max_length: int = 100) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = text.strip("_")

    if len(text) > max_length:
        text = text[:max_length].rstrip("_")

    return text or "sample"


def sorted_join(values):
    values = ensure_list(values)
    values = [str(x) for x in values if x is not None]

    return " + ".join(sorted(values))


# =========================
# LABEL HELPERS
# =========================

def labels_key(item: dict) -> dict:
    return item.get("predicted_labels", {})


def get_label_set(item: dict, field_name: str) -> set[str]:
    labels = labels_key(item)

    return set(ensure_list(labels.get(field_name, [])))


def get_entities(item: dict) -> set[str]:
    return get_label_set(item, "entities")


def get_interaction(item: dict) -> set[str]:
    return get_label_set(item, "interaction")


def get_outcome(item: dict) -> set[str]:
    return get_label_set(item, "outcome")


def all_characteristics_combo(labels: dict) -> str:
    entities = sorted_join(labels.get("entities", [])) or "none"
    interaction = sorted_join(labels.get("interaction", [])) or "none"
    outcome = sorted_join(labels.get("outcome", [])) or "none"

    return f"{entities} | interaction={interaction} | {outcome}"


def entities_combo(labels: dict) -> str:
    entities = sorted_join(labels.get("entities", [])) or "none"

    return entities


def get_entity_combo(item: dict) -> str:
    return entities_combo(labels_key(item))


# =========================
# SOURCE CODE + PATH FILTERING
# =========================

def read_source_code(item: dict) -> tuple[str | None, Path]:
    relative_file_path = normalize_path(item["file_path"])
    src_path = SRC_ROOT_DIR / relative_file_path

    if not src_path.exists():
        return None, src_path

    code = src_path.read_text(encoding="utf-8", errors="ignore")

    return code, src_path


def source_code_contains_excluded_term(code: str) -> bool:
    code_lower = code.lower()

    for term in SOURCE_CODE_EXCLUDE_TERMS:
        if term.lower() in code_lower:
            return True

    return False


def path_contains_excluded_term(relative_file_path: str) -> bool:
    path_lower = relative_file_path.lower()

    for term in PATH_EXCLUDE_TERMS:
        if term.lower() in path_lower:
            return True

    return False


def filter_items(data: list[dict]) -> tuple[list[dict], dict]:
    kept_items = []
    missing_source_files = []
    excluded_items_by_source_code = []
    excluded_items_by_path = []

    for item in data:
        relative_file_path = normalize_path(item["file_path"])

        if path_contains_excluded_term(relative_file_path):
            excluded_items_by_path.append(relative_file_path)
            continue

        code, src_path = read_source_code(item)

        if code is None:
            missing_source_files.append(relative_file_path)
            continue

        if source_code_contains_excluded_term(code):
            excluded_items_by_source_code.append(relative_file_path)
            continue

        kept_items.append(item)

    summary = {
        "total_items_before_filter": len(data),
        "total_items_after_filter": len(kept_items),
        "total_missing_source_files": len(missing_source_files),
        "total_excluded_by_source_code_terms": len(excluded_items_by_source_code),
        "total_excluded_by_path_terms": len(excluded_items_by_path),
        "source_code_exclude_terms": SOURCE_CODE_EXCLUDE_TERMS,
        "path_exclude_terms": PATH_EXCLUDE_TERMS,
        "missing_source_files": sorted(missing_source_files),
        "excluded_items_by_source_code_terms": sorted(excluded_items_by_source_code),
        "excluded_items_by_path_terms": sorted(excluded_items_by_path),
    }

    return kept_items, summary


# =========================
# MATCHING HELPERS
# =========================

def matches_exact(field_values: set[str], expected_values: list[str]) -> bool:
    return field_values == set(expected_values)


def contains_all(field_values: set[str], required_values: list[str]) -> bool:
    return set(required_values).issubset(field_values)


def matches_static_image_no_interaction_no_sound_image_synth(item: dict) -> bool:
    entities = get_entities(item)
    interaction = get_interaction(item)
    outcome = get_outcome(item)

    allowed_entity_sets = [
        {"synthesized_image"},
        {"synthesized_image", "randomness"},
        {"synthesized_image", "processed_image"},
        {"synthesized_image", "randomness", "processed_image"},
    ]

    return (
        entities in allowed_entity_sets
        and interaction == {"no"}
        and outcome == {"visual", "static"}
    )


def item_matches_request(item: dict, request: dict) -> bool:
    if request.get("special") == "static_image_no_interaction_no_sound_image_synth":
        return matches_static_image_no_interaction_no_sound_image_synth(item)

    if request.get("special") == "rare_entity_combinations":
        raise ValueError(
            "rare_entity_combinations should be handled separately."
        )

    entities = get_entities(item)
    interaction = get_interaction(item)
    outcome = get_outcome(item)

    if "entities_exact" in request:
        if not matches_exact(entities, request["entities_exact"]):
            return False

    if "interaction_exact" in request:
        if not matches_exact(interaction, request["interaction_exact"]):
            return False

    if "outcome_exact" in request:
        if not matches_exact(outcome, request["outcome_exact"]):
            return False

    if "entities_contains" in request:
        if not contains_all(entities, request["entities_contains"]):
            return False

    if "interaction_contains" in request:
        if not contains_all(interaction, request["interaction_contains"]):
            return False

    if "outcome_contains" in request:
        if not contains_all(outcome, request["outcome_contains"]):
            return False

    return True


def get_matching_items(data: list[dict], request: dict) -> list[dict]:
    return [
        item
        for item in data
        if item_matches_request(item, request)
    ]


def get_rare_entity_combination_items(data: list[dict]) -> tuple[list[dict], dict]:
    entity_combo_counts = Counter(get_entity_combo(item) for item in data)

    rare_combos = {
        combo
        for combo, count in entity_combo_counts.items()
        if count <= RARE_ENTITY_COMBO_MAX_COUNT
    }

    matching_items = [
        item
        for item in data
        if get_entity_combo(item) in rare_combos
    ]

    rare_combo_counts = {
        combo: entity_combo_counts[combo]
        for combo in sorted(rare_combos)
    }

    metadata = {
        "rare_entity_combo_max_count": RARE_ENTITY_COMBO_MAX_COUNT,
        "number_of_rare_entity_combinations": len(rare_combos),
        "rare_entity_combo_counts": rare_combo_counts,
    }

    return matching_items, metadata


def sample_items(items: list[dict], n: int, seed: int) -> list[dict]:
    rng = random.Random(seed)
    sample_size = min(n, len(items))

    return rng.sample(items, sample_size)


# =========================
# NOTEBOOK CREATION
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


def create_notebook(
    output_path: Path,
    request: dict,
    matching_count: int,
    sampled_items: list[dict],
    extra_metadata: dict | None = None,
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

    intro = (
        f"# {request['title']}\n\n"
        f"{request['description']}\n\n"
        f"Prompt folder: `{PROMPT_FOLDER_NAME}`\n\n"
        f"Matching files after filtering: `{matching_count}`\n\n"
        f"Samples in this notebook: `{len(sampled_items)}`\n\n"
        f"Excluded source-code terms: `{', '.join(SOURCE_CODE_EXCLUDE_TERMS)}`\n\n"
        f"Excluded path terms: `{', '.join(PATH_EXCLUDE_TERMS)}`\n"
    )

    if extra_metadata:
        intro += "\n## Extra metadata\n\n"
        intro += f"```json\n{json.dumps(extra_metadata, indent=2, ensure_ascii=False)}\n```\n"

    cells.append(make_markdown_cell(intro))

    if not sampled_items:
        cells.append(
            make_markdown_cell(
                "No valid samples were available for this requested combination."
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

    for i, item in enumerate(sampled_items, start=1):
        relative_file_path = normalize_path(item["file_path"])
        label_combination = all_characteristics_combo(labels_key(item))
        entity_combination = get_entity_combo(item)

        labels_text = json.dumps(
            item.get("predicted_labels", {}),
            indent=2,
            ensure_ascii=False,
        )

        cells.append(
            make_markdown_cell(
                f"## Sample {i}\n\n"
                f"**File path:**\n\n"
                f"`{relative_file_path}`\n\n"
                f"**Label combination:**\n\n"
                f"`{label_combination}`\n\n"
                f"**Entity combination:**\n\n"
                f"`{entity_combination}`\n\n"
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


# =========================
# SUMMARY HELPERS
# =========================

def save_request_match_files(
    output_path: Path,
    matching_items: list[dict],
    sampled_items: list[dict],
) -> None:
    output = {
        "matching_files": sorted(
            normalize_path(item["file_path"])
            for item in matching_items
        ),
        "sampled_files": sorted(
            normalize_path(item["file_path"])
            for item in sampled_items
        ),
    }

    write_json(output, output_path)


# =========================
# MAIN
# =========================

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTEBOOK_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Prompt folder: {PROMPT_DIR}")
    print(f"Clean JSON: {CLEAN_JSON_PATH}")
    print(f"Source root folder: {SRC_ROOT_DIR}")
    print(f"Output folder: {OUTPUT_DIR}")
    print(f"Notebook folder: {NOTEBOOK_DIR}")
    print()

    if not CLEAN_JSON_PATH.exists():
        raise FileNotFoundError(
            f"Could not find clean JSON: {CLEAN_JSON_PATH}"
        )

    data = read_json(CLEAN_JSON_PATH)

    filtered_data, filtering_summary = filter_items(data)

    write_json(
        filtering_summary,
        OUTPUT_DIR / "filtering_summary.json",
    )

    print(
        f"Kept {len(filtered_data)} of {len(data)} files after filtering."
    )
    print(
        f"Excluded by source-code terms: "
        f"{filtering_summary['total_excluded_by_source_code_terms']}"
    )
    print(
        f"Excluded by path terms: "
        f"{filtering_summary['total_excluded_by_path_terms']}"
    )
    print(
        f"Missing source files: "
        f"{filtering_summary['total_missing_source_files']}"
    )
    print()

    summary_rows = []

    for request_index, request in enumerate(REQUESTED_COMBINATIONS, start=1):
        request_name = request["name"]

        print(f"Processing: {request['title']}")

        extra_metadata = None

        if request.get("special") == "rare_entity_combinations":
            matching_items, extra_metadata = get_rare_entity_combination_items(
                filtered_data
            )
        else:
            matching_items = get_matching_items(filtered_data, request)

        sampled_items = sample_items(
            matching_items,
            n=N_SAMPLES,
            seed=RANDOM_SEED + request_index,
        )

        notebook_name = (
            f"{request_index:02d}_"
            f"{slugify(request_name)}_"
            f"{N_SAMPLES}_samples.ipynb"
        )

        notebook_path = NOTEBOOK_DIR / notebook_name

        create_notebook(
            output_path=notebook_path,
            request=request,
            matching_count=len(matching_items),
            sampled_items=sampled_items,
            extra_metadata=extra_metadata,
        )

        match_files_path = (
            OUTPUT_DIR
            / f"{request_index:02d}_{slugify(request_name)}_files.json"
        )

        save_request_match_files(
            output_path=match_files_path,
            matching_items=matching_items,
            sampled_items=sampled_items,
        )

        summary_rows.append(
            {
                "request_index": request_index,
                "name": request_name,
                "title": request["title"],
                "matching_files_after_filter": len(matching_items),
                "sampled_files": len(sampled_items),
                "notebook_path": str(notebook_path),
                "files_json_path": str(match_files_path),
            }
        )

        print(f"  Matching files: {len(matching_items)}")
        print(f"  Sampled files: {len(sampled_items)}")
        print(f"  Saved notebook: {notebook_path}")
        print()

    summary_path = OUTPUT_DIR / "advisor_requested_combination_summary.json"

    write_json(
        summary_rows,
        summary_path,
    )

    print("Done.")
    print(f"Summary saved: {summary_path}")
    print(f"All notebooks saved in: {NOTEBOOK_DIR}")


if __name__ == "__main__":
    main()