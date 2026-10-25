# sh31 — Add abbreviations described completion and history events

Materialised from pelt#88 (head 0a7a0f66, merged 2026-10-25) at the merge.

Footprint: cross-cutting

## Forbidden

No shell or line-editor implementation source read. Fish and bash were
measured only through fresh-HOME owned ptys. No Mac git config, PAX build, label, merge, tag, release, or issue filing.
The compatibility follow-up built/tested native on nomad under the
RULES4 memory guard, as requested; the original feature pass built on hasu. Hasu uses block B,
cores 6–11 under its flock, rootless containers limited to 12 GB. Signal
input witnesses use pty bytes. The five sections here are the lane note,
for materialization as `notes/sh31-the-words.md` at merge.

## Inputs verified

- Base `a274d13`; rebased over the notes-only `98b675a`, no code from trunk.
- Unchanged wolf 0.2.35 / lupin 0.1.56 / std `2386522e`. Release digest
  fields read twice; archives independently hashed twice; staged wolf,
  runtime archive and lupin matched their archive bytes twice.
- Fish 4.9.3-1, bash 5.3.20-1, dash 0.5.13.4-1; image rebuilt from sh30's
  Containerfile with diffutils present. No corpus expectation re-recorded.
- All 1,038 corpus cases and 488 original session expectations unchanged.
  64 new independently asserted typed sessions make 552 recorded sessions.
- px70/pax#162's palette/cell basis retained; the exact framebuffer and
  serial pending input rows are unchanged. No PAX result claimed.

## Prediction

`a1dec49` recorded the prediction before measurement. Fish expands an
abbreviation on both Space and Enter, as predicted. Six described choices
used **three columns at 80/120**, one at 24/40, not the guessed two at 80.
64 sessions, not the guessed 70. Post-integration release key latency at
`5497d4c` was below the required 1 ms; final-head measurements are pending.

Implemented recommendations, not maintainer rulings:
- R-sh31-1 A: bounded non-executable `name<TAB>replacement` records,
  private exclusive temporary file and atomic rename; malformed rows ignored.
- R-sh31-2 amended after measurement with orchestrator concurrence:
  **Space and Enter**, whole unquoted command word, including command
  position after separators. Quoted spellings and arguments remain literal.
- R-sh31-3: measured Tab/backtab/arrows/Enter/Escape navigation.
- R-sh31-4 A: own error and original line left for editing, unlike bash's
  measured fresh prompt after a failed event reference.
- R-sh31-5 A / R-sh31-6 A: last shell word as spelled; expanded accepted
  text echoed and recorded in history, not written into editable storage.
- R-sh31-7, orchestrator concurred: adaptive columns, at most five rows;
  marker-only selection until Enter, Enter accepts without executing.
- R-sh31-8: `abbr` and `complete` option names; help probes only on explicit
  option Tab, per-prompt bounded cache, never during highlighting or idle.

Fish's commandline snapshot includes a candidate during navigation; pelt
intentionally does not mutate Ed.buf until acceptance. `--help` probing
is actual external-command execution and can have that program's effects;
this is distinct from no-execute-on-highlight/selection. The collection
budget is 50 ms; OS startup/scheduling/cleanup can add wall time. Opt-in
stays; the pin lane owns argv[0]/default-on policy.

## Evidence index

Marker-lifecycle follow-up at `0a7a0f6`:
- Run **40209085844**, Mac native job **121216424171**, failed reading
  `slow-probes` after warm-up had unlinked it. The old complete timing race
  did not fail in a local full run, but the extracted old warm-up and new
  lifecycle regression reproduced the exact FileNotFoundError under
  nomad's real `/var/folders/.../T/` TMPDIR before the fix.
- Warm-up now retains zero-length counters. The slow helper writes its
  entry counter in the warmed shell before `exec` of the delaying Python;
  this preserves one owned pid and avoids a sleeping descendant. Cache
  assertions still require exactly one start, never a missing/empty pass.
- Regression GREEN; full Mac native words witness GREEN under the8GiB
  memory guard, actual Mac TMPDIR; eight extra help/cache/timeout repetitions
  GREEN8/8. Mac median0.111333ms/p990.227708ms; Linux idle accounting is an
  explicit Mac SKIP. CI planner GREEN.
- Linux native/release updated words witnesses GREEN; strict release
  median0.160571ms/p990.322963ms, idle10s counters unchanged.
- Application source,50ms budget, corpus and552 session expectations are
  unchanged. Evidence: `notes/sh31/macos-marker-fix.txt` and indexed logs.
- The new head's run list was read once immediately after push and was
  empty; no run ID was available on that read. No CI wait or label change.


Compatibility follow-up at `b9af8a8`:
- Run **40187287608**, macOS native job **121150715227**, failed before
  any pty row because Python3.15 removed `SourceFileLoader.load_module`.
  Reproduced RED on nomad's installed3.15 and with an API-hiding regression
  on3.11; replaced it with `spec_from_loader/module_from_spec/exec_module`.
- `tools/words-loader-test` now runs on every built CI host/tier and is
  asserted by the planner. No application source or old expectation changed.
- Full Mac native words witness on3.15 is green, including raw pty laws;
  median0.045417ms/p990.061375ms. The Linux-only idle row explicitly skips.
