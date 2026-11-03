# sh35 — shape-rss: the shape memory read twice inside one shell

The lane's report, from PR #105 (merged at `877a2c36`, 2026-11-03): pelt#104, the instrumented 200-run proof, and the unexplained run-89 red filed as pelt#110 (a rate bound, not a fix).

Footprint: cross-cutting

Refs #104 and #110. One-process measurement is implemented and the instrumented 200-run proof is green. The old run-89 prompt loss remains unexplained and is **not claimed fixed**. No closing keyword is intended for either issue.

## Prediction

Compare N and 2N turns in one shell process, not two unrelated processes. On Linux the shell reads its own `/proc/self/smaps_rollup` Anonymous + Swap; on macOS it pauses while the harness samples the same PID. Preserve all 52 shapes, turn counts, predicates, row overrides and slack. Require zero reds in 200 new whole-tool runs under four-CPU load, plus retained-buffer negative controls. Predictions preceded the implementation and the resumed corrections.

## Forbidden

No other shell implementation source read; only specifications, black-box output and this project's own code. No shell/runtime/compiler-pin changes, relaxed bounds, attribution trailers, packages, unrelated data, process-group kills, labels, merges, tags or issue closures. Cleanup targets owned descendant PIDs. Final recording used only kasumi 4–7, non-root, under a 12 GiB memory cap and a container lifetime below two hours per lock take. Other slots were untouched.

## Inputs verified

- Base `7908f94d2d1bffd61a1915740a7c021b6380fa37`; final PR head `877a2c36399d929b33ce1a76b63d6fd7c3e6bc50`.
- Proof tool head `ce8168dc2a3b94114e0411a31cea49e50d8b9b3c`. `git diff --stat ce8168d..877a2c3` lists **only `tools/shape-rss-test`**, 87 insertions/14 deletions. Tool, sampler, trace library, cleanup library and measured shell are unchanged between proof and final head.
- Final full CI **41633188828 is green at `877a2c3`**: https://github.com/wolffe-lang/pelt/actions/runs/41633188828 . Its watch is separate from these local records.
- Fresh final-head recorder checkout: `/home/mfwolffe/lanes/sh35/final-record-green-877a2c3`; pinned toolchain revalidated, both native/release binaries rebuilt from the commit, UID 1000 with keep-id, taskset 4–7. Raw step output is indented two spaces so a binary's `SKIP:` is not a recorder directive. The only unindented plant failure is the recorder's explicit witness, emitted after validating the actual row's exit, answer and memory delta.
- Plant branch **`sh35-record-plant`**, pushed **without a PR**, head `753dc41c58fb546f7acd9ea4c5f8abbe23c825e0`, parent exactly `877a2c36399d929b33ce1a76b63d6fd7c3e6bc50`. One commit, one file (`tools/shape-rss`), one hunk: baseline retains a fresh 1 KiB value under each distinct counter name. The independent preflight proves three earlier values each have 1024 bytes. It uses the SAME final-head built pelt binary and unchanged default N=10000, 100 B/turn + 1024 KiB allowance.

## Evidence index

### Final-head green recorder record

Remote `/home/mfwolffe/lanes/sh35/final-green-877a2c3.record.log`; local `/Users/mfwolffe/lanes/sh35/final-green-877a2c3.record.log`. The org recorder's verifier checks the head/tree, timestamps and every step result; both records were independently reverified together after copying locally. Header and footer:
```
RECORD repo=pelt head=877a2c36399d929b33ce1a76b63d6fd7c3e6bc50 tree=3079145d21fc4aff0b57501c0a9dc8b5a0c29e31 host=c01d99441d79 boot=db705914-53d6-4a8f-a7e1-6d768fd5271d start=2026-11-03T20:32:38Z
RECORD-END worst=0 steps=44 end=2026-11-03T21:28:21Z
```
Every END line:
```
END toolchain exit=0 secs=0
END planner exit=0 secs=3
END proof-rig-contracts exit=0 secs=0
END fmt exit=0 secs=0
END clauses exit=0 secs=0
END build exit=0 secs=49
END wolf-tests exit=0 secs=1
END sampler-native exit=0 secs=13
END self-check-native exit=0 secs=5
END glob-rss-native exit=0 secs=0
END loop-rss-native exit=0 secs=1
END shape-rss-native exit=0 secs=187
END exec-native exit=0 secs=0
END signal-native exit=0 secs=2
END differential-native exit=0 secs=30
END sessions-native exit=0 secs=1250
END shadow-native exit=0 secs=12
END colour-native exit=0 secs=16
END words-native exit=0 secs=19
END prompt-native exit=0 secs=53
END edit-native exit=0 secs=25
END hist-native exit=0 secs=5
END words-loader-native exit=0 secs=0
END reap-native exit=0 secs=21
END sampler-release exit=0 secs=13
END self-check-release exit=0 secs=61
END glob-rss-release exit=0 secs=1
END loop-rss-release exit=0 secs=0
END shape-rss-release exit=0 secs=137
END exec-release exit=0 secs=0
END signal-release exit=0 secs=2
END differential-release exit=0 secs=25
END sessions-release exit=0 secs=1245
END shadow-release exit=0 secs=12
END colour-release exit=0 secs=15
END words-release exit=0 secs=20
END prompt-release exit=0 secs=52
END edit-release exit=0 secs=26
END hist-release exit=0 secs=5
END words-loader-release exit=0 secs=0
END reap-release exit=0 secs=21
END differential-plant exit=0 secs=0
END session-plant exit=0 secs=16
END proof-ledger-200 exit=0 secs=0
```

