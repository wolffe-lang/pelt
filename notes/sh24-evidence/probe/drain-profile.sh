#!/bin/sh
f() { :; }
g() { local v; v=$1; return 0; }
i=0
while [ $i -lt 10000 ]; do
  x=$(echo a | cat)
  i=$((i+1))
done
echo $i
