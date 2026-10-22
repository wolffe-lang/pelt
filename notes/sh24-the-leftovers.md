# sh24 — the leftovers

pelt#45, #46, #53, #54, #55 and two parts of #28. GPT-6.1-Sol, crawl 54.
The contract is `sprints/pelt/25-the-leftovers/sh24-the-leftovers.md` in the
planning repository. The prediction was committed before implementation in
`a3100b7`, `notes/sh24-evidence/prediction.txt`.

Footprint: cross-cutting

## 1. Forbidden, absolutely

No shell's, libc's or kernel's source was read. References were the required
planning records, pelt's own code, wolf's guide/specification and black-box
dash 0.5.13.4 and bash 5.3.20. No pin changed. Every build, corpus, session,
profile and process measurement ran inside sh24's own rootless container on
kasumi, `ulimit -c 0`. No build on nomad-1, package installed, issue filed or
closed, merge, tag, or attribution trailer. Detached jobs use `setsid -f`,
recorded pids and namespaced paths; stopped runs were identified by their
sh24 container ids, never by process group or another lane's name.

The coordinator moved the four-core measurements from CPUs 0–3 to 8–11
because eight lanes were sharing 0–3. The final gauntlet also runs bare
controls. Uptime is printed beside every table and at each gate. The existing
`builtin/c_times_real` timed out at high load in the first run; neither its
assertion nor ten-second timeout changed. A separate printing driver waits
for load below 16 to retake it.

## 2. Inputs, verified

Trunk was `57ffef9`, fetched into the separate sh24 worktree without switching
the shared checkout. Wolf 0.2.34 / lupin 0.1.55 / std `e036bec` remain pinned.
`tools/fetch-toolchain` verified the Linux archives against their recorded
SHA256 values. The starting counts were sh20's 989/0/28 and 289/0/2.

Paths: `src/sh/jobs.lu` holds the table/listing, `exec.lu` the fast command,
compound redirection and input-boundary paths; `builtin.lu` has trap options
and checked writes. `tools/shape-rss` is the memory gate. sh22's chunk-grab
profiler and sh20's RssAnon/RssFile split were re-used, not shell source.

## 3. Prediction

- **#45:** a new listing per call was the cause, but pooling alone left the
  ordinary path's copied expansion encoding. A constant encoding for the
  literal empty query removes that too; listing text/bytes live in a region
  and failed writes still propagate. The 10,000-call check subtracts an
  equal-length `true` input control to exclude input/parser storage; Linux
  RssAnon excludes file-backed pages. Initial native result: trunk 72–74,
  head 0–1, dash −1–0 B/call. The CI gate uses 100,000 calls, bound 16 B/call plus
  the existing 1 MiB granularity allowance. Final table below is still pending.
- **#46:** the prediction that records/text, not descriptors, dominated held.
  The first fold/cache implementation did not meet the bound: RssAnon grew
  about 220 B/job. It is retained as failed evidence, not waived. The final
  layout folds only an ended single-process background job in a script,
  leaving foreground pipeline readers and interactive records intact; caches
  syntax-node text; packs group and common pooled text references into the
  existing slot; and has an unlimited overflow-reference list. Released pool
  entries are reused. Native/release checked table tests include extreme
  groups/status/flags, shared/replaced/released texts, overflow and AST reuse.
  The original nominal 160 B prediction is slightly missed on release 163,
  inside the committed 160 B/job + 64 KiB over 3,000 jobs gate. No bound increased.
- **#54:** the predicted `redirs_of` list, not saved descriptors, was the
  keep: 103 of 104 root chunk grabs were `[list_push] < redirs_of < run`.
  Direct AST iteration alone took the first native rows 663–681 to 20–86
  B/turn. Three separate brace/if/while rows cover it.
- **#55:** the literal free-on-reap prediction was wrong. Dash keeps a waited
  job inside the same complete input command. It tells/frees between complete
  commands of a sourced interactive file, where pelt kept it to the prompt.
  Accepted R-sh24-1 fixes that boundary. The first broad evaluator change
  moved notices at the prompt too and failed seven existing sessions; those
  logs remain. `4e8cb20` restricts notification to sourced input and preserves
  prompt timing. The new session is red at trunk: pelt `[2],[1]`, dash `[1]`.
- **#53:** the fast path reported after closing the shadow's redirections.
  It now reports through shadow descriptor2 while open. An optimized
  one-command subshell still reports outside its redirections/capture;
  the added capture control exposed and fixed that distinction.
- **Item6:** two cheap fixes, as predicted: invalid trap options are fatal in
  a script, and non-EPIPE builtin writes are checked. A failed shadow builtin
  must not flush before ordinary fallback (`printf_bad_number` caught the
  duplicate-output attempt). #6 requires input/lexer read boundaries,
  lookahead, aliases and here-documents, not one echo in the evaluator; #20
  still needs W06 byte-string process/environment/file APIs. #28's census
  timestamp coin is untouched. These three issues remain open.

R-sh24-2, accepted: the new monitor row reads retained Linux RssAnon at the end
of the same complete command, before notices/exec. Identical binaries moved
100+ KiB of RssFile between runs; peak could both hide and invent a failure.
The 160 B/job + 64 KiB bound is unchanged. macOS retains peak RSS for full CI.
The other existing shapes retain their measurements and assertions.

### Memory table at the frozen code head

Ranges over three passes, each bare and on CPUs 8–11 (six readings per cell),
`logs/table-*.log`. Bytes per turn/call/job. The loop floor is included except
for the explicitly input-controlled jobs query. Negative values are noise,
not a claim that a turn frees memory.

