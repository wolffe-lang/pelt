#!/bin/bash
# setm/run.sh — lane-local (sh22): each m*.sh under dash, bash --posix and
# the pelts given, without a terminal (stdin /dev/null, stderr into the
# same pipe as stdout) and with one (ttyrun.py). Inside ctr.sh.
# usage: run.sh OUTDIR PELT...
D=$(cd "$(dirname "$0")" && pwd)
O=$1; shift; mkdir -p "$O"
W=$TMPDIR/setm.$$; mkdir -p "$W"; cd "$W" || exit 9
for s in "$D"/m*.sh; do
  b=$(basename "$s" .sh)
  for sh in dash "bash --posix" "$@"; do
    n=$(basename "${sh%% *}")
    { $sh "$s" 2>&1 </dev/null; echo "exit $?"; } > "$O/$b.$n.notty.txt"
    python3 "$D/ttyrun.py" $sh "$s" > "$O/$b.$n.tty.txt" 2>&1
  done
done
cd / && rm -rf "$W"
