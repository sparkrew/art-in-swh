#!/usr/bin/env bash
#input: json list of urls
#output: list of urls + live / nolive

# File containing URLs
# The JSON file should look like: ["https://example.com", "https://another.com"]
# URL_FILE="test-sample.json"
URL_FILE="data_in_array.json"


# Declare associative array for results
declare -A url_status

# Read each URL from the JSON file
# jq -r enumerates each element
urls=$(jq -r '.[].origin' "$URL_FILE")

# Iterate through URLs
for url in $urls; do
    # Get HTTP status code (silent mode, no output)
    # curl the url, -o /dev/null sends the output to dev/null so only the code is printed,  -w "%{http_code} also removes HTTTP/2
    status_code=$(curl -o /dev/null -s -w "%{http_code}" "$url")

    # Check if status code starts with 2
    if [[ $status_code =~ ^2 ]]; then
        url_status["$url"]="live"
    else
        url_status["$url"]="nolive"
    fi
done

# Print results as JSON
echo "{"
first=true
for key in "${!url_status[@]}"; do
    if [ "$first" = true ]; then
        first=false
    else
        echo ","
    fi
    echo -n "  \"${key}\": \"${url_status[$key]}\""
done
echo
echo "}"
