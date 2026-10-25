Add the opt-in friendly left prompt, bounded right-prompt display and den porcelain cache. Preserve explicit PS1 and all old expectations.

Footprint: cross-cutting

# Note

The wrapper cannot write a Markdown lane report. Materialize this Note as `notes/sh32-the-prompt.md` at merge. Evidence and the sh33 draft are tracked under `notes/sh32/`.

## Prediction

`0f588f6` committed the prediction before implementation or measurement: at80/200 columns, visible `mfwolffe@sh32 ~> `, shortened `~/a/b/gamma`, `[1]` on failure, root `#`, green user/host and blue path; right-prompt release median delta below0.10ms with median and p99 below1ms; deadline plant hardest.

Measured fish4.9.3 in fresh-HOME owned ptys at24/40/80/200 columns, both uid1000 and container root. Path/status/root predictions held. Host was the container's generated hostname, not `sh32`; no-config foreground was default/reset, not green/blue; status digit was bold. Unicode path `~/a/b/日本語` stayed intact. Raw input/output hex and screens are in `notes/sh32/oracle/`.

Release visible-right median0.406661ms/p990.577726ms; no-right0.318649ms/0.501811ms; median delta+0.088012ms: predicted bar met.80-character input with overlap hiding the right prompt:0.055718ms/0.267165ms. All strict median/p99<1ms. Deadline was not harder: every plant failed exactly one named selfcheck.

Implemented recommendations, not rulings:
- R-sh32-1 A: measured fish-shaped visible prompt, pelt-owned reset protocol.
- R-sh32-2 A: explicit PS1 wins, including empty/default-valued assignments; later unset stays ordinary-empty. Existing POSIX expansions remain; subshell assignments roll back.
- R-sh32-3 A: right display<=columns/3, ellipsis, hidden below40, on overlap/wrap/pager/shadow; clear before execution/EOF/resize.
- R-sh32-4 A: one direct den status per primary prompt,50ms/32KiB collection; stale same-directory value dimmed, directory change invalidates; no idle work.
- R-sh32-5: prompt_right uses ordinary command-substitution isolation once per primary prompt. Its display is bounded/control-escaped; arbitrary user-function runtime and capture memory are NOT bounded by the den deadline. Documented, no stronger claim.
- R-sh32-6: USER/LOGNAME display identity; HOSTNAME or one bounded hostname invocation, then `?`; root marker reads effective uid.
- R-sh32-7: list prompt_friendly only without explicit PS1, preserving immutable explicit-PS1 option transcripts.

## Forbidden

No shell, line-editor, git or libgit2 implementation source read. Fish was run only black-box. No pin/default-on change, old expectation modification, PAX build, Mac build/test, label, merge, release, tag, issue filing or closure. No attribution trailers. Planning repository and ~/.claude untouched. All execution used hasu blockA cores0–5 under its flock, taskset inside rootless podman,12GiB cap. New interrupt witnesses use pty0x03. No maintainer data or servers touched.

## Inputs verified

- Base `0b5eaa5394667c485de3a134f771c87024b68a3c`; preceding labelled run40213526418 read success at0a7a0f668c9cfc31ceb7bdcdba6235e354a272e4. Preceding final full regression is recorded green in sh31's note.
- Unchanged wolf0.2.35/lupin0.1.56/std2386522e. Published Linux archive digests read twice; archives and staged driver/runtime/lupin hashed twice. `notes/sh32/logs/pin-digests.log`.
- Oracle image rebuilt from sh31 with diffutils, pinned to blockA. Fish reports4.9.3. Actual den trunkfd42d7fff07cb0bd84a4839835edd6c7af6a8574 built and run: `den init`, create untracked file, `den status --porcelain` => `?? untracked`, exit0. Thus real den integration, not a no-provider stub. Outside-repository exit1 also recorded.
-32 new independently asserted typed sessions make584. All1038 corpus cases and552 older session expectations, the pin and exact PAX framebuffer/serial pending rows are unchanged. No PAX result claimed.
- Prompt bit16777216; explicit-PS1 frame bit33554432. Help probes never feed prompt data. Prompt text/styles never enter Ed.buf/history/undo/kills.

