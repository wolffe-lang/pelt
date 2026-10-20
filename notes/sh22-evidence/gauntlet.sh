#!/bin/bash
# sh22 gauntlet (sh21's, split in two): the builds on kasumi's host (a
# compile kills nothing), every check that starts, signals, times out or
# kills a process inside this lane's container (ctr.sh, RULES §5). Each
# gate's exit status in logs/TAG.status. usage: gauntlet.sh TAG
T=$1
S=$HOME/lanes/sh22
TREE=${TREE:-$S/pelt}
cd "$TREE" || exit 9
export TMPDIR=$S/tmp
L=$S/logs
St=$L/$T.status
mkdir -p "$L/gauntlet"
: > "$St"
echo "head=$(git rev-parse HEAD) dirty=$(git status --porcelain | wc -l)" >> "$St"
run() { n=$1; shift; "$@" > "$L/gauntlet/$T-$n.log" 2>&1; echo "$n=$?" >> "$St"; }
run fetch tools/fetch-toolchain
run fmt tools/check-fmt
run build tools/build --all
run test tools/check-test
run clause tools/clause-census
run width tools/gen-width --check
sha256sum target/native/pelt target/release/pelt >> "$St"
CTRPIDS=8192 CTRDIR=$TREE "$S/ctr.sh" bash "$S/gauntlet-ctr.sh" "$T" "$TREE"
echo "ctr=$?" >> "$St"
echo done >> "$St"
