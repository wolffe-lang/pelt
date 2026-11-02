#!/usr/bin/env bash
# Continue f423b34 after its green signal-native step, under CI-like uid 1000.
set -eu
[ "$(id -u)" = 1000 ]
[ "$(id -g)" = 1000 ]
[ "$(git rev-parse HEAD)" = f423b342041b9debba3e5222ad4347a19b18979f ]
[ -z "$(git status --porcelain --untracked-files=no)" ]
echo "NONROOT_UID=$(id -u) GID=$(id -g)"
grep -E '^(CapEff|Cpus_allowed_list):' /proc/self/status
printf '%s\n' \
 '7f6b316498091106e52901f5bc0f822278d981890c826515da77b48ed0817dd3  target/native/pelt' \
 '2e104b256d371faf634b004d43606eeb8940ff3c56b2f70997cc41036625a019  target/release/pelt' | sha256sum -c -
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
# Repeat the sampler cheaply under the corrected identity, then continue
# at the first stopped step. Do not alter/skip any differential row.
step sampler-native-nonroot env PELT_TEST_SHELL=/work/target/native/pelt python3 tools/shape-rss-test
step differential-native tools/difftest --bin target/native
step sessions-native tools/session --bin target/native
for witness in shadow colour words prompt edit hist; do
    step "$witness-native" "tools/$witness-witness" target/native/pelt
done
step words-loader-native python3 tools/words-loader-test
step reap-native tools/reap-witness target/native

step sampler-release env PELT_TEST_SHELL=/work/target/release/pelt python3 tools/shape-rss-test
step self-check-release tools/self-check release
step glob-rss-release tools/glob-rss target/release/pelt
step loop-rss-release tools/loop-rss target/release/pelt
step shape-rss-release tools/shape-rss target/release/pelt
step exec-release tools/exec-witness target/release/pelt
step signal-release tools/signal-witness target/release/pelt
step differential-release tools/difftest --bin target/release
step sessions-release tools/session --bin target/release
for witness in shadow colour words prompt edit hist; do
    step "$witness-release" "tools/$witness-witness" target/release/pelt
done
step words-loader-release python3 tools/words-loader-test
step reap-release tools/reap-witness target/release
step differential-plant tools/difftest-selftest target/release
step session-plant tools/session-selftest target/release
step proof-under-load python3 notes/sh35-evidence/rig.py proof target/native/pelt /lane/nonroot-proof-records
[ -z "$(git status --porcelain --untracked-files=no)" ]