- Fresh executable fixture startup on macOS measured142.5ms, then3.2–3.6ms.
  Explicitly warm only the owned help fixtures before opening pelt, remove
  markers, and retain all no-execution/cache/late-output assertions.
  The application's50ms budget is unchanged, not waived or relaxed.
- Updated loader/words gates also pass on Linux native and release.
  Strict release median0.142180ms/p990.339032ms; idle10s unchanged.
- Both original hasu whole jobs are now exit0; final1148708 printed
  `FINAL: 0 failed` and inputs-stable0 at12:13:44Z. Those application sources
  are unchanged by this harness-only correction. Three plants were confirmed
  red by their named rows and closed by the orchestrator.
- New-head CI **40209085844** was read once as queued. No CI wait.
  Evidence: `notes/sh31/macos-loader-fix.txt` and its indexed logs.


- `f10f2ea`: persistent abbreviations, typed/raw and direct storage checks.
- `3864aed`: Enter-only history events, separate accepted text, echo/history.
- `8091c9b`: described bounded pager and explicit cached help probes.
- `5d4f754`: measured Space/Enter and separator abbreviation triggers.
- `3d6b0e1`: pelt's lexer extracts nested/quoted last shell words.
- `a3cc04d`: 64 typed sessions, raw witness and CI/planner gate.
- `e43646d`, `fe77684`: user docs and README refresh.
- `b855cde`, `47b9d4f`: final review guards for midword Enter, height-only
  resize and strict remaining capture capacity; final-head validation pending.

Verified through pre-review `5497d4c` (same code as rebased `a3cc04d`):
- [x] Both native/release builds and compiled selfchecks.
- [x] Checked wolf tests: 1 passed, zero rejected/unsupported.
- [x] 64 new sessions on each tier: 64 pass, zero fail/pending.
- [x] Raw resets, no style in stored text, separate-shell persistence,
  exclusive-temp collision, malformed records, script/-c/pipe isolation.
- [x] Events echo, quoting/comments, spelling, abbr order, cancel, history.
- [x] Pager columns/navigation/accept-not-execute/dismissal/width resize;
  explicit-help nonexecution while typing, cache and timeout.
- [x] CI planner and legacy-expectation diff checks.
- [x] Strict release median and p99 below 1 ms after executing `!!`.
- [x] Whole local regression at1148708, including the last review guards;
  unchanged application source, updated harness separately green on Mac/Linux.
- [ ] Final-head `tier pr`, then orchestrator-labelled `tier full` on hosts.
- [x] Three plants confirmed red at the intended named rows and closed by orchestration.

Cost/idle at `5497d4c`, owned pty, 80 columns, 100 keys after warmup:

| tier | median ms | p99 ms | idle 10 seconds |
|---|---:|---:|---|
| native | 0.056639 | 0.063717 | zero context-switch delta; RSS 11056→11056 kB |
| release | 0.047037 | 0.054128 | zero context-switch delta; RSS 8068→8068 kB |

CPU/fault/resident/anonymous memory also unchanged, child-only THP disabled.
These figures are not final-head evidence after `b855cde`/`47b9d4f`.

Plants (fix/gate committed first at `5497d4c`), draft PRs never to merge;
run IDs and first states read once by the lane; orchestration subsequently
confirmed these named reds and closed the drafts:
- #85 `9b5bd67`, run **40186401537**, in_progress:
  `tools/words-witness` / `abbr-script-gate` must reject script expansion.
- #86 `4ff081f`, run **40186405017**, in_progress:
  compiled selfcheck / `completion-pager-storage` must reject ESC in Ed.buf.
- #87 `c726d06`, run **40186410400**, in_progress:
  selfcheck / `event-last-word redirection` and event rows reject first-word !$.

Durable full jobs on hasu, not waits held by this lane:
- Earlier frozen `5497d4c`: `/home/mfwolffe/lanes/sh31/final-job.{pid,log,exit}`;
  pid 2496650; native whole corpus already 1023/0/15. This job does NOT
  cover the last review guards and cannot substitute for the next job.
- Final-head `1148708`: `/home/mfwolffe/lanes/sh31/final-head-job.{pid,log,exit}`;
  separate checkout `/home/mfwolffe/lanes/sh31/pelt-final`, queued behind
  the first on the same B lock; both have now exited0. Per-step logs under
  `notes/sh31/logs/` there.
  The job asserts tracked source input manifests before/after the whole rig.

## Done-when

Implementation, 64 new typed expectations, raw gates, oracle measurements,
docs, README, plants and sh32 draft are staged at the final head. This is
**not merge approval**: new-head CI and the orchestrator's labelled full
tier remain required; local full/application and changed-harness results
and named plant reds are now recorded above. The
lane does not label or wait on CI. README read and refreshed.

`notes/sh31/measurements.txt` records the recommendation amendment and
measurement limits; `follow-on.txt` drafts sh32's friendly/right prompt;
`issues-to-file.txt` lists existing PAX/pin gaps and documented limitations,
with no issue filed or closed. `prune-list.txt` names only sh31 paths.
Preserve raw recordings and both jobs' evidence until review. Audit status
and the final run's id/state follow in the handback.

