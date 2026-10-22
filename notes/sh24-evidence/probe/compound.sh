#!/bin/sh
i=0
while [ $i -lt 10000 ]; do
  { true; } >/dev/null
  i=$((i+1))
done
echo $i
