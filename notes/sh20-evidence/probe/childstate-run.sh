#!/bin/bash
# sh20: childstate.sh under SHELL three ways (inside ctr.sh): a script,
# a script with `set -m`, and typed at `SHELL -i -m` through a pty.
# usage: childstate-run.sh SHELL OUT (OUT absolute)
SH=$1; OUT=$2
D=$(cd "$(dirname "$0")" && pwd)
cd "$TMPDIR" || exit 9
cp "$D/childstate.sh" ./childstate.sh
{
  echo "## script"; "$SH" ./childstate.sh 2>&1
  echo "## set -m script"; "$SH" -c 'set -m; . ./childstate.sh' 2>&1
  echo "## typed, -i -m"; python3 "$D/typein.py" "$SH" ". ./childstate.sh" 2>&1
} > "$OUT"
