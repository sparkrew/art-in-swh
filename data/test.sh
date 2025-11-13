#!/usr/bin/env bash
count=0
while [ $count -le 1 ]; do
  $(jq '.[count]' t2.json)
  ((count++))
done