#!/bin/bash
# lane-local: quick checks on the dev worktree; usage: dtest.sh TAG [shape names]
T=$1; SH=${2:-pipeline,subshell,substitution,call}
cd "$HOME/lanes/sh08/dev" || exit 9
export TMPDIR=$HOME/lanes/sh08/tmp
L=$HOME/lanes/sh08/logs
tools/difftest --bin target/native > "$L/dev-$T-diff-native.log" 2>&1; echo "diff-native=$?"; tail -2 "$L/dev-$T-diff-native.log"
tools/shape-rss --only "$SH" target/release/pelt > "$L/dev-$T-shape.log" 2>&1; echo "shape=$?"; cat "$L/dev-$T-shape.log"
