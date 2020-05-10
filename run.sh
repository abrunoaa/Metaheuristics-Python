#!/bin/bash

results="results/sa/"

# TSP
for file in $(find . -name '*a280.tsp'); do
#  break
  echo "Processing $file"
#  pypy3 tsp_aco.py "$file"
#  pypy3 tsp_ga.py "$file"
#  pypy3 tsp_sa.py "$file"
done

# CVRP
for file in $(find . -name '*X\\X-n101-k25.vrp'); do
#  break
  output="${file%.*}.out"
  output="${output:12}"
  dir=$(dirname "${output}")
  result_file="$results$output"
  if [ ! -f "$result_file" ]; then
    echo "Processing $file"
    mkdir -p "$results$dir"

#    pypy3 cvrp_aco.py "$file" # >"$result_file"
#    pypy3 cvrp_ga.py "$file" # >"$result_file"
    pypy3 cvrp_sa.py "$file" # >"$result_file"
  else
    echo "Ignoring $file"
  fi
done
