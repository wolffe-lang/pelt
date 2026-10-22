#!/bin/bash
set -u
S=$(cd "$(dirname "$0")" && pwd)
cd "$S/regress/head" || exit 9
ulimit -c 0
St=$S/logs/drain-verify.status
: > "$St"
run() {
  local n=$1; shift
  echo "$(date -Is) start $n $(uptime)" | tee -a "$St"
  "$@" > "$S/logs/drain-$n.log" 2>&1 &
  local p=$! tick=0
  while kill -0 "$p" 2>/dev/null; do
    sleep 1; tick=$((tick+1)); if ((tick%60==0)); then echo "running $n $(uptime)"; fi
  done
  wait "$p"; local rc=$?
  echo "$n=$rc" | tee -a "$St"
  return "$rc"
}
run record tools/oracle-record cmdsub/drain_chunks
for tier in native release; do
  run chunks-$tier tools/difftest --bin target/$tier cmdsub/drain_chunks
  for pass in 1 2 3 4 5 6; do
    run fixed-$tier-$pass tools/shape-rss --only substitution-pipeline target/$tier/pelt
  done
  run diff-$tier tools/difftest --bin target/$tier
  run diff-$tier-taskset taskset -c 8-11 tools/difftest --bin target/$tier
  run self-$tier tools/self-check $tier
done
run test tools/check-test
echo done >> "$St"
