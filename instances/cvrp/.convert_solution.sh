#!/bin/bash

path="converted"
mkdir "$path"

for filename in $(find . -name '*X-*.sol'); do
  outfile=${filename%.*}.opt
  outfile=${outfile#*\\}
  outfile=${outfile##*/}
  outfile="$path/$outfile"
  echo "convert '$filename' to '$outfile'"

#  if [ "$filename" == "X-*.cvrp" ]; then
#    echo "$filename"
#  fi
#  continue

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
  done <"$filename"

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
    done <"$filename"
  fi

  {
    echo $answer
    echo "${routes[@]}"
  } >"$outfile"
done
