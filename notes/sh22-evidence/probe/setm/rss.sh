#!/bin/bash
# setm/rss.sh — lane-local (sh22): what a `set -m` script's loop keeps a
# job until the loop ends (pelt#41), by shape-rss's method (peak RSS from
# /usr/bin/time at N and 2N turns): `set -m`, then N jobs in one loop,
# then `echo $i`. The notices (after the loop, as dash) go to /dev/null.
# Also the same loop without `set -m`. Inside ctr.sh (CTRPIDS high: a
# shell that reaps nothing in the loop holds N children).
# usage: rss.sh N SHELL...
N=$1; shift
W=$TMPDIR/setmrss.$$; mkdir -p "$W"; cd "$W" || exit 9
for sh in "$@"; do
  for body in 'env true &' 'true &'; do
    for m in "set -m" ":"; do
      for n in $N $((2 * N)); do
        { echo "$m"; echo 'exec 2>/dev/null'; echo 'i=0'; echo "while [ \$i -lt $n ]; do"; echo "$body"; echo 'i=$((i+1)); done'; echo 'echo $i'; } > s.sh
        /usr/bin/time -f %M -o t.out "$sh" s.sh > o.out
        rc=$?
        eval "kb$n=$(tail -1 t.out)"; eval "out$n=\$(cat o.out)"; eval "rc$n=$rc"
      done
      a=$(eval echo \$kb$N); b=$(eval echo \$kb$((2 * N)))
      echo "setm-rss: $(basename "$sh") [$m] [$body] $N ${a} KB $((2 * N)) ${b} KB  $(( (b - a) * 1024 / N )) B a job  (exit $(eval echo \$rc$N),$(eval echo \$rc$((2 * N))) out $(eval echo \$out$N),$(eval echo \$out$((2 * N))))"
    done
  done
done
cd / && rm -rf "$W"
