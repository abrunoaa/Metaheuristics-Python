#!/bin/bash

output_base_path='../results'

#for file in $(find ../instances/ -name '*.crp' -name '*.cvrp' -name '*.tsp'); do
#for file in $(find ../instances/ -name '*A-n32-k5.cvrp'); do
for file in $(find ../instances/ -name '*A-n80-k10.cvrp'); do
#for file in $(find ../instances/ -name '*X-n1001-k43.cvrp'); do
#for file in $(find ../instances/ -name '*berlin52.tsp'); do
  echo Processing "$file"

  instance=${file##*.}
  out_path="$output_base_path/$instance"
  output_file=${file##*/}
  output_file=${output_file%.*}.out

  echo "Reading from $file and writing to $out_path/ALGORITHM/$output_file"
  mkdir -p "$out_path/aco/"
  mkdir -p "$out_path/ga/"
  mkdir -p "$out_path/pso/"
  mkdir -p "$out_path/sa/"

  if [ "$instance" = "crp" ]; then
#    sudo nice -n -20 sudo -u brunoalmeda pypy3 -O run.py CRP ACO -i "$file" -o "$out_path/aco/$output_file"
#    sudo nice -n -20 sudo -u brunoalmeda pypy3 -O run.py CRP GA  -i "$file" -o "$out_path/ga/$output_file"
#    sudo nice -n -20 sudo -u brunoalmeda pypy3 -O run.py CRP PSO -i "$file" -o "$out_path/pso/$output_file"
    sudo nice -n -20 sudo -u brunoalmeda pypy3 -O run.py CRP SA  -i "$file" -o "$out_path/sa/$output_file"
  elif [ "$instance" = "cvrp" ]; then
#    sudo nice -n -20 sudo -u brunoalmeda pypy3 -O run.py CVRP ACO -i "$file" -o "$out_path/aco/$output_file"
#    sudo nice -n -20 sudo -u brunoalmeda pypy3 -O run.py CVRP GA  -i "$file" -o "$out_path/ga/$output_file"
    sudo nice -n -20 sudo -u brunoalmeda pypy3 -O run.py CVRP PSO -i "$file" -r 10 #-o "$out_path/pso/$output_file"
#    sudo nice -n -20 sudo -u brunoalmeda pypy3 -O run.py CVRP SA  -i "$file" -o "$out_path/sa/$output_file"
  elif [ "$instance" = "tsp" ]; then
    sudo nice -n -20 sudo -u brunoalmeda pypy3 -O run.py TSP ACO -i "$file" -o "$out_path/aco/$output_file"
#    sudo nice -n -20 sudo -u brunoalmeda pypy3 -O run.py TSP GA  -i "$file" -o "$out_path/ga/$output_file"
#    sudo nice -n -20 sudo -u brunoalmeda pypy3 -O run.py TSP PSO -i "$file" -o "$out_path/pso/$output_file"
#    sudo nice -n -20 sudo -u brunoalmeda pypy3 -O run.py TSP SA  -i "$file" -o "$out_path/sa/$output_file"
  else
    echo "Error: unknown instance of '$instance' from '$file'"
  fi

  echo "Done."
done
