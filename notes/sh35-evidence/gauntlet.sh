#!/usr/bin/env bash
# Run only in the four-CPU, 12 GiB lane container, from a pinned archive.
set -eu
step() {
    local name=$1
    shift
    echo "BEGIN $name $(date -u)"
    set +e
    "$@"
    local code=$?
    set -e
    echo "END $name exit=$code"
    return "$code"
}
step toolchain tools/fetch-toolchain
step planner python3 ci/tiers-test.py
step proof-rig-contracts python3 tools/shape-rss-rig-test
step fmt tools/check-fmt
step clauses tools/clause-census
step build tools/build --all
step wolf-tests tools/check-test
trace_root=${SH35_TRACE_CONTRACT_ROOT:-target/trace-contracts}
for tier in native release; do
    shell="target/$tier/pelt"
    step "sampler-$tier" env PELT_TEST_SHELL="$shell" PELT_SHAPE_TEST_TRACES="$trace_root/$tier" python3 tools/shape-rss-test
    step "self-check-$tier" tools/self-check "$tier"
    step "glob-rss-$tier" tools/glob-rss "$shell"
    step "loop-rss-$tier" tools/loop-rss "$shell"
    step "shape-rss-$tier" tools/shape-rss "$shell"
    step "exec-$tier" tools/exec-witness "$shell"
    step "signal-$tier" tools/signal-witness "$shell"
    step "differential-$tier" tools/difftest --bin "target/$tier"
    step "sessions-$tier" tools/session --bin "target/$tier"
    for witness in shadow colour words prompt edit hist; do
        step "$witness-$tier" "tools/$witness-witness" "$shell"
    done
    step "words-loader-$tier" python3 tools/words-loader-test
    step "reap-$tier" tools/reap-witness "target/$tier"
done
step differential-plant tools/difftest-selftest target/release
step session-plant tools/session-selftest target/release
# The NEW 200-run proof is a separate ledger of <=16-run, <=2 h chunks.
# A green ordinary gauntlet is not the proof; require every chunk record too.
echo 'GAUNTLET_COMPLETE proof_chunks_required=200'
