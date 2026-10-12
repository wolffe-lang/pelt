#!/bin/bash
# lane-local: pelt reading N command lines from a file, interactive (-i) and not; usage: typed-file.sh PELT LINE
P=$1; L=$2
cd "$HOME/lanes/sh08/tmp" || exit 9
for n in 10000 20000; do
  : > ti.sh; k=0; while [ $k -lt $n ]; do printf '%s; i=$((i+1))\n' "$L" >> ti.sh; k=$((k+1)); done; echo 'echo $i' >> ti.sh
  /usr/bin/time -f %M -o t.out "$P" -i < ti.sh > o.out 2>/dev/null; echo "-i from a file $n: $(cat t.out) KB, out $(tail -1 o.out)"
  /usr/bin/time -f %M -o t.out "$P" < ti.sh > o.out 2>/dev/null; echo "stdin, not -i $n: $(cat t.out) KB, out $(tail -1 o.out)"
done
