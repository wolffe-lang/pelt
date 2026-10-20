#!/bin/bash
# profsetm — lane-local (sh22): heapprof.py over a `set -m` script whose
# loop starts BODY TURNS times (pelt#41's loop), the notices to
# /dev/null. Inside ctr.sh. usage: profsetm.sh SHELL OUT TURNS BODY
P=$1; O=$2; T=$3; B=$4
H=$(cd "$(dirname "$0")" && pwd)
D=$TMPDIR/profsetm.$$; mkdir -p "$D"; cd "$D" || exit 1
{ echo 'set -m'; echo 'exec 2>/dev/null'; echo 'i=0'; echo "while [ \$i -lt $T ]; do"; echo "$B"; echo 'i=$((i+1)); done'; echo 'echo $i'; } > l.sh
{ echo "== set -m loop [$B]"; timeout 1800 python3 "$H/heapprof.py" "$P" l.sh 5; } > "$O" 2>&1
cd / && rm -rf "$D"
