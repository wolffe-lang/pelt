# sh33 — the small fixes

_Materialised from pelt#96's body at the merge (`247b7a4`); the Codex wrapper writes no .md notes._

Fix the PATH-directory diagnostic, in-script noexec, monitor/nolog round trips and floating printf. Preserve every existing expected byte.


This five-section PR body is the lane note: this wrapper prohibits Markdown report files. Materialize it as `notes/sh33-the-small-fixes.md` at merge.

## Prediction

`2845d5b` committed the plan/prediction before measurements or implementation, following contract items 1–8. The lookup/list-boundary/listing/float predictions held. Two measurements corrected the brief: directory-only search in dash 0.5.13.4 reports Permission denied with statuses **127/127/126** for plain/command/exec, not 126 everywhere; dollar-single-quote high bytes at trunk are already refused, not replaced with a question mark.

R-sh33-1 was accepted by orchestration: implement the measured 127/127/126 triple and dash's wording. No new ruling or compiler pin. Noexec guards run before expansions, redirections, definitions and asynchronous starts, and parsing still diagnoses later syntax errors. A while loop whose body enables noexec is left rather than busy-spinning; the raw dash/bash loop-timeout probes are preserved in `notes/sh33/71-oracle-loops.log` (not claimed as passing differentials).

## Forbidden

No shell, libc or other third-party implementation source read; dash/bash only black-box. No expected-byte changes, compiler/std pin change, CI edit, Mac build/test, host package installation, image publication, label, merge, tag, release or issue creation/closure. No attribution trailers. Planning checkout and ~/.claude untouched. All execution used kasumi's rootless container under the CPU8–11 flock; the frozen rig additionally asserts affinity inside the container. Plant branches are draft-only and must never merge.

## Inputs verified

- Base: pelt trunk `1ddebe5`. Unchanged wolf0.2.35/lupin0.1.56/std2386522e; staged whole driver/runtime/interpreter pair copied from the existing matching pin, version/STD-REV checked, driver/runtime/lupin hashes read twice and matching sh32's receipts (`notes/sh33/pin.log`). No source-built compiler.
- Test container base: `docker.io/library/archlinux@sha256:8185e444e45ba166146b244b41f1cba2d7d91f3eddce533a839cc9591e0fa785`. As sh28's rig, it mounts host /usr/package database read-only: measured dash0.5.13.4-1.1, bash5.3.20-2, fish4.9.3-1. This is explicitly NOT the requested reproducible reference-recording image.
- Nine new differential cases were recorded before their fixes; baseline failure output is `notes/sh33/red.log`, with added noexec/float input reds alongside it. Original corpus .out files and every typed-session expectation are unchanged. Only c_floats's pending flag was retired.
- #65: bash emits hex ff for octal/hex dollar-single quotes, pelt exits2 with no stdout and the named UTF-8 refusal. Valid UTF-8 c3a9 passes both. `notes/sh33/65-byte-stop.log`; words and os_spawn_fds/os_exec argv are still List[str]. Stop on this item: W06, pelt#20/#65, wolf-lang#687/#912 remain open.
- #69: exact dash/fish archive filenames and sha256s read twice. The exact bash5.3.20-2 archive is absent from its directory listing and its URL returns HTTP404; only -1 is listed. `notes/sh33/69-archive-stop.log`. Per orchestration's explicit stop, no substitution, package installation, image build/digest, recording reproduction or workflow is claimed. Tools-only recipe/manifest/runner are staged with a fatal UNAVAILABLE preflight. Every dependency, including Python if needed, still needs exact pinning before this becomes operational.

## Evidence index

Commits:
- `125fe34`: #72 denial wording and measured 127/127/126 statuses, later-executable precedence, command-v still refuses directories.
- `cea4149`: #71 nested noexec side-effect gates, four new differential cases plus the old syntax-error case.
- `8794f3a`: #70 monitor/nolog listings, saved nolog bit and frame/fast-state propagation, round-trip differential.
- `b208185`: #73 e/E/f/F/g/G, binary64 decimal parsing/exact half-even output via pinned std.decimal, one-round hexadecimal operand reader, signed zero/NaN/inf, flags/width/precision and g notation AFTER rounding; pure checked/compiled laws and recorded rows.
- `61f2d0e`: #69 blocked reproducible-image preparation and strict immutable-id/version/network/read-only guards.
- `fcf80a7`: #65 byte-boundary stop receipt.
- `ba6c356`: behavior changelog; `7662b25`: README-only counts/behavior refresh.
- `586b76e`: named plant receipts, pin receipt, complete preflight log and frozen two-tier regression helper.
- `247b7a4`: sampled census update and explicit uncovered-%a caveat.

