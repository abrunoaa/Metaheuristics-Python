#!/bin/bash

# CVRP
results="results/sa/"
for file in $(find . -name '*a280.tsp'); do
#for file in $(find . -name '*X\\X-n101-k25.vrp'); do
  output="${file%.*}.out"
  output="${output:12}"
  dir=$(dirname "${output}")
  result_file="$results$output"
  if [ ! -f "$result_file" ]; then
    echo "Processing $result_file"
    mkdir -p "$results$dir"
#    pypy3 sa_tsp.py "$file" # >"$result_file"
#    pypy3 ga_tsp.py "$file" # >"$result_file"
    pypy3 aco_tsp.py "$file" # >"$result_file"
#    pypy3 sa_cvrp.py "$file" # >"$result_file"
#    pypy3 ga_cvrp.py "$file" # >"$result_file"
  else
    echo "Ignoring $result_file"
  fi
done
