#!/bin/bash

path="converted/"
mkdir "$path"

for filename in $(find . -name '*.vrp'); do
  echo "$filename"

  outfile=${filename%.*}.cvrp
  outfile="$path/${outfile#*\\}"
  echo "convert '$filename' to '$outfile'"
  file=$(<"$filename")
  file=${file//[-$'\r']}

  dimension=$(echo ${file#*DIMENSION[[:space:]]*:} | cut -d ' ' -f 1)
  capacity=$(echo ${file#*CAPACITY[[:space:]]*:} | cut -d ' ' -f 1)
  locations=$(echo ${file#*NODE_COORD_SECTION} | cut -d ' ' -f 1-$((3 * dimension)))
  demand=$(echo ${file#*DEMAND_SECTION} | cut -d ' ' -f 1-$((2 * dimension)))

  if ! [[ "$dimension" =~ ^[0-9]+$ ]] || ! [[ "$capacity" =~ ^[0-9]+$ ]]; then
    echo "invalid file"
    continue
  fi

  {
    echo "$dimension $capacity"

    demand=($demand)
    echo -n "0"
    for ((i=1; i < $dimension; ++i)); do
      echo -n " ${demand[2 * i + 1]}"
    done
    echo ""

    locations=($locations)
    for ((i=0; i < $dimension; ++i)); do
      echo "${locations[3 * i + 1]} ${locations[3 * i + 2]}"
    done
  } >"$outfile"
done
