#!/bin/bash

input_base_path='../instances'
output_base_path='../results'

function execute {
  repeat=3
  population_size=20
  output_path="$output_base_path/$instance/$2/test"
  mkdir -p "$output_path/"

  echo "Reading from '$file' and writing to '$output_path/$output_file.out'"
  pypy3 run.py "$1" "$2" -r $repeat -s $population_size -i "$file" #-o "$output_path/$output_file.out"

  if [ $? != 0 ]; then
    echo "$file"
  fi

#  mkdir -p "$output_path/plots/"
#  for ((i=0; i < repeat; ++i)); do
#    python3.8 "plot-$i.py" >"$output_path/plots/$output_file-$i.png"
#  done
#  find . -name 'plot-*.py' -delete
}

#for file in $(find "$input_base_path" -name '*.crp'); do
#for file in $(find "$input_base_path" -name '*.cvrp'); do
#for file in $(find "$input_base_path" -name '*[ABEFMP]-n*.cvrp'); do
#for file in $(find "$input_base_path" -name '*A-n32-k5.cvrp'); do
for file in $(find "$input_base_path" -name '*A-n80-k10.cvrp'); do
#for file in $(find "$input_base_path" -name '*X-n101-k25.cvrp'); do
#for file in $(find "$input_base_path" -name '*X-n1001-k43.cvrp'); do
#for file in $(find "$input_base_path" -name '*.tsp'); do
#for file in $(find "$input_base_path" -name '*berlin52.tsp'); do

  instance=${file##*.}
  output_file=${file##*/}
  output_file=${output_file%.*}

  if [ "$instance" = "crp" ]; then
#    execute crp aco
#    execute crp ga
#    execute crp pso
    execute crp sa
  elif [ "$instance" = "cvrp" ]; then
    execute cvrp aco
#    execute cvrp ga
#    execute cvrp pso
#    execute cvrp sa
  elif [ "$instance" = "tsp" ]; then
#    execute tsp aco
#    execute tsp ga
#    execute tsp pso
    execute tsp sa
  else
    echo "Error: unknown instance of '$instance' from '$file'"
  fi

#  echo "Done."
done
