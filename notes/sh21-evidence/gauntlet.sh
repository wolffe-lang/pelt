#!/bin/bash
# sh21 gauntlet (sh19's, its paths moved): every local check, each exit status recorded. usage: gauntlet.sh TAG
T=$1
S=$HOME/lanes/sh21
TREE=${TREE:-$S/pelt}
cd "$TREE" || exit 9
export TMPDIR=$S/tmp
L=$S/logs
St=$L/$T.status
: > "$St"
echo "head=$(git rev-parse HEAD) dirty=$(git status --porcelain | wc -l)" >> "$St"
echo "self: $(grep -E 'SigBlk|SigIgn' /proc/$$/status | tr '\n\t' '  ')" >> "$St"
run() { n=$1; shift; "$@" > "$L/$T-$n.log" 2>&1; echo "$n=$?" >> "$St"; }
run fetch tools/fetch-toolchain
run fmt tools/check-fmt
run build tools/build --all
run test tools/check-test
run clause tools/clause-census
run width tools/gen-width --check
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
done
run oracle-check env REFDIR=$TREE $S/refrun.sh python3 tools/oracle-record --check
run static tools/build --static
cp target/static/pelt "$S/sc/pelt-$T" && sha256sum "$S/sc/pelt-$T" >> "$St"
sha256sum target/native/pelt target/release/pelt >> "$St"
echo done >> "$St"
