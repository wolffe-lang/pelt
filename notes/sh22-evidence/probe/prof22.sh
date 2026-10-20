#!/bin/bash
# prof22 — lane-local (sh22): heapprof.py (sh08's, unchanged but its
# docstring) over one loop per pelt#39 shape. Runs inside ctr.sh.
# usage: prof22.sh SHELL OUTDIR [TURNS]
P=$1; O=$2; T=${3:-3000}; mkdir -p "$O"
H=$(cd "$(dirname "$0")" && pwd)
D=$TMPDIR/prof.$$; mkdir -p "$D"; cd "$D" || exit 1
i=0
while IFS= read -r body; do
  i=$((i+1))
  { echo 'i=0'; echo "while [ \$i -lt $T ]; do"; printf '%b\n' "$body"; echo 'i=$((i+1)); done'; echo 'echo $i'; } > l$i.sh
  { echo "== loop [$body]"; timeout 1800 python3 "$H/heapprof.py" "$P" l$i.sh; } > "$O/loop$i.txt" 2>&1
done <<'B'
read x </dev/null
eval :
cd .
command true
umask 022
umask >/dev/null
true &
env true &
B
cd / && rm -rf "$D"
