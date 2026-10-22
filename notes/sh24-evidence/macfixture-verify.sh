#!/bin/bash
set -u
S=$(cd "$(dirname "$0")" && pwd)
cd "$S/macfixture" || exit 9
ulimit -c 0
St=$S/logs/macfixture.status
: > "$St"
run() {
  local n=$1; shift
  echo "$(date -Is) start $n $(uptime)" | tee -a "$St"
  "$@" > "$S/logs/macfixture-$n.log" 2>&1 &
  local p=$! tick=0
  while kill -0 "$p" 2>/dev/null; do
    sleep 1; tick=$((tick+1)); if ((tick%60==0)); then echo "running $n $(uptime)"; fi
  done
  wait "$p"; local rc=$?
  echo "$n=$rc" | tee -a "$St"
  return "$rc"
}
run build tools/build --all || exit 2
run record tools/oracle-record cmdsub/drain_chunks
for t in native release; do
  run row-$t tools/difftest --bin target/$t cmdsub/drain_chunks
  run cmdsub-$t tools/difftest --bin target/$t cmdsub
  run corpus-$t tools/difftest --bin target/$t
done
run oracle-check tools/oracle-record --check
echo done >> "$St"
