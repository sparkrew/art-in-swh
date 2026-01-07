import json
import os


SWH_INPUT_FILE = 'no_live_status/swh_files.json'
GH_INPUT_FILE = 'no_live_status/github_art_repos_by_topic_parsed.txt'
OUTPUT_FILE = 'no_live_status/all_data_sources.json'


def parse_file_line(line):
    """Parse SWH input line into structured JSON entry."""
    try:
        data = json.loads(line)
    except json.JSONDecodeError:
        return None

    repo_url = data.get("ori_url")
    ori_swhid = data.get("ori_swhid")
    matches = data.get("matches_info", [])

    matched_files = []
    extensions = set()

    for match in matches:
        if len(match) >= 2:
            swhid, filename = match[0], match[1]
            matched_files.append({"file_name": filename, "swhid": swhid})
            _, ext = os.path.splitext(filename)
            if ext:
                extensions.add(ext)

    new_entry = {
        repo_url: {
            "SWH_GHtopics": {"enum": []},
            "SWH_signals": {"enum": sorted(list(extensions)) if extensions else []},
            "matched_files": matched_files if matched_files else None,
            "live": None,  
            "swhid": ori_swhid or None
        }
    }
    return new_entry


def parse_gh_repos(line):
    """Parse GitHub repo topic line."""
    try:
        parts = line.strip().split('\t')
        if len(parts) < 2:
            return None

        repo_url = parts[0].strip().strip('"')
        topics = json.loads(parts[1].strip())

        if not isinstance(topics, list):
            topics = [topics]

        # remove duplicates / empty strings
        topics = [t for t in topics if t]

        new_entry = {
            repo_url: {
                "SWH_GHtopics": {"enum": topics},
                "SWH_signals": {"enum": []},
                "matched_files": None,
                "live": None,
                "swhid": None
            }
        }
        return new_entry

    except Exception as e:
        print(f"Error parsing GH repo line: {line.strip()} -> {e}")
        return None


def merge_entry(existing_data, new_entry):
    """
    Merge new GitHub entry into existing SWH data:
    - If repo exists: only update/merge SWH_signals (no duplicates, no nulls)
    - If new: add full entry
    """
    for repo_url, new_values in new_entry.items():
        if repo_url in existing_data:
            # Merge only signals
            existing_signals = existing_data[repo_url].get("SWH_signals", {}).get("enum", [])
            new_signals = new_values["SWH_signals"]["enum"]
            merged = sorted(set(existing_signals + new_signals))
            existing_data[repo_url]["SWH_signals"]["enum"] = merged
            return True
        else:
            # Add new entry as-is
            existing_data[repo_url] = new_values
            return False


def main():
    all_data = {}
    line_count = 0
    skipped_lines = 0

    # === 1. Read SWH source data ===
    print("Loading SWH input...")
    with open(SWH_INPUT_FILE, 'r', encoding='utf-8') as infile:
        for i, line in enumerate(infile):
            parsed = parse_file_line(line)
            if parsed:
                all_data.update(parsed)
            else:
                skipped_lines += 1
            line_count += 1
            if line_count % 100 == 0:
                print(f"Processed {line_count} SWH lines...")

    # === 2. Read GitHub repos and merge ===
    print("Merging GitHub repos...")
    merged_lines = 0
    with open(GH_INPUT_FILE, 'r', encoding='utf-8') as infile:
        for i, line in enumerate(infile):
            parsed = parse_gh_repos(line)
            if parsed:
                merged = merge_entry(all_data, parsed)
                if merged:
                    merged_lines += 1
            else:
                skipped_lines += 1
            line_count += 1
            if line_count % 100 == 0:
                print(f"Processed {line_count} total lines...")

    # === 3. Write merged output ===
    print("Writing output file...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
        json.dump(all_data, outfile, indent=2, ensure_ascii=False)

    print(f"✅ Done. Total processed: {line_count} lines.")
    print(f"✅ Skipped lines: {skipped_lines}")
    print(f"✅ Total unique repos: {len(all_data)}")
    print(f"✅ Merged GitHub entries into existing repos: {merged_lines}")


if __name__ == "__main__":
    main()