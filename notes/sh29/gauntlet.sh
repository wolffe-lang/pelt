#!/bin/bash
# Run through ctr.sh, holding CPUs4-7's flock for the complete pair.
set -u -o pipefail
root=$(pwd)
logs=$root/notes/sh29/logs
mkdir -p "$logs"
: > "$logs/final.status"
bad=0
run() {
    local name=$1
    shift
    printf 'BEGIN %s %s\n' "$name" "$(date -Iseconds)"
    if "$@" > "$logs/final-$name.log" 2>&1; then rc=0; else rc=$?; fi
    printf '%s %s\n' "$name" "$rc" >> "$logs/final.status"
    tail -3 "$logs/final-$name.log"
    printf 'END %s status=%s %s\n' "$name" "$rc" "$(date -Iseconds)"
    if [ "$rc" -ne 0 ]; then bad=$((bad+1)); fi
}
git rev-parse HEAD > "$logs/final.head"
git ls-files -z src tools tests .github | sort -z | xargs -0 sha256sum > "$logs/final.inputs-before"
run build tools/build --all
run fmt tools/check-fmt
run checked-tests tools/check-test
run ci-planner python3 ci/tiers-test.py
for tier in native release; do
    run "$tier-selfcheck" tools/self-check "$tier"
    run "$tier-corpus" tools/difftest --bin "target/$tier"
    run "$tier-sessions" tools/session --bin "target/$tier"
    run "$tier-shadow" tools/shadow-witness "target/$tier/pelt"
    run "$tier-terminal" tools/edit-witness "target/$tier/pelt"
    run "$tier-history" tools/hist-witness "target/$tier/pelt"
done
git ls-files -z src tools tests .github | sort -z | xargs -0 sha256sum > "$logs/final.inputs-after"
run inputs-stable cmp "$logs/final.inputs-before" "$logs/final.inputs-after"
printf 'GAUNTLET: %s failed\n' "$bad"
if [ "$bad" -ne 0 ]; then exit 1; fi
