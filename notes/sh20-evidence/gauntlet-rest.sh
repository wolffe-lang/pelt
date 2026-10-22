#!/bin/bash
# sh20: gauntlet-ctr.sh's gates from FROM on, for a run stopped part way
# (the pin's, stopped at the pause after sess-release-taskset). Inside
# ctr.sh. usage: gauntlet-rest.sh TAG TREE FROM
T=$1; TREE=$2; FROM=$3
S=$(cd "$(dirname "$0")" && pwd)
cd "$TREE" || exit 9
ulimit -c 0
L=$S/logs
St=$L/$T.status
echo "rest from $FROM: head=$(git rev-parse HEAD 2>/dev/null) ulimit -c $(ulimit -c)" >> "$St"
echo "ctr self: $(grep -E 'SigBlk|SigIgn' /proc/$$/status | tr '\n\t' '  ') nproc=$(nproc)" >> "$St"
on=0
run() { n=$1; shift; [ "$n" = "$FROM" ] && on=1; [ $on = 1 ] || return 0; "$@" > "$L/gauntlet/$T-$n.log" 2>&1; echo "$n=$?" >> "$St"; }
run sess-native-taskset taskset -c 0-3 tools/session --bin target/native
run sess-selftest tools/session-selftest target/release
for t in native release; do
  if [ -x tools/self-check ]; then
    run self-$t tools/self-check $t
  fi
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
