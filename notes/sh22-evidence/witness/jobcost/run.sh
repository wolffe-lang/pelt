#!/bin/bash
# jobcost/run.sh — lane-local (sh22): build main.lu on both tiers with
# pelt's pinned wolf and read each mode's peak RSS at N and 2N.
# usage: run.sh PELT_TREE OUTDIR
T=$1; O=$2; mkdir -p "$O"
D=$(cd "$(dirname "$0")" && pwd)
W=$T/.wolf-bin/wolf
"$W" build --deny-warnings "$D/main.lu" -o "$O/jobcost-native" || exit 2
"$W" build --release --deny-warnings "$D/main.lu" -o "$O/jobcost-release" || exit 2
for tier in native release; do
  for m in nine int1 bool1 str1 chunk; do
    a=$(/usr/bin/time -f %M "$O/jobcost-$tier" $m x 2>&1 >/dev/null | tail -1)
    b=$(/usr/bin/time -f %M "$O/jobcost-$tier" $m xx 2>&1 >/dev/null | tail -1)
    echo "jobcost: $tier $m 100000 ${a} KB 200000 ${b} KB  $(( (b - a) * 1024 / 100000 )) B a slot"
  done
done
