#!/bin/bash
set -u
S=$(cd "$(dirname "$0")" && pwd)
cd "$S/regress/head" || exit 9
ulimit -c 0
St=$S/logs/post-drain.status
: > "$St"
run() {
  local n=$1; shift
  echo "$(date -Is) start $n $(uptime)" | tee -a "$St"
  "$@" > "$S/logs/post-drain-$n.log" 2>&1 &
  local p=$! tick=0
  while kill -0 "$p" 2>/dev/null; do
    sleep 1; tick=$((tick+1)); if ((tick%60==0)); then echo "running $n $(uptime)"; fi
  done
  wait "$p"; local rc=$?
  echo "$n=$rc" | tee -a "$St"
  return "$rc"
}
rss() { run shape-$1 tools/shape-rss target/$1/pelt; }
sessions() {
  for t in native release; do
    run sess-$t tools/session --bin target/$t
    run sess-$t-taskset taskset -c 8-11 tools/session --bin target/$t
    run exec-$t tools/exec-witness target/$t/pelt
    run signal-$t tools/signal-witness target/$t/pelt
  done
  run fmt tools/check-fmt
  run clause tools/clause-census
  run width tools/gen-width --check
  run oracle-check tools/oracle-record --check
}
rss native & a=$!
rss release & b=$!
sessions & c=$!
wait "$a"; echo "rss-native=$?" >> "$St"
wait "$b"; echo "rss-release=$?" >> "$St"
wait "$c"; echo "sessions=$?" >> "$St"
echo done >> "$St"
