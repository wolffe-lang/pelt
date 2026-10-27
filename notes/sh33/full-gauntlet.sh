#!/bin/bash
# Run inside ctr.sh: lock and explicit in-container CPU8–11 affinity.
set -u -o pipefail
S=/home/mfwolffe/lanes/sh33
L=$S/full-logs
mkdir -p "$L"
: > "$L/status"
bad=0
run() {
    local name=$1
    shift
    printf 'BEGIN %s %s\n' "$name" "$(date -Iseconds)"
    if "$@" > "$L/$name.log" 2>&1; then rc=0; else rc=$?; fi
    printf '%s %s\n' "$name" "$rc" >> "$L/status"
    tail -4 "$L/$name.log"
    printf 'END %s status=%s %s\n' "$name" "$rc" "$(date -Iseconds)"
    if [ "$rc" -ne 0 ]; then bad=$((bad+1)); fi
}
git rev-parse HEAD > "$L/head"
find src -name '*.lu' -type f -print0 | sort -z | xargs -0 sha256sum > "$L/sources-before"
grep '^SigBlk:\|^SigIgn:\|^Cpus_allowed_list:' /proc/self/status
python3 -c 'import os; assert os.sched_getaffinity(0) == {8,9,10,11}; print("affinity: 8–11")' || exit 2
run fmt tools/check-fmt
run planner python3 ci/tiers-test.py
run clauses tools/clause-census
run checked tools/check-test
for tier in native release; do
    run "$tier-build" tools/build "--$tier"
    run "$tier-selfcheck" tools/self-check "$tier"
    run "$tier-corpus" tools/difftest --bin "target/$tier"
    run "$tier-floats-wording" python3 -I notes/sh33/probe-floats.py "target/$tier/pelt"
    run "$tier-sessions" timeout 1800 tools/session --bin "target/$tier"
    run "$tier-exec" tools/exec-witness "target/$tier/pelt"
    run "$tier-signals" timeout 480 tools/signal-witness "target/$tier/pelt"
    run "$tier-shadow" timeout 300 tools/shadow-witness "target/$tier/pelt"
    run "$tier-colour" timeout 300 tools/colour-witness "target/$tier/pelt"
    run "$tier-words" timeout 300 tools/words-witness "target/$tier/pelt"
    run "$tier-prompt" timeout 300 tools/prompt-witness "target/$tier/pelt"
    run "$tier-terminal" timeout 480 tools/edit-witness "target/$tier/pelt"
    run "$tier-history" timeout 480 tools/hist-witness "target/$tier/pelt"
    run "$tier-reaper" timeout 300 tools/reap-witness "target/$tier"
    run "$tier-glob-rss" tools/glob-rss "target/$tier/pelt"
    run "$tier-loop-rss" tools/loop-rss "target/$tier/pelt"
    run "$tier-shape-rss" timeout 1200 tools/shape-rss "target/$tier/pelt"
done
run words-loader python3 tools/words-loader-test
run diff-harness tools/difftest-selftest target/release
run session-harness tools/session-selftest target/release
find src -name '*.lu' -type f -print0 | sort -z | xargs -0 sha256sum > "$L/sources-after"
run sources-stable cmp "$L/sources-before" "$L/sources-after"
printf 'SH33 full gauntlet: %s failed\n' "$bad"
[ "$bad" -eq 0 ]