## Evidence index

Commits:
- `ce95efe`: left/right prompt data and renderer with pure laws.
- `83e7e78`: raw-byte, storage, idle/cost witness.
- `ec62583`: bounded executable VCS probe and frame-isolation fixes/tests.
- `845fb4f`:32 typed sessions, independently asserted stdout before screen pinning.
- `16ed74a`: CI/planner gate on every built tier.
- `145b765`: feature/key/changelog documentation.
- `4bb50cf`: README-only feature/count refresh.
- `5863d1a`: oracle, measurements, named plants, follow-on and frozen full-run script.

Completed at the reviewed application sources (`notes/sh32/logs/prompt-reviewed.log`, `native-regression.log`):
- [x] Native/release builds and compiled selfchecks.
- [x] Checked tests1passed,0failed/rejected/unsupported.
- [x] New native sessions32/0/0; release32/0/0 before the final frame/EOF review, rerun in the frozen full job.
- [x] Raw resets/cursor/storage/history, PS1 environment/assignment/empty/default/subshell, right hook isolation/one-call, width/wrap/resize/pagers/controls, POSIX/script/pipe/dumb gates.
- [x] Executable VCS fixture: timely dirty/clean, deadline, invalidUTF-8, changed directory, zero per-key probes; deterministic boundary selfcheck.
- [x] Strict release visible-right and80-character cost bars.10s idle context switches/CPU/fault/RSS unchanged; right RSS9280→9280kB, no-right8628→8628kB; child-only THP disabled.
- [x] Native cost: visible-right0.458452ms/p990.595958ms; no-right0.369569ms/0.527489ms;80-character0.174984ms/0.578579ms. Idle unchanged.
- [x] Native full differential corpus1023pass/0fail/15existing pending; formatter/planner and immutable-input diffs green.
- [x] Each plant formatter green and native selfcheck exactly one intended named RED.
- [ ] Frozen full old-session/terminal/history regression completed.
- [ ] Final-head PR-tier green, orchestrator label and full-tier green; all plant CI named reds confirmed.

Plants, draft and never merge; fixes committed first:
- #89 `5ea33edb197244f10ca7adff4dc4e91b985513ad`: `prompt-PS1-precedence` (explicit PS1 replaced).
- #90 `857e1b1ed939fc5060bed6cc96c796b86fbfbe48`: `prompt-right-storage` (ESC appended to Ed.buf).
- #91 `167a79c1e2c562f03bde4d098ec2e4c82fdbeaee`: `prompt-vcs-deadline` (late result accepted fresh).
Each branch's run list was read once immediately after push/draft creation and returned `[]`. No run id returned; no later lookup/poll. Orchestration must retrieve eventual ids and confirm those named reds, not a build/format failure. Local logs preserved in `notes/sh32/logs/plant-*.log`.

Frozen full hasu job survived nomad's reboot; do not relaunch:
- Head `5863d1a30c46269a22ef35ff20b09a16dfde5e3e`, pid45797.
- `/home/mfwolffe/lanes/sh32/final-job.pid`
- `/home/mfwolffe/lanes/sh32/final-job.log`
- `/home/mfwolffe/lanes/sh32/final-job.exit` (created on completion).
- Per-step status/logs and before/after source manifests under `/home/mfwolffe/lanes/sh32/pelt/notes/sh32/logs/`.
Recovery read: through native corpus green; native sessions running. This is not a completed-full verdict. The long job is handed back rather than waited on.

## Done-when

Open at final head; no label or CI wait by this lane. Orchestration watches the frozen local job, confirms named plant reds, labels the final head and merges only on required greens, then materializes this Note. README read and refreshed. `notes/sh32/follow-on.txt` drafts sh33: pin-lane argv[0]/default-on coordination, px-owned session slot, custom-hook budget follow-up, den extension only after measurement. `issues-to-file.txt` lists limitations, not hidden regressions; no issue filed/closed. `prune-list.txt` lists only lane-owned paths: three plant target/cache trees pruned;738MiB lane footprint, final evidence/builds retained through review. Audit status and the immediate final run read are in the handback.

