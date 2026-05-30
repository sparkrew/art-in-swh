import json
from pathlib import Path

PREDICTIONS_FILE = Path("../artworks/predictions.json")
SUCCESS_FILE = Path("../artworks/successes.txt")


def main():
    with PREDICTIONS_FILE.open("r", encoding="utf-8") as f:
        predictions = json.load(f)

    file_paths = []
    seen = set()

    for item in predictions:
        file_path = item.get("file_path")
        if file_path and file_path not in seen:
            seen.add(file_path)
            file_paths.append(file_path)

    with SUCCESS_FILE.open("w", encoding="utf-8") as f:
        for file_path in file_paths:
            f.write(file_path + "\n")

    print(f"Rebuilt {SUCCESS_FILE} with {len(file_paths)} paths.")


if __name__ == "__main__":
    main()