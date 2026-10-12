#!/bin/bash
# profall — lane-local (sh08): heapprof.py over one script per shape. usage: profall.sh SHELL OUTDIR
P=$1; O=$2; mkdir -p "$O"
D=$HOME/lanes/sh08/tmp/prof.$$; mkdir -p "$D"; cd "$D" || exit 1
export TMPDIR=$D
i=0
while IFS= read -r body; do
  i=$((i+1))
  { echo 'f() { :; }'; echo 'g() { local v; v=$1; return 0; }'; echo 'i=0'
    echo "while [ \$i -lt 3000 ]; do"; echo "$body"; echo 'i=$((i+1)); done'; echo 'echo $i'; } > l$i.sh
  { echo "== loop [$body]"; timeout 1200 python3 "$HOME/lanes/sh08/probe/heapprof.py" "$P" l$i.sh; } > "$O/loop$i.txt" 2>&1
done <<'B'
x=$(true)
g a b
f
( true )
case a in a) :;; esac
for j in 1; do :; done
x=$(echo a | cat)
B
for line in 'true' ': $((i=i+1))' 'f'; do
  i=$((i+1))
  { echo 'f() { :; }'; k=0; while [ $k -lt 4000 ]; do echo "$line"; k=$((k+1)); done; } > s$i.sh
  { echo "== script [$line]"; timeout 1200 python3 "$HOME/lanes/sh08/probe/heapprof.py" "$P" s$i.sh 5; } > "$O/script$i.txt" 2>&1
done
cd / && rm -rf "$D"