| row | sh20's archived issue baseline | trunk native / release, rederived | head native / release | dash, rederived |
|---|---|---|---|---|
| bare loop | 36–59 | 19–51 / 36–52 | 38–75 / 39–65 | −9–5 |
| jobs query, own keep | about 60 | 75–86 / 77–82 | −4–2 / −2–0 | −1–0 |
| monitored `env true & wait $!` | 111–299 on the older no-wait/peak shapes | 353–361 / 352–354 | 159–163 / 161–163 | 90–91 |
| redirected braces | 644–721 | 638–714 / 638–675 | 24–64 / 31–67 | −9–14 |
| redirected if | 644–721 | 658–716 / 675–705 | 43–67 / 49–83 | −4–6 |
| redirected while | 644–721 | 648–670 / 657–683 | 33–63 / 34–64 | −5–2 |

The monitor row now uses retained RssAnon, and waits each job explicitly; its
dash reading is **90–91**, not the archived 0–16 for different no-wait/peak
shapes. These are not presented as the same measurement. The original
no-wait neighbors are being rederived separately with the new instrument.
The stricter 10,000-call jobs check (`jobs-anon-bare.log`,
`jobs-anon-four.log`) reads trunk 72–74 native / 72–73 release, head −2–0 /
−1–0, dash −1–0 B/call: comfortably within 16 on both tiers.

The high-load timing row was retaken unchanged at load 13.88–14.94 and passed
on both tiers, bare and four-core (`retake-times-*.log`, `retake.launch.log`).

## 4. Evidence index

Everything here is under `notes/sh24-evidence/`.

- Baseline reds: `logs/rows-base-native.log`,
  `logs/compound-base-native.log`, `logs/jobs-base-corrected.log`,
  `logs/session-base-native4.log`, `logs/setm-base-final.log`.
- Attribution: `probe/heapprof.py`, `probe/compound.sh`, `probe/setm.sh`;
  `logs/profile-base.launch.log`, `logs/profile-compound.launch.log`.
- Retention instrument: `probe/jobs-anon.py`, `probe/monitor-anon.py`.
  Equal-length controls and RssAnon are explicitly distinguished from peak.
- Frozen final code: `428e4ff`; later commits change notes/docs/README only.
  `gauntlet.sh`, `table.sh`, `retake.sh`, `ctr.sh`, `launch.sh` reproduce the
  container runs. Final gauntlet/table logs and counts are pending.
- First attempt: `first.status`, `gauntlet/first-*`, `first-table-*` retain
  the inadequate monitor layout and the prompt-notification regression.
  Stopped/moving-tree exploration is not final-head evidence.
- CI plant A: `39798914029`, `sh24-plant` at `2fc22e4`, source at trunk.
  Both tiers red on exactly the five new memory rows, four new corpus rows
  (`trap_bad_option`, `write_full`, `jobs/write_failure`,
  `signal/simple_end_redirected`) and `jc_wait_frees`. Counts 990/4/28 and
  sessions 289/1/2. `ci/plant-a-39798914029.log` is the full log.
- Updated-metric plant A: `39803107364`, `0dcc58a`, pending.
- Packed-field plant B: `39803216452`, `ee1eab9`, pending; status writes
  deliberately erase packed group/text bits. These branches never merge.

Commits:
- `ad79302`, `464046b`, `3ece371`: pooled jobs queries/listing/error propagation.
- `5b6b344`, `af940cf`: compound redirection scratch and its three gates.
- `a5a3867`, `4e8cb20`: sourced complete-command notification, prompt retained.
- `96065a5`, `97523af`: redirected signal notices and optimized subshell control.
- `8604cbf`, `799bd78`, `c267215`: trap/write fixes and shadow fallback guard.
- `2c5819a`, `3d7b5da`, `17a563f`: folded records, packed group/text pool, overflow.
- `169db63`: approved monitor RssAnon measurement with unchanged bound.

## 5. Done-when

- [x] Prediction before the first implementation change.
- [x] Five principal fixes and two cheap #28 fixes; no pin move.
- [x] Each issue's new row red at trunk; first CI plant red on both tiers.
- [ ] Final corpus 994/0/28 and sessions 290/0/2 on both tiers, bare/four-core.
- [ ] Three full shape passes on both tiers, bare/four-core; comparison table.
- [x] Low-load retake of the existing timing row, no assertion/timeout changes.
- [ ] Updated-metric and packed-field CI plants, final evidence recorded.
- [ ] Final tier-pr verdict, final-head full-matrix label, lane audit, pruning.

On merge, close pelt#45, #46, #53, #54, #55. Comment #28 (two fixes, census
coin remains), #6 and #20 (not one-site fixes; unchanged pending surfaces).
Leave pelt#56's job-text ruling untouched. No issue was filed or closed.

## State at the pause (2026-10-22)

The source is frozen at 428e4ff. New gauntlet `logs/final.status` has both native
corpus runs green 994/0/28; sessions and remaining gates are running. The
interleaved table runs independently, with uptime; the low-load retake prints
once a minute while waiting below 16. Paths on kasumi are
`/home/mfwolffe/lanes/sh24/head` (frozen code), `pelt` (staging), `base`
(trunk binaries), `first-head` (failed first layout), `logs` and `probe`.
All pids are recorded under that lane directory. Draft PR #58 is not ready to
merge. Final measurements, CI/audit and pruning are still owed.
