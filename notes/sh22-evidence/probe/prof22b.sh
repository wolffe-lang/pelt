#!/bin/bash
# prof22b — lane-local (sh22): heapprof.py over the shapes too small for
# prof22.sh's 3,000 turns (20,000 turns, the first 5 grabs skipped).
# Runs inside ctr.sh (CTRPIDS=32768: pelt reaps no job nobody waits for).
# usage: prof22b.sh SHELL OUTDIR [TURNS]
P=$1; O=$2; T=${3:-20000}; mkdir -p "$O"
H=$(cd "$(dirname "$0")" && pwd)
D=$TMPDIR/profb.$$; mkdir -p "$D"; cd "$D" || exit 1
i=0
while IFS= read -r body; do
  i=$((i+1))
  { echo 'i=0'; echo "while [ \$i -lt $T ]; do"; printf '%b\n' "$body"; echo 'i=$((i+1)); done'; echo 'echo $i'; } > l$i.sh
  { echo "== loop [$body]"; timeout 1800 python3 "$H/heapprof.py" "$P" l$i.sh 5; } > "$O/loop$i.txt" 2>&1
done <<'B'
command true
umask 022
true &
env true &
cd .
:
B
cd / && rm -rf "$D"