Final-head audit (run once from the org directory): `AUDIT FAIL (footprint: cross-cutting)`. Holds only: run40230964381 still in progress, no green tier job yet, missing orchestrator-owned full-matrix label. All other audit checks passed, including five sections, ancestry, head match and no attribution. The immediate final push/PR run-list read returned `[]`; the mandatory audit subsequently exposed run40230964381. No CI poll or wait followed.


## sh32b — symlinked HOME

- Red: full run40231129755, `gauntlet (macos-latest, true, native)`, `prompt-home` at24 columns. The original raw-byte assertions and temporary-HOME spelling remain unchanged.
- Measured cause: with HOME=`/var/folders/9b/_fvnxkt53q38gcg63wtp3w9r0000gn/T/sh32b-path-euq4bo8q`, both `pwd` and `pwd -P` returned `/private/var/folders/9b/_fvnxkt53q38gcg63wtp3w9r0000gn/T/sh32b-path-euq4bo8q`. This no-build Mac probe used the existing sh31 binary's unchanged startup-PWD logic; the exact sh32 prompt red is preserved from CI. The witness supplies no inherited PWD, so startup correctly chooses the physical cwd; literal-only HOME folding was wrong.
- Recommend and implement **R-sh32b-1 A**, not a ruling: prefer logical PWD, fold against HOME as given or `fs_realpath(HOME)`, then try the shell's physical cwd. Resolve once per primary prompt, never per key. Preserve HOME, PWD and `cd`/`pwd -L`; retain logical paths through symlinks pointing outside HOME. B (normalising only the witness) is not implemented.
- `0e07019`: new native `prompt-symlink-HOME` law is RED against the existing sh32 Linux binary, GREEN after `8de2818`; includes physical startup, Unicode descendant, logical symlink-out preference, another alias, inherited logical PWD, trailing slash, sibling boundary, missing/unset HOME. Eleven pure path laws pass checked and compiled. `8670643` preserves evidence in `notes/sh32b/`.
- [x] hasu fmt, native build/selfcheck, checked tests1/0/0/0, full prompt witness including idle and cost. Linux execution moved, by orchestration, from occupied blockB to CPUs12–15 without flock; wl69's server was untouched.
- [x] Exactly one Mac native build and one full `tools/prompt-witness` invocation: new regression and original24/39/40/80/200-column assertions all GREEN. No Mac soak or unrelated test suite. Pin and old corpus/session expectations unchanged.
- [ ] Remaining native Linux gauntlet, one detached job on CPUs12–15: pid3599544, `/home/mfwolffe/lanes/sh32b/job.log`, completion `/home/mfwolffe/lanes/sh32b/job.exit`; per-step status and logs `/home/mfwolffe/lanes/sh32b/pelt/.cache/sh32b-gauntlet/`. Started at application head `8de2818`; final head only adds evidence. The first immutable-input check could not see shared-clone objects inside the container (exit128); objects were materialised locally and that exact check rerun GREEN (`old-expectations-recheck.log`). Its initial failure remains in the job's final count; do not mistake that for a source/test failure or call the whole gauntlet green before reviewing every remaining row.
- Final head `8670643a6cdd65b967f0ea303b5aff3d88faf82a`, plain fast-forward push to `sh32`; immediate run-list read returned `[]` (no row yet). No label or CI wait. Local branch is `sh32b` because the old clean sh32 worktree still owns `sh32`, left untouched as requested.
- Prune list: remove only the clean, pushed Mac `/Users/mfwolffe/lanes/sh32b/pelt` worktree; retain `/Users/mfwolffe/lanes/sh32b/logs/` and the running hasu `/home/mfwolffe/lanes/sh32b/` job/evidence until review. No other lane tree touched.

sh32b mandatory audit (once at the final head): `AUDIT FAIL (footprint: cross-cutting)`. It found run40241633095 in progress and no completed green tier; full-matrix label, head, ancestry, five sections, cited commits and no-attribution checks passed. It also held the still-present worktree, which was then removed cleanly without force. The two lane-owned local transfer bundles were pruned too. No CI polling followed the audit.

