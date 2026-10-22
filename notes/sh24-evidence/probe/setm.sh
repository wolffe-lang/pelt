#!/bin/sh
set -m
exec 2>/dev/null
i=0
while [ $i -lt 3000 ]; do
  env true & wait $!
  i=$((i+1))
done
echo $i
