#!/usr/bin/env bash
set -euo pipefail

# Always run from the folder where this .sh file lives
cd "$(dirname "$0")"

echo "Step 1/3: running classification..."
# python -u 01_classify_artworks.py
python -u 01_classify_artworks_async.py

echo
echo "Step 2/3: running prediction processing..."
python -u 02_prediction_processing.py

echo
echo "Step 3/3: create prediction processing cases..."
python -u 05_create_random_src_samples.py

echo
echo "Done."