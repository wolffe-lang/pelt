#!/bin/bash
# sh24: approved two-RSS-worker schedule, immutable head/ binaries.
# Parent affinity is 8-11, including bare controls; four-core legs also
# spell taskset explicitly. Release sessions run independently.
set -u
S=$(cd "$(dirname "$0")" && pwd)
cd "$S/head" || exit 9
ulimit -c 0
T=final; L=$S/logs; St=$L/$T.status
printf 'schedule=two-RSS-workers inherited-affinity=8-11 head=%s\n' "$(cat CODE_HEAD)" >> "$St"
run() {
  local name=$1; shift
  local status=$L/gauntlet/$T-$name.status
  { echo "head=$(cat CODE_HEAD)"; echo "start=$(date -Is)"; uptime;
    taskset -p $$; printf 'command='; printf '%q ' "$@"; echo; } > "$status"
  echo "$(date -Is) start $name $(uptime)" | tee -a "$St"
  "$@" > "$L/gauntlet/$T-$name.log" 2>&1 &
  local pid=$! tick=0
  while kill -0 "$pid" 2>/dev/null; do
    sleep 1
    tick=$((tick+1))
    if ((tick % 60 == 0)); then echo "$(date -Is) running $name $(uptime)"; fi
  done
  wait "$pid"; local rc=$?
  echo "exit=$rc" >> "$status"
  echo "$name=$rc" | tee -a "$St"
  return "$rc"
}
release_checks() {
  run diff-release tools/difftest --bin target/release
  run diff-release-taskset taskset -c 8-11 tools/difftest --bin target/release
  run sess-release tools/session --bin target/release
  run sess-release-taskset taskset -c 8-11 tools/session --bin target/release
  run self-release taskset -c 8-11 tools/self-check release
  for gate in glob-rss loop-rss exec-witness edit-witness hist-witness signal-witness; do
    run $gate-release taskset -c 8-11 tools/$gate target/release/pelt
  done
  run reap-release taskset -c 8-11 tools/reap-witness target/release
  run edit-release-control tools/edit-witness target/release/pelt
  run signal-release-control tools/signal-witness target/release/pelt
  run edit-native-control tools/edit-witness target/native/pelt
  run signal-native-control tools/signal-witness target/native/pelt
  run diff-selftest tools/difftest-selftest target/release
  run sess-selftest tools/session-selftest target/release
  run oracle-check tools/oracle-record --check
}
rss_worker() {
  local worker=$1
  for tier in native release; do
    for pass in 1 2 3; do
      if [ "$worker" = 0 ]; then
        run shape-$tier-$pass tools/shape-rss target/$tier/pelt
      else
        run shape-$tier-$pass-taskset taskset -c 8-11 tools/shape-rss target/$tier/pelt
      fi
    done
  done
  if [ "$worker" = 0 ]; then
    # Completed sequential neighbor legs 1-bare,1-four,2-bare remain;
    # only the interrupted/unstarted legs are repeated here (P).
    for spec in 2-four 3-bare 3-four; do
      run neighbors-$spec python3 "$S/probe/monitor-neighbors.py" "$S/head" "$S/base/target/native/pelt" "$S/head/target/native/pelt" "$S/base/target/release/pelt" "$S/head/target/release/pelt" /usr/bin/dash
    done
  fi
}
release_checks & r=$!
rss_worker 0 & a=$!
rss_worker 1 & b=$!
wait "$r"; echo "release-driver=$?" >> "$St"
wait "$a"; echo "rss-worker-0=$?" >> "$St"
wait "$b"; echo "rss-worker-1=$?" >> "$St"
echo done >> "$St"
