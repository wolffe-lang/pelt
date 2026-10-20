#!/bin/bash
# cwdregion/run.sh — lane-local (sh22): build main.lu on both tiers with
# pelt's pinned wolf, read each mode's peak RSS at N and 2N.
# usage: run.sh PELT_TREE OUTDIR
T=$1; O=$2; mkdir -p "$O"
D=$(cd "$(dirname "$0")" && pwd)
W=$T/.wolf-bin/wolf
"$W" build --deny-warnings "$D/main.lu" -o "$O/cwdregion-native" || exit 2
"$W" build --release --deny-warnings "$D/main.lu" -o "$O/cwdregion-release" || exit 2
cd "$O" || exit 9
for tier in native release; do
  for m in cwd interp none; do
    a=$(/usr/bin/time -f %M "$O/cwdregion-$tier" $m x 2>&1 >/dev/null | tail -1)
    b=$(/usr/bin/time -f %M "$O/cwdregion-$tier" $m xx 2>&1 >/dev/null | tail -1)
    echo "cwdregion: $tier $m (cwd $(pwd | wc -c) bytes) 100000 ${a} KB 200000 ${b} KB  $(( (b - a) * 1024 / 100000 )) B a call"
  done
done
