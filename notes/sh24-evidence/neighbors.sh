#!/bin/bash
S=$(cd "$(dirname "$0")" && pwd)
ulimit -c 0
for pass in 1 2 3; do
  for mode in bare four; do
    echo "neighbors pass=$pass mode=$mode $(uptime)"
    if [ "$mode" = four ]; then cmd=(taskset -c 8-11); else cmd=(); fi
    "${cmd[@]}" python3 "$S/probe/monitor-neighbors.py" "$S/head" "$S/base/target/native/pelt" "$S/head/target/native/pelt" "$S/base/target/release/pelt" "$S/head/target/release/pelt" /usr/bin/dash > "$S/logs/neighbors-$pass-$mode.log" 2>&1
    echo "neighbors pass=$pass mode=$mode exit=$?"
  done
done
