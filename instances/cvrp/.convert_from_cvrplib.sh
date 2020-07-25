#!/bin/bash

path="converted"
mkdir "$path"


function convert() {
  if ! [[ "$dimension" =~ ^[0-9]+$ ]]; then
    echo "Invalid dimension: $dimension"
    return 1
  elif ! [[ "$capacity" =~ ^[0-9]+$ ]]; then
    echo "Invalid capacity: $capacity"
    return 1
  fi

  for ((i=1; i < dimension; ++i)); do
    if [[ "${demand[2 * i]}" != "$((i + 1))" ]]; then
      echo "Demand sequence is invalid: ${demand[2 * i]} at node $((i + 1)) (which will become $i)"
      return 1
    elif [[ ${demand[2 * i + 1]} -le 0 ]]; then
      echo "Demand must be > 0: ${demand[2 * i + 1]} at index ${2 * i + 1}"
      return 1
    fi
  done

  for ((i=0; i < dimension; ++i)); do
    if [[ "${locations[3 * i]}" -ne $((i + 1)) ]]; then
      echo "Location sequence is invalid: ${locations[3 * i]} at node $((i + 1)) (which will become $i)"
      return 1
    fi
  done

  if [[ $answer == 0 ]]; then
    echo "Can't find the answer"
    return 1
  fi

  {
    echo "$dimension $capacity"

    echo -n "0"
    for ((i=1; i < dimension; ++i)); do
      echo -n " ${demand[2 * i + 1]}"
    done
    echo ""

    for ((i=0; i < dimension; ++i)); do
      echo "${locations[3 * i + 1]} ${locations[3 * i + 2]}"
    done

    echo $answer
    echo "${routes[@]}"
  } >"$outfile"

  # convert to unix format
  writen=$(<"$outfile")
  echo "${writen//[-$'\r']}" >"$outfile"

  return 0
}


for vrp_file in $(find . -name '*.vrp'); do
  sol_file=${vrp_file%.*}.sol
  outfile=${vrp_file%.*}.cvrp
  outfile="$path/${outfile#*\\}"

  echo "convert '$vrp_file' and '$sol_file' to '$outfile'"

  # read cvrp file
  cvrp=$(<"$vrp_file")
  cvrp=${cvrp//[-$'\r']}

  # extract attributes
  dimension=$(echo ${cvrp#*DIMENSION[[:space:]]*:} | cut -d ' ' -f 1)
  capacity=$(echo ${cvrp#*CAPACITY[[:space:]]*:} | cut -d ' ' -f 1)
  locations=$(echo ${cvrp#*NODE_COORD_SECTION} | cut -d ' ' -f 1-$((3 * dimension)))
  demand=$(echo ${cvrp#*DEMAND_SECTION} | cut -d ' ' -f 1-$((2 * dimension)))

  # read solution for set X
  routes=(0)
  answer=0
  while read -r line; do
    line=($line)
    line=${line//[-$'\r']}

    if [ "${#line[@]}" == 1 ]; then
      if [ $answer == 0 ]; then
        answer=${line[0]}
      fi
      continue
    fi

    routes+=( ${line[@]:7} )
  done <"$sol_file"

  # read solution if isn't the set X
  if [ "$answer" == 0 ]; then
    routes=(0)
    while read -r line; do
      line=($line)
      line=${line//[-$'\r']}
      if [ "${line[0]}" == "cost" ] || [ "${line[0]}" == "Cost" ]; then
        answer=${line[1]}
        break
      fi

      routes+=( ${line[@]:2} 0 )
    done <"$sol_file"
  fi

  # convert to array
  demand=($demand)
  locations=($locations)

  convert "$@"
done
