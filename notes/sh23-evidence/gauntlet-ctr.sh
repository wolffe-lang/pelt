#!/bin/bash
# sh23 gauntlet, the half inside the container (gauntlet.sh starts it).
# usage: gauntlet-ctr.sh TAG TREE
T=$1; TREE=$2
S=$(cd "$(dirname "$0")" && pwd)
cd "$TREE" || exit 9
L=$S/logs
St=$L/$T.status
echo "ctr self: $(grep -E 'SigBlk|SigIgn' /proc/$$/status | tr '\n\t' '  ') nproc=$(nproc)" >> "$St"
run() { n=$1; shift; "$@" > "$L/gauntlet/$T-$n.log" 2>&1; echo "$n=$?" >> "$St"; }
for t in native release; do
  run diff-$t tools/difftest --bin target/$t
done
run diff-release-taskset taskset -c 0-3 tools/difftest --bin target/release
run diff-native-taskset taskset -c 0-3 tools/difftest --bin target/native
run diff-selftest tools/difftest-selftest target/release
for t in native release; do
  run sess-$t tools/session --bin target/$t
done
run sess-release-taskset taskset -c 0-3 tools/session --bin target/release
run sess-native-taskset taskset -c 0-3 tools/session --bin target/native
run sess-selftest tools/session-selftest target/release
for t in native release; do
  run glob-$t tools/glob-rss target/$t/pelt
  run loop-$t tools/loop-rss target/$t/pelt
  run shape-$t tools/shape-rss target/$t/pelt
  run exec-$t tools/exec-witness target/$t/pelt
  run edit-$t tools/edit-witness target/$t/pelt
  run edit-$t-taskset taskset -c 0-3 tools/edit-witness target/$t/pelt
  run hist-$t tools/hist-witness target/$t/pelt
  run sigw-$t tools/signal-witness target/$t/pelt
  run sigw-$t-taskset taskset -c 0-3 tools/signal-witness target/$t/pelt
  if [ -x tools/reap-witness ]; then
    run reap-$t tools/reap-witness target/$t
  fi
done
run oracle-check python3 tools/oracle-record --check
echo "ctr done" >> "$St"
