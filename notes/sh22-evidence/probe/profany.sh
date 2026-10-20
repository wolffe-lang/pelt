#!/bin/bash
# profany — lane-local (sh22): heapprof.py over one loop per body given,
# TURNS turns each, the first SKIP chunk grabs skipped. Inside ctr.sh.
# usage: profany.sh SHELL OUTDIR TURNS SKIP BODY...
P=$1; O=$2; T=$3; K=$4; shift 4; mkdir -p "$O"
H=$(cd "$(dirname "$0")" && pwd)
D=$TMPDIR/profany.$$; mkdir -p "$D"; cd "$D" || exit 1
i=0
for body in "$@"; do
  i=$((i+1))
  { echo 'i=0'; echo "while [ \$i -lt $T ]; do"; printf '%b\n' "$body"; echo 'i=$((i+1)); done'; echo 'echo $i'; } > l$i.sh
  { echo "== loop [$body]"; timeout 1800 python3 "$H/heapprof.py" "$P" l$i.sh "$K"; } > "$O/loop$i.txt" 2>&1
done
cd / && rm -rf "$D"
