# Filter out .clj files
jq -c '
  .matches_info |= map(select(.[1] | endswith(".clj") | not)) |
  .match_count = (.matches_info | length) |
  select(.match_count > 0)
' matching_repos1.ndjson > matching_repos1_filtered.ndjson

# Count ori_swhid entries
wc -l < matching_repos1.ndjson

# Sum of all match_count values
jq -s 'map(.match_count) | add' matching_repos1.ndjson