### Current one-break plant recorder record

Remote `/home/mfwolffe/lanes/sh35/final-plant-753dc41.record.log`; local `/Users/mfwolffe/lanes/sh35/final-plant-753dc41.record.log`. `--base 877a2c36399d929b33ce1a76b63d6fd7c3e6bc50 --plant baseline`. The expected recorder exit is 1, not a green substitute. Literal witness and every END line:
```
FAIL baseline memory retained-buffer grew=24388KiB limit=2000KiB shell_answer_valid=yes
END retained-payload exit=0 secs=0
END baseline-memory exit=1 secs=10
END record-wrapper exit=1 secs=0
RECORD-END worst=1 steps=3 end=2026-11-03T21:29:32Z
```
The preflight is green; the baseline failure is **memory-only**, with valid shell answer, not a timeout or malformed sampler result. No plant PR was opened. The older draft plant PR is not used as this record.

### New instrumented whole-tool proof: 200/200, zero reds

Ledger `/home/mfwolffe/lanes/sh35/instrumented-ce8168d-20261103T110757Z-ledger.json`; local `/Users/mfwolffe/lanes/sh35/final-proof-evidence/instrumented-ledger.json`. All 200 unique global run IDs, 52 rows per run, summaries and exit markers were verified. Thirteen independently named chunks (12×16 + 8); four workers plus four original own-slot load processes, alive through every chunk. Maximum chunk runtime **2785.41 s (46.43 min)**, every container capped at 6600 s and every controller at 6000 s; lock released between chunks. Ordinary external pool activity was left alone. No red or interrupted run was silently retried or credited.

Every chunk END and the driver terminal lines:
```
END proof-chunk-1-16 exit=0
END proof-chunk-17-32 exit=0
END proof-chunk-33-48 exit=0
END proof-chunk-49-64 exit=0
END proof-chunk-65-80 exit=0
END proof-chunk-81-96 exit=0
END proof-chunk-97-112 exit=0
END proof-chunk-113-128 exit=0
END proof-chunk-129-144 exit=0
END proof-chunk-145-160 exit=0
END proof-chunk-161-176 exit=0
END proof-chunk-177-192 exit=0
END proof-chunk-193-200 exit=0
LEDGER_COMMITTED completed=200 red=0
END instrumented-proof-200 exit=0
SH35_INSTRUMENTED_PROOF_DRIVER_COMPLETE exit=0
```
Per-range artifacts: same prefix plus `-proof-NNN-NNN.log`, `.exit` and `-records/proof-summary.json`. Driver `/home/mfwolffe/lanes/sh35/instrumented-ce8168d-20261103T110757Z-driver.log`/`-driver.exit` (0).

### Unexplained original prompt loss: #110, not fixed

Old proof at `f423b34`: **128 completed = 127 green + run 89 red**, plus four interrupted later attempts. Run 89 completed exit 1 with all 52 rows; `typed-fork-subshell` reported `no prompt after line 10962`. Its -1/-1 samples are invalid sentinels, not zero growth. The failure preceded the host reset. Original log `/home/mfwolffe/lanes/sh35/proof-requeue-8-11-20261103T015853Z-records/proof-089.log`; durable copy `/Users/mfwolffe/lanes/sh35/final-proof-evidence/proof-089.log`. No later run was used to continue that defeated proof.

