#!/bin/bash
# sh24: every build/check in ctr.sh's pid namespace. Called inside it.
set -u
S=$HOME # ctr.sh uses scratch HOME: derive lane from this script instead
S=$(cd "$(dirname "$0")" && pwd)
TREE=$1; T=$2; CPUSET=${CPUSET:-8-11}
cd "$TREE" || exit 9
ulimit -c 0
L=$S/logs; mkdir -p "$L/gauntlet"
St=$L/$T.status
printf 'head=%s\ncpus=%s ulimit=%s\n' "$(cat CODE_HEAD)" "$CPUSET" "$(ulimit -c)" > "$St"
run() {
  local n=$1; shift
  echo "$(date -Is) start $n $(uptime)" | tee -a "$St"
  "$@" > "$L/gauntlet/$T-$n.log" 2>&1 &
  local pid=$!
  local tick=0
  while kill -0 "$pid" 2>/dev/null; do
    sleep 1
    tick=$((tick+1))
    if (( tick % 60 == 0 )); then
      echo "$(date -Is) running $n $(uptime)"
    fi
  done
  wait "$pid"; local rc=$?
  echo "$n=$rc" | tee -a "$St"
  return "$rc"
}
run fmt taskset -c "$CPUSET" tools/check-fmt
run build taskset -c "$CPUSET" tools/build --all || exit 2
run test taskset -c "$CPUSET" tools/check-test
run clause taskset -c "$CPUSET" tools/clause-census
run width taskset -c "$CPUSET" tools/gen-width --check
sha256sum target/{native,release}/pelt >> "$St"
for t in native release; do
  run diff-$t tools/difftest --bin target/$t
  run diff-$t-taskset taskset -c "$CPUSET" tools/difftest --bin target/$t
  run sess-$t tools/session --bin target/$t
  run sess-$t-taskset taskset -c "$CPUSET" tools/session --bin target/$t
  run self-$t taskset -c "$CPUSET" tools/self-check $t
  for gate in glob-rss loop-rss exec-witness edit-witness hist-witness signal-witness; do
    run $gate-$t taskset -c "$CPUSET" tools/$gate target/$t/pelt
  done
  run reap-$t taskset -c "$CPUSET" tools/reap-witness target/$t
  for pass in 1 2 3; do
    run shape-$t-$pass tools/shape-rss target/$t/pelt
    run shape-$t-$pass-taskset taskset -c "$CPUSET" tools/shape-rss target/$t/pelt
  done
done
run diff-selftest taskset -c "$CPUSET" tools/difftest-selftest target/release
run sess-selftest taskset -c "$CPUSET" tools/session-selftest target/release
run oracle-check taskset -c "$CPUSET" tools/oracle-record --check
echo done >> "$St"
