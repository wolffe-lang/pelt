#!/bin/bash
# sh08 gauntlet: every local check, each exit status recorded. usage: gauntlet.sh TAG
T=$1; D=${2:-$HOME/lanes/sh08/pelt}
cd "$D" || exit 9
export TMPDIR=$HOME/lanes/sh08/tmp
L=$HOME/lanes/sh08/logs
S=$L/$T.status
: > "$S"
echo "head=$(git rev-parse HEAD) dirty=$(git status --porcelain | wc -l) start=$(date -u +%FT%TZ)" >> "$S"
tools/fetch-toolchain > "$L/$T-fetch.log" 2>&1; echo "fetch=$?" >> "$S"
tools/check-fmt > "$L/$T-fmt.log" 2>&1; echo "fmt=$?" >> "$S"
tools/build --all > "$L/$T-build.log" 2>&1; echo "build=$?" >> "$S"
tools/check-test > "$L/$T-test.log" 2>&1; echo "test=$?" >> "$S"
tools/clause-census > "$L/$T-clause.log" 2>&1; echo "clause=$?" >> "$S"
for t in native release; do
  tools/difftest --bin target/$t > "$L/$T-diff-$t.log" 2>&1; echo "diff-$t=$?" >> "$S"
done
taskset -c 0-3 tools/difftest --bin target/release > "$L/$T-diff-release-taskset.log" 2>&1; echo "diff-taskset=$?" >> "$S"
tools/difftest-selftest target/release > "$L/$T-diff-selftest.log" 2>&1; echo "diff-selftest=$?" >> "$S"
for t in native release; do
  tools/session --bin target/$t > "$L/$T-sess-$t.log" 2>&1; echo "sess-$t=$?" >> "$S"
done
taskset -c 0-3 tools/session --bin target/release > "$L/$T-sess-release-taskset.log" 2>&1; echo "sess-taskset=$?" >> "$S"
tools/session-selftest target/release > "$L/$T-sess-selftest.log" 2>&1; echo "sess-selftest=$?" >> "$S"
for t in native release; do
  tools/glob-rss target/$t/pelt > "$L/$T-glob-$t.log" 2>&1; echo "glob-$t=$?" >> "$S"
  tools/loop-rss target/$t/pelt > "$L/$T-loop-$t.log" 2>&1; echo "loop-$t=$?" >> "$S"
  if [ -x tools/shape-rss ]; then
    tools/shape-rss target/$t/pelt > "$L/$T-shape-$t.log" 2>&1; echo "shape-$t=$?" >> "$S"
  fi
  tools/exec-witness target/$t/pelt > "$L/$T-exec-$t.log" 2>&1; echo "exec-$t=$?" >> "$S"
  tools/edit-witness target/$t/pelt > "$L/$T-edit-$t.log" 2>&1; echo "edit-$t=$?" >> "$S"
done
tools/oracle-record --check > "$L/$T-oracle-check.log" 2>&1; echo "oracle-check=$?" >> "$S"
tools/build --static > "$L/$T-static.log" 2>&1; echo "static=$?" >> "$S"
mkdir -p "$HOME/lanes/sh08/sc"
cp target/static/pelt "$HOME/lanes/sh08/sc/pelt-$T" && sha256sum "$HOME/lanes/sh08/sc/pelt-$T" >> "$S"
echo "done end=$(date -u +%FT%TZ)" >> "$S"