Issue **#110** preserves the original evidence, instrumented ledger, hypotheses and bound. **0/200 licenses a rate bound, not a fix:** under independent, constant-probability Bernoulli trials, the one-sided 95% upper bound is `1 - 0.05^(1/200) = 1.4867%` **per instrumented whole-tool invocation**, not per turn. Shared pool conditions may correlate runs, so those assumptions are not established; without them the observation is simply 0/200. It does not bound the uninstrumented rig or establish zero risk.

Instrumentation **could mask a timing failure**: per-IO timing calls, event copying, exit checks and between-row observation overhead perturb interleavings. Published failure snapshots are taken only after a failure verdict and cannot rescue that missing prompt, but earlier observation overhead can prevent the original timing from occurring. There is no causal fix or minimised reproducer; #110 remains open.

### Negative controls, portability and retained history

- Completed trunk baseline: **50 whole-tool attempts**, original base `7908f94d`; all tools red with the legacy separate-process RSS instrument. Full 52-row ranges/counts: `/home/mfwolffe/lanes/sh35/baseline-summary-final.jsonl` (hasu), local `/Users/mfwolffe/lanes/sh35/baseline-summary-final.jsonl`. Script-background-wait 21–169 B/turn, jobs-set-m 158–166 B/turn, neither memory-red in 50. Typed-fork-subshell had 48 numeric readings and **two prompt failures** (runs 45/46), excluded from numeric ranges rather than retried. Legacy typed RSS reds are not automatically called noise because the metric differs.
- Corrected all-shape buffer plant `2ae12d1`: **52/52 memory-red, no wrong-answer rows**, aggregate exit 0, `/home/mfwolffe/lanes/sh35/corrected-plant-records/plant-summary.json`. Earlier plant `5f571b6` accidentally retained empty entries; committed invariant `ed2a61f` was red with `0 0 0`, then the braced counter correction was green with `1025 1025 1025` and preserved prior values. Empty-entry results are not credited as buffer evidence.
- Strict expected-notice validation accepts only the observed successful 38-byte `true` job notice and exact 2N count; all other stderr still fails. Two original loops inside one complete command replace the per-turn checkpoint branch that itself added about 32 B/turn. The six-job retention E2E proves the midpoint does not clear jobs. Memory predicates and bounds never widened.
- Trace implementation `1827ef2`, red-first hang/exit tests `05dc002`: real planted hangs still fail at the unchanged 10 s deadline and preserve the living process/child before cleanup. EOF and process exit are distinguished from deadline expiry.
- Test-only timing regression `1cbfd0d` was red on both hosts with hosted macOS total **28.0649 s** versus the old 25 s enclosing-test budget. `877a2c3` keeps Linux at 25 s and gives Darwin 40 s (about 12 s/42% margin), with measured reasons in the comment. Mac green: **22 tests, two Linux-only skips**, real E2E/hang/exit executed; Linux green: **22 tests, no skips**. Phase timings persist in `hang-timing.json` and every hang assertion message. This does not alter the row deadline.
- Historical operational errors remain recorded: a hasu baseline was observed holding the inner lock without the outer name, blocking another holder about 100 min; retained command text is not a live ownership receipt. The old reboot-cut proof held kasumi 8–11 about 6 h 2 min, beyond the two-hour limit. New proof/record launchers use independent capped lock takes. Root permission tests were wrong for the non-root oracle: identical binary root 0/3 versus UID1000 3/3; the environment was corrected, not the cases.

## Done-when

- [x] Same-process checkpoints, all 52 rows/counts/predicates/bounds preserved; malformed/missing samples fail closed.
- [x] Fifty original baseline attempts, actual payload negative controls, all 52 corrected retained-buffer plants red.
- [x] Real Mac and Linux E2E plus red-first timing/notice/checkpoint/retention/cleanup/controller contracts.
- [x] New complete 200-run instrumented proof, every chunk independently green and below the lock cap.
- [x] Final-head full CI green; final-head green recorder record and current one-break plant record verified.
- [x] Unexplained original functional red filed as #110 with limitations, not claimed fixed.
- [ ] Final lane audit and any merge decision are separate; no audit, merge or issue closure performed by this lane at this handoff.

### Named follow-ons

- **#110 — unexplained typed-fork-subshell prompt loss.** Capture a recurrence or establish a causal explanation; 0/200 under instrumentation is not a fix.
- **Test library — Darwin descendant cleanup.** `tools/lib_reap.py:end_tree` may scan `ps` up to 200 times. Measured local cleanup **8.165–8.437 s**, Linux **.0203–.0204 s**; Mac snapshots only **.021–.028 s**. Hosted Mac total was **28.065 s**, without its old phase split. Investigate a cheaper bounded descendant-table strategy separately. Not changed under this proof.

