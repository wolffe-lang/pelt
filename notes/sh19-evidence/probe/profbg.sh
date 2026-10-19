#!/bin/bash
# profbg — lane-local (sh19): heapprof.py over one loop per background
# shape (pelt#33). usage: profbg.sh SHELL OUTDIR [TURNS]
P=$1; O=$2; T=${3:-3000}; mkdir -p "$O"
D=$HOME/lanes/sh19/tmp/prof.$$; mkdir -p "$D"; cd "$D" || exit 1
export TMPDIR=$D
i=0
while IFS= read -r body; do
  i=$((i+1))
  { echo 'i=0'; echo "while [ \$i -lt $T ]; do"; echo "$body"; echo 'i=$((i+1)); done'; echo 'echo $i'; } > l$i.sh
  { echo "== loop [$body]"; timeout 1800 python3 "$HOME/lanes/sh19/probe/heapprof.py" "$P" l$i.sh; } > "$O/loop$i.txt" 2>&1
done <<'B'
wait
true &
env true &
true & wait
env true & wait $!
( true ) & wait
B
cd / && rm -rf "$D"
