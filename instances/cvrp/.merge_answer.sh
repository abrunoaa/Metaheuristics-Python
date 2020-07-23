#!/bin/bash

path="converted"
mkdir "$path"

for filename in $(find . -name '*.cvrp'); do
#  echo "$filename"
  ans_filename=${filename%.*}.opt

  outfile=${filename%.*}.cvrp2
  outfile=${outfile#*\\}
  outfile=${outfile##*/}
  outfile="$path/$outfile"
  echo "convert '$filename' to '$outfile'"

  {
    echo "$(<"$filename")"
    echo "$(<"$ans_filename")"
  } >"$outfile"
done
