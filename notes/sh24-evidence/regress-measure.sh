#!/bin/bash
set -u
S=$(cd "$(dirname "$0")" && pwd)
ulimit -c 0
St=$S/logs/regress-measure.status
: > "$St"
run() {
  local n=$1; shift
  echo "$(date -Is) start $n $(uptime)" | tee -a "$St"
  "$@" > "$S/logs/regress-$n.log" 2>&1 &
  local p=$! tick=0
  while kill -0 "$p" 2>/dev/null; do
    sleep 1; tick=$((tick+1))
    if ((tick%60==0)); then echo "running $n $(uptime)"; fi
  done
  wait "$p"; local rc=$?
  echo "$n=$rc" | tee -a "$St"
  return "$rc"
}
for tree in base head; do
  cd "$S/regress/$tree" || exit 9
  run build-$tree tools/build --all || exit 2
done
cd "$S/regress/head" || exit 9
for pass in 1 2 3 4 5 6; do
  for tier in native release; do
    for tree in base head; do
      run $tree-$tier-$pass tools/shape-rss --only substitution-pipeline "$S/regress/$tree/target/$tier/pelt"
    done
  done
done
echo done >> "$St"