Completed local checks (`notes/sh33/preflight-green.log`, `73-green.log`, `70-green.log`):
- [x] Native/release builds and compiled selfchecks; checked tests1passed,0failed/rejected/unsupported.
- [x] Full native differential corpus **1033 pass / 0 fail / 14 named pending**, total1047; original c_floats now non-pending.
- [x] Release all nine new rows plus original c_floats:10/0/0.
- [x] Independent deterministic339-case float black-box sweep against dash, both native and release:339/0 each; explicit directory diagnostic suffix + status127/127/126 checks pass both.
- [x] Entire44-row option area and round-trip case pass; formatter/clause census green.
- [x] Oracle preparation fails loudly before network/build on missing bash; mutable tags, malformed ids and the wrong base image are refused. `notes/sh33/69-runner.log`.
- [x] Two plants format/build successfully and fail named compiled checks locally; fixes committed first.
- [ ] Frozen full native/release regression, including584 existing typed sessions each, signal/terminal/history/friendly witnesses, all memory shapes, harness selftests and before/after source manifests: detached below, NOT a completed-green claim.
- [ ] Final-head PR-tier green: orchestration watches CI; this lane reads its run list once immediately, never waits or labels.

Draft plants (local reds are the module-lane evidence, no workflow dispatch):
- #94, `acf6648`: set-n-keeps-running, exactly one failed table check. `notes/sh33/plant-noexec.log`.
- #95, `b7b7245`: printf-g-prints-literal and printf-rounding-and-alternate, two failed table checks. `notes/sh33/plant-printf-g.log`.
Each immediate post-creation CI lookup returned []; no subsequent plant-CI polling.

Read-only #83/#57: no performance fix or new measurement claim. shape-rss still compares separate peak-RSS N/2N processes; the issue's shared-runner step and existing RssFile-noise comments remain plausible instrument causes, not a proven leak. Fork child_start still resets traps and calls sig_apply after descriptor/job setup (`src/sh/fork.lu`); sh26 already recommends measuring that disposition loop and closes before optimizing. No cheap measured speed fix is claimed.

Frozen full local job (source head `586b76e`; final head adds documentation only):
- pid1342857, `/home/mfwolffe/lanes/sh33/full-job.pid`
- aggregate `/home/mfwolffe/lanes/sh33/full-job.log`
- completion marker `/home/mfwolffe/lanes/sh33/full-job.exit`
- per-step logs/status/manifests `/home/mfwolffe/lanes/sh33/full-logs/`
- helper `notes/sh33/full-gauntlet.sh`; explicit BEGIN/END and each command's own status, all steps continue after an independent failure. Launch verified by first log line, in-container affinity8–11 and initial formatter/planner/census greens. No polling of the long job by this lane.

## Done-when

Application fixes for orchestration to close on merge: **pelt#72, #71, #70, #73**. Keep **#65/#20** and **#69** open; #83/#57 were read-only. Follow-on issue to file: printf/8's existing census statement includes %a but c_floats samples only e/f/g. The tool mechanically reports533/548 samples passing; %a is still unsupported/uncovered, explicitly documented rather than claimed as full conformance. Add its named pending differential in the next coverage pass.

README read and refreshed; no install/build/default-on claims moved. No CI or pin changed, so Footprint remains module. Final head pushed, PR open, mandatory audit run once, no label/CI wait. Orchestration must review the frozen local job's completion and every per-step status, then merge only on required green. Retain the remote builds/logs until review; only this lane's clean, pushed Mac worktrees and transfer bundle may be pruned. Current lane target72MiB + staged pin363MiB; kasumi /home49GiB free at the last read. The local podman occasionally prints an unrelated stale-container refresh warning; no other container or lane was changed.

Final-head closeout: the immediate push/PR CI read returned `[]`. The mandatory audit, run once afterward, exposed run40438781077 in progress. Its last line was `AUDIT FAIL (footprint: module)`: the only holds were that run still running and no green tier job yet. All ancestry, path-footprint, head-match, five-section, cited-sha and no-attribution checks passed. The three clean, pushed Mac worktrees were removed individually; the audit confirms the lane worktree is gone and no orphan names it. No label, second CI query or wait followed. Audit retained at `/Users/mfwolffe/lanes/sh33/audit.log`, five-section note input `/Users/mfwolffe/lanes/sh33/pr-body.txt`, local evidence copies `/Users/mfwolffe/lanes/sh33/evidence/`. The detached kasumi full-job handoff above remains pending; no full-gauntlet green is claimed.

