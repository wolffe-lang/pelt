#!/bin/bash
# Run via ctr.sh; that wrapper holds CPUs12-15's flock for this whole job.
set -u -o pipefail
ulimit -c 0
tier=${1:?native or release}
case "$tier" in native|release) ;; *) exit 2;; esac
root=$(pwd)
logs=$root/notes/sh28-evidence/logs
status=$logs/final-$tier.status
: > "$status"
bad=0
run() {
    name=$1; shift
    printf 'BEGIN %s %s\n' "$name" "$(date -Iseconds)"
    if "$@" > "$logs/final-$tier-$name.log" 2>&1; then rc=0; else rc=$?; fi
    printf '%s %s\n' "$name" "$rc" >> "$status"
    tail -3 "$logs/final-$tier-$name.log"
    printf 'END %s status=%s %s\n' "$name" "$rc" "$(date -Iseconds)"
    if [ "$rc" -ne 0 ]; then bad=$((bad+1)); fi
}
git rev-parse HEAD > "$logs/final-$tier.head"
find src -name '*.lu' -type f -print0 | sort -z | xargs -0 sha256sum > "$logs/final-$tier.sources-before"
run build tools/build "--$tier"
run fmt tools/check-fmt
run selfcheck tools/self-check "$tier"
if [ "$tier" = native ]; then run checked-tests tools/check-test; fi
run corpus tools/difftest --bin "target/$tier"
run sessions tools/session --bin "target/$tier"
run terminal tools/edit-witness "target/$tier/pelt"
run history tools/hist-witness "target/$tier/pelt"
run friendly python3 -I -u notes/sh28-evidence/witness.py "target/$tier/pelt"
find src -name '*.lu' -type f -print0 | sort -z | xargs -0 sha256sum > "$logs/final-$tier.sources-after"
run sources-stable cmp "$logs/final-$tier.sources-before" "$logs/final-$tier.sources-after"
printf 'GAUNTLET %s: %s failed\n' "$tier" "$bad"
if [ "$bad" -ne 0 ]; then exit 1; fi
