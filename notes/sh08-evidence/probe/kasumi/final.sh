#!/bin/bash
# sh08: at the pushed head — the gauntlet, the script census both ways, then the bench.
# Waits first for an earlier lane-local perf run (pid given) to end, so the bench is not shared with it.
set -u
S=$HOME/lanes/sh08
T=${1:-head2}
W=${2:-}
if [ -n "$W" ]; then while kill -0 "$W" 2>/dev/null; do sleep 20; done; fi
"$S/head.sh" "$T"
"$S/census.sh" "$T-unaided" "$S/sc/pelt-$T"
"$S/census.sh" "$T-aided" "$S/sc/pelt-$T" --aided
"$S/bench.sh" "$S/wt-$T" > "$S/logs/$T-bench.out" 2>&1
echo finished > "$S/logs/$T-final.done"
