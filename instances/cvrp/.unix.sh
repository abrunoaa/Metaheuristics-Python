#!/bin/bash

for filename in $(find . -name '*.cvrp'); do
  file=$(<"$filename")
  echo "${file//[-$'\r']}" >"$filename"
done
