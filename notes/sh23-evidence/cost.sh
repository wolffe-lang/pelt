#!/bin/bash
# sh23: the check's cost (§3.5), inside the container under taskset -c 0-3.
# An interactive pelt (`pelt -i`, the lines on standard input) runs a loop
# of N commands that command search finds nowhere (`nosuch_sh23`, stderr
# to /dev/null), with the option off and on; and, for scale, a loop of a
# program it finds (`basename x`). Wall time: 7 runs each, interleaved,
# the median kept. System calls: one run at N=1000 under strace -f -c.
# usage: cost.sh PELT_DIR OUT   (PELT_DIR/native/pelt, PELT_DIR/release/pelt)
set -u
B=$1; OUT=$2; mkdir -p "$OUT"
W=$(mktemp -d "${TMPDIR:-/tmp}/sh23-cost.XXXXXX"); cd "$W"
mk() { # file opt n cmd
  { [ "$2" = on ] && echo "set -o autocd"
    echo "i=0; while [ \$i -lt $3 ]; do $4; i=\$((i+1)); done; exit"; } > "$1"
}
for o in off on; do
  mk miss-$o.in $o 10000 'nosuch_sh23 2>/dev/null'
  mk found-$o.in $o 2000 'basename x >/dev/null'
  mk miss1k-$o.in $o 1000 'nosuch_sh23 2>/dev/null'
done
TIMEFORMAT=%R
for t in native release; do
  p=$B/$t/pelt
  for shape in miss found; do
    for o in off on; do : > "$OUT/$t-$shape-$o.times"; done
    for r in 1 2 3 4 5 6 7; do
      for o in off on; do
        { time taskset -c 0-3 "$p" -i < $shape-$o.in > /dev/null 2>&1 ; } 2>> "$OUT/$t-$shape-$o.times"
      done
    done
    for o in off on; do
      echo "$t $shape $o median $(sort -n "$OUT/$t-$shape-$o.times" | sed -n 4p) s, runs $(tr '\n' ' ' < "$OUT/$t-$shape-$o.times")" >> "$OUT/summary.txt"
    done
  done
  for o in off on; do
    taskset -c 0-3 strace -f -c -o "$OUT/$t-strace-miss1k-$o.txt" "$p" -i < miss1k-$o.in > /dev/null 2>&1
    echo "$t strace miss x1000 $o: total $(awk '/total/ {print $4}' "$OUT/$t-strace-miss1k-$o.txt") calls; stat-family $(awk '$NF ~ /stat/ {s += $4} END {print s+0}' "$OUT/$t-strace-miss1k-$o.txt")" >> "$OUT/summary.txt"
  done
done
cd /; rm -rf "$W"
cat "$OUT/summary.txt"
