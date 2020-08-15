#!/bin/bash

input_base_path='../instances'
output_base_path='../results'
repeat=3
population_size=20

function execute {
  output_path="$output_base_path/$instance/$2"
  mkdir -p "$output_path/"

  echo "Reading from '$file' and writing to '$output_path/$output_file.out'"
  pypy3 -O run.py "$1" "$2" -r $repeat -s $population_size -i "$file" -o "$output_path/$output_file.out"

  if [ $? != 0 ]; then
    echo "The execution for file '$file' failed"
  fi

#  mkdir -p "$output_path/plots/"
#  for ((i=0; i < repeat; ++i)); do
#    python3.8 "plot-$i.py" >"$output_path/plots/$output_file-$i.png"
#  done
#  find . -name 'plot-*.py' -delete
}

#for file in $(find "$input_base_path" -name '*.crp'); do
#for file in $(find "$input_base_path" -name '*[ABEFMP]-n*.cvrp'); do
#for file in $(find "$input_base_path" -name '*X-n*.cvrp'); do
#for file in $(find "$input_base_path" -name '*A-n32-k5.cvrp'); do
#for file in $(find "$input_base_path" -name '*A-n80-k10.cvrp'); do
#for file in $(find "$input_base_path" -name '*.tsp'); do
#for file in $(find "$input_base_path" -name '*berlin52.tsp'); do
for file in 'X-n101-k25' 'X-n120-k6' 'X-n125-k30' 'X-n134-k13' 'X-n148-k46' 'X-n153-k22' 'X-n186-k15' 'X-n270-k35' 'X-n313-k71' 'X-n336-k84' 'X-n359-k29' 'X-n439-k37' 'X-n459-k26' 'X-n469-k138' 'X-n502-k39' 'X-n599-k92' 'X-n685-k75' 'X-n733-k159'; do
  file="../instances/cvrp/$file.cvrp"
#  echo $file
#  continue

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
#    execute cvrp ba
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
