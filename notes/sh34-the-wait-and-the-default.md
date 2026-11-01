# sh34 — the stalled wait, the macOS gauntlet's minutes, and friendly by default

Contract: `wolf/sprints/pelt/34-the-wait-and-the-default/sh34-the-wait-and-the-default.md` (crawl 54, batch A). Base: pelt
trunk `81562fd3` (wolf 0.2.36, lupin 0.1.58, std `78b9d3cb`). Clean room: no shell's or line editor's source; dash, bash
and fish are black-box oracles only. wolf-lang's runtime is read at the pin (`5adf3d91`).

## Prediction

Written 2026-11-01 15:40 EST, before any change or measurement of this lane. The evidence read so far is px83's three
timeout snapshots on hasu (`~/lanes/px83/runs/diagnostic-f0-{12,15,16}/driver.log`) and the runtime's source at the pin.

### #98, the stalled `wait`

- **What the snapshots already show.** At every timeout pelt (pid 28 there, pid 1 of its namespace) has exactly one task,
  `/proc/28/task/28`, in `futex_do_wait`, with SIGCHLD caught (SigCgt bit 16) and nothing blocked (SigBlk 0). A pelt at
  rest has two (`"Threads": "2"` in sh32's idle measurements): main and the runtime's signal drain thread
  (`wolf-signal`, `crates/wolf_rt/src/signal.rs` `reader_main`). So **the drain thread is gone** and the main thread is
  parked in `os_signal_wait`'s condvar (`signal.rs` `wait`, `h.cv.wait(st)`, no timer since s242), which only the drain
  thread's `drain` + `notify_all` ever wakes. The SIGCHLD of the last child runs the trampoline on the main thread,
  writes its byte to the self-pipe and interrupts the futex, which std retries on EINTR: nobody reads the byte, the
  `wait` never returns, the child stays a zombie.
- **H2, the leading hypothesis (the runtime's).** `reader_loop` reads `errno` *after* `back_from_poll()`:
  `let n = poll(..); back_from_poll(); if n < 0 { if last_os_error() == EINTR { continue } return }`. During `os_fork`
  the main thread blocks every catchable signal and `fork_hold` claims the drain thread (`READER_HELD`) inside its `poll`.
  A SIGCHLD from an earlier `true &` can then only go to the drain thread: `poll` answers -1/EINTR, `back_from_poll`
  finds the claim and `std::thread::park()`s, and when the fork's `fork_release` unparks it between the parker's state
  change and its `futex` call, the futex answers EAGAIN, which overwrites `errno`. The thread reads EAGAIN, takes the
  interrupted poll for a fatal error and returns; `READER_UP` stays true, so `try_hub` never makes another. Eight `true &`
  with no `wait` between them fork while earlier children end (the shape that stalls); `true & wait` reaps each child
  before the next fork (the shape just before it, always green).
- **Expected at the replays.** hasu block B, `taskset -c 6-9` inside the container, the F0 sequence (px83's shapes keys)
  typed into a fresh `sh` (pelt, argv[0] `sh`) through a pty at 20 ms a byte: trunk stalls at a rate of the order of
  9 of 20. In every stalled replay the per-step task watch shows the thread count fall from 2 to 1 at or before the
  stalled step, and an strace of a stalled shell shows the drain thread's last calls as `poll … = -1 EINTR`, a
  `futex(…FUTEX_WAIT…) = -1 EAGAIN`, and the thread's `exit`. If the watch shows two tasks at a stall, H2 is wrong and
  the cause is in pelt's wait path (the job table, `jc_wait`, `jc_record`), which is then read first.
- **If H2 holds** the cause is the runtime's: a minimal wolf witness (forks while children end, with CHILD listened;
  the thread count read from `/proc/self/status` each round) goes to the orchestrator to file on wolf-lang, and pelt
  is changed only where pelt is wrong. Whether pelt bridges the stall until a fixed pin is a ruling (`R-sh34-2`).
- **The Mac.** macOS's std parks on a semaphore, not a futex that answers EAGAIN, so the Mac may not reproduce H2's
  clobber; I expect fewer stalls there or none.

### #99, the macOS release gauntlet's minutes

- Expected: the suite grew. sh28–sh32 added the friendly sessions and four witness steps after pelt#40 measured the job
  at 38–41 minutes, and the session corpus is the step that holds most of it. The runner's speed varies night to night
  by a few minutes, which is what tips a job near its cap over it. The fix keeps every row: a split of the macOS
  release leg's session corpus into its own job or a limit sized by the house rule ((peak phases + scaled big rows +
  180 s) × 1.4), `R-sh34-1`.

### Friendly by default (ruling #126, R-F-1)

- `friendly_invocation_allowed` (`src/sh/edit.lu`) decides from argv[0]'s basename (a login shell's leading `-`
  stripped), `--posix`, `-c`, a script operand, and stdin/stderr being terminals. Expected: every friendly session that
  sets `set -o friendly` today passes unchanged with the line removed; every session compared with `dash -i` runs with
  friendly off by its invocation (argv[0] `sh` in the session harness), and its bytes do not move; the corpus and the
  scripts do not move. One new row per off-condition (argv[0] `sh`, `-sh`, `--posix`, `-c`, a script, a pipe), each
  red at trunk where trunk is opt-in (at trunk an interactive `pelt` is off, so the "on by default" row is the red one;
  the off rows are green at trunk and stay green).

### How the prediction held

- **#98: the snapshot reading held, and H2 is the mechanism (the runtime's).** hasu block B, `taskset -c 6-9` in `sh32-oracle`, trunk's code
  (`78f2b7f` = trunk + the tool), the F0 sequence through a pty: native 1 stall in 20, release 0 in 20, static 0 in 20,
  under strace 0 in 10 (job 1, `~/lanes/sh34/job1.log` on hasu). The rate is far below px83's 9 in 20, which ran pelt as
  pid 1 of its namespace beside the rest of pax's job. The one stall (native run 2) is the snapshot exactly: `Threads: 1`,
  the main task in `futex_do_wait` (syscall 202), one zombie child, SIGCHLD caught and unblocked, and **every hub
  descriptor still open** (fds 3–8, the self-pipe, the control pipe and the wake pipe), so no descriptor was closed
  under the drain thread; the watch shows two tasks at the prompt before step 23 and one at the stall, so the thread
  left during the eight `true &`. The Mac: 0 stalls in 40 (20 native, 20 release), as predicted.
- **The witness proves H2.** `notes/sh34/witness/drain_after_fork.lu` (CHILD listened, eight forks back to back whose
  children exit at once, `Threads:` read before each reap) on hasu under `taskset -c 0-3`: **9 of 10 runs red**, the
  drain thread gone at round 2 to 13 of 3,000; the tenth hung in its reap's `os_signal_wait` until its 120 s timeout
  (the stall itself). Under `strace -f` red at the first try (`notes/sh34/witness/strace-red-drain-thread.log`): the
  drain thread's `poll` answers EINTR (a SIGCHLD's trampoline runs on it, since main blocks every catchable signal
  across the fork), it parks in `back_from_poll` for the fork's hold, a later park's `futex` answers **`-1 EAGAIN`**
  when the unpark wins the race, and the thread `exit(0)`s: `reader_loop` read EAGAIN for the poll's errno. pelt is not
  wrong anywhere on this path (`R-sh34-2`). Filed by the orchestrator as **wolffe-lang/wolf-lang#1006** from
  `notes/sh34/witness/ISSUE.txt` (confirmed on wolf-lang trunk); s275 fixes it in the runtime. pelt#98 stays open on it.
- **#99: the suite grew, as predicted.** The 290 sessions both a 24 Oct and a 31 Oct nightly ran cost 588 s on both
  dates; the 294 the friendly lanes added (sh28 203 s, sh29 211 s, sh30 118 s, sh31 236 s, sh32 139 s) cost 911 s. The
  macOS leg's peak steps summed to 47–50 minutes against its 45. Not the runner, not one step. The prediction missed one
  thing: the linux legs were close too (35–36 of 45, the session step 20.7 of its 25 minutes), so the fix is every host's.
- **Friendly: the default held, the probe did not at first.** The first form of the new rows probed `bindings
  >/dev/null 2>&1`, which points standard error away from the terminal before the lookup, so friendly is never active
  for it; it was corrected before the code commits (the rows commit was amended locally, never pushed in the wrong form).

## Forbidden

- No shell's or line editor's source was read (dash, bash, readline, libedit, fish, zsh, ksh, busybox, yash, toybox);
  dash 0.5.13.4 and bash 5.3.20 ran only as black boxes (the two new corpus cases' expectations are checked by
  `tools/oracle-record --check` against them). wolf-lang's runtime was read at the pin (`signal.rs`, `fork.rs`), as the
  contract allows; px83's evidence on hasu was read, not written.
- No attribution trailer in any commit or PR. No label, merge, tag, release or issue filed or closed. No CI run re-run,
  cancelled or waited on: each run id was read once.
- kasumi untouched. hasu: blocks taken by both lock names with one `flock -w 21600` each, detached with a pid file, a log
  and an exit marker; from the 2026-11-01 21:10Z rule on, each new job went to the emptier block. Containers keep bash as
  pid 1 (`; exit $?`). Processes ended only by recorded pid, and only ones the lane started (a stalled replay's shell
  and its zombie's parent, the replay's own busy loops).
- The Mac: every build and run behind the Mac build lock, the 8 GiB gate a conditional in the runner, each in a
  worktree pinned to a commit. **One slip:** at 16:36 the gauntlet's runner took the lock about 20 s after this lane's
  run 5 released it, because the runner checked the 60 s turn only when it started, not when it took the lock; s272's
  waiter (pid 75810) was starved for that turn. The runner is fixed (`mac-run3.sh` checks at the taking). No fork storm on the host's table: the witness ran on hasu only.
- Nothing under `/var/folders`, `~/.claude`, the planning repo, another lane's directory, or the maintainer's data.

## Inputs verified

- Base pelt trunk `81562fd3` (pinned wolf 0.2.36 `5adf3d9`, lupin 0.1.58, std `78b9d3cb`); `tools/fetch-toolchain`
  staged the pinned archives on hasu (x86_64 linux) and on nomad (aarch64 darwin), each digest checked by the tool;
  `wolf --version` read `wolf 0.2.36 (wolfgang, pin 5adf3d9)` on both.
- `env_arg0`/`env_args_bytes` at the pin: `spec/11-os.md` `[os.env.argv]` says a non-UTF-8 argv[0] traps `env_arg0`
  (exit 134), so pelt reads argv[0] with `env_args_bytes` and never decodes it.
- The CI evidence for #99: the jobs API of the ten scheduled runs 39962942279 … 41320778847 (2026-10-23 … 11-01), per-step
  times, and the logs of 40095486040 and 41211008350 for per-session times (`~/lanes/sh34/ci99/` on nomad).
- The container `localhost/sh32-oracle` (Arch; python3, cc, strace, dash, bash, fish), used as sh32 and sh33 did.

## Rulings recommended (R-sh34-N), each implemented as recommended

- **R-sh34-1 (#99): how the macOS gauntlet fits.** (A) size the gauntlet's limit by the house rule, (peak phases +
  180 s) × 1.4: about 74 minutes for macOS, 55 for linux, and every leg still serial; (B) the session corpus in a job of
  its own on every leg that builds, each job's limit by the house rule; (C) shard the corpus inside the job. **B**: the
  corpus is half of every leg on every host, linux's session step was at 20.7 of its 25 minutes, and a split halves
  every leg's wall time (a pull request's linux legs about 36 → 23 minutes) where A doubles macOS's hold of a scarce
  slot; C runs timing-sensitive cases (idle, resize, deadlines) side by side. Cost: the nightly holds four macOS slots
  for about 27 minutes instead of two for 45, the merge two for 27 instead of one for 45. Limits: gauntlet 40 (peak
  24.6 min, rule 38.7), sessions 45 (peak 27.5, rule 42.7), the corpus step macOS 40 (25.1, rule 39.8) and linux 35
  (20.7, rule 33.6). No case is dropped, filtered or sharded; `ci/tiers-test.py` pins all of it (red first at `6a7db3e`,
  67 FAILs against the old workflow; 138 PASS at the head).
- **R-sh34-2 (#98): what pelt does about a runtime that loses its drain thread.** (A) nothing: pelt's `wait` and
  foreground wait keep parking in `os_signal_wait` as `[os.signal.wait]` says they may, the witness goes to wolf-lang
  (filed as wolf-lang#1006), and pelt#98 waits on the pin with the fix (pax keeps its one-retry bridge); (B) a bridge in pelt until that pin: park
  in `os_signal_wait_fds([], set, -1)`, whose `poll(2)` is interrupted by the signal on the main thread and reads the
  self-pipe itself, so a lost drain thread no longer hangs pelt (no sleep; `trap` of a new signal would still wait up
  to 5 s for the gone thread's unblock). **A**, as the contract directs: pelt is not wrong here, and a bridge would hide
  the runtime's bug from the replay that shows it. The proof's "0 stalls in 100 at the head" is therefore not met by
  this PR, and the orchestrator waived it (the cause is the runtime's); the head's count is reported beside trunk's
  from the same rig.
- **R-sh34-3 (friendly): what the default turns on.** (A) `friendly` with every feature it gates and `suggest` and
  `histsearch`, docs/FRIENDLY.md's planned default and the campaign's rule 1 (the umbrella gates the whole, each
  feature has its own `set +o`); (B) only what `set -o friendly` turns on, suggestions and filtered history still
  opt-in. **A.** Every existing friendly session and witness names its starting state explicitly, so none moved.
- **R-sh34-4 (friendly): is `sh` a hard off or a default off?** (A) hard: invoked as `sh`, `set -o friendly` records
  the option and nothing turns on, as `--posix` (the seam's own comment since sh28: "reject an argv[0] whose basename is
  `sh`"); (B) default off only, `set -o friendly` works under `sh`. **A**: a `/bin/sh` session is dash's whatever an ENV
  file asks, and PAX's `/bin/sh` console stays POSIX; a user who wants friendly runs `pelt`.

## Evidence index

Commits (base `81562fd3`):
- `0698fe6` the prediction, before any change.
- `78f2b7f` `tools/wait-replay`, the F0 replay through a pty (pelt#98's row); `28b2858` its `--load`.
- `ead2b49` the session harness names the invocation: `sh` unless a case says `argv0=` (`INVOKE`, `invocation`).
- `95f9704` the 252 sessions that use friendly are invoked as `pelt`; `541d058` each names `suggest`/`histsearch` (and
  the seven that turn friendly on in their keys, `friendly`) off, as they started; `2241911` the witnesses (`lib_shadow`)
  start with every friendly option off.
- `0d0ea03` seven sessions, red first at trunk: `sh34_default_on`, `sh34_default_on_login`, `sh34_off_sh`,
  `sh34_off_login_sh`, `sh34_off_path_sh`, `sh34_off_posix`, `sh34_off_c_script_pipe`.
- `a214f61` argv[0] from `env_args_bytes`, `named_sh`, `invoked_sh`: invoked as `sh` friendly is off; `8553a63` the
  default (`friendly_default`) at an interactive start, before the command line's options; `b1be241` its layout.
- `6a7db3e` `ci/tiers-test.py` for the split, red first (67 FAILs against the old workflow,
  `~/lanes/sh34/ci99/tiers-test-red.log` on nomad); `d8d8bac` the planner's `sessions` job; `cea3f69` the workflow;
  `32ac326` the moved-corpus check reads steps (138 PASS).
- `e46adfc` `wait/c_last_child`, `wait/c_last_child_trapped` (the plant's rows: c_all's two children end together);
  `b9a43fd` docs/CENSUS's wait/1.
- `46f0faa` docs (FRIENDLY, KEYS, CHANGELOG); `f1860bb` README-only (friendly on by default, the sessions' job, the
  stall under "not yet", the counts 591 sessions and 1,049 cases).
- The note's evidence: `notes/sh34/witness/` (the witness, its runs, the strace excerpt, the issue text).

Rows, red then green:
- The seven sessions against trunk's binary (`78f2b7f`'s build, the head's harness), nomad: 6 FAIL (`sh34_default_on`,
  `sh34_default_on_login`, `sh34_off_c_script_pipe`, `sh34_off_login_sh`, `sh34_off_path_sh`, `sh34_off_sh`) and
  `sh34_off_posix` ok (trunk's `--posix` was already a hard off); at the head 7 of 7 on both tiers
  (`~/lanes/sh34/mac/run4.log`). The friendly rows' first probe was wrong (above); the committed rows are the corrected
  ones, and trunk's red is theirs.
- The table check: `invoked as sh, friendly is on by default or allowed` and the `named_sh` cases (`src/sh/selftest.lu`).
- `wait/c_last_child*`: green at trunk and the head (15 of 15 wait cases), red under the plant.

Plants (off the line, draft PRs, red by name):
- pelt#101 `sh34-plant-wait` (`5937ae9`; the same break on `c20c6ec` run on nomad): `FAIL wait/c_last_child`,
  `FAIL wait/c_last_child_trapped`, `difftest: wait 13 2 0` (`~/lanes/sh34/mac/run4.log`); red again at the pushed `5937ae9`
  (`~/lanes/sh34/mac/run5.log`). Its PR run 41350852471.
- pelt#102 `sh34-plant-sh` (`edec268`; the same break on `98bb980` on nomad): `FAIL sh34_off_login_sh`,
  `FAIL sh34_off_path_sh`, `FAIL sh34_off_sh`, and the table check `invoked as sh, friendly is on by default or
  allowed` (`~/lanes/sh34/mac/run4.log`); red again at the pushed `edec268` (`~/lanes/sh34/mac/run5.log`). Its PR
  run 41350855334.

The replays (pelt#98), one rig: hasu, `sh32-oracle`, four CPUs, the F0 sequence into `sh` at 20 ms a byte:
- trunk's code: native 1 of 20, release 0 of 20, static 0 of 20, release under strace 0 of 10 (job 1); under three busy
  loops (`--load 3`, CPUs 0-3, block A): static 0 of 20, release 0 of 20 (hasu job 5). So 1 stall in 100 trunk
  replays on hasu: the replay is a weak row for this race, the witness (9 of 10 red) the strong one. nomad: 0 of 40.
- the proof's 100 at the head (`b1be241`) and 100 at trunk (`78f2b7f`'s build), static, CPUs 6-9 (job 4b):
  **head 4 of 100, trunk 3 of 100**. All seven at step 23, each `Threads: 1`, `futex_do_wait`, one zombie child: the
  rate is the runtime's and unchanged, as R-sh34-2 A says it must be (`notes/sh34/logs/replays-hasu.txt`).

## Done-when

- [x] #98 reproduced on hasu (four CPUs) and on nomad; the cause found from evidence and proven by a minimal witness
  (the runtime's: wolf-lang#1006); pelt changed nowhere on the path, as pelt is not wrong there (R-sh34-2 A). The
  "0 stalls in 100 at the head" proof is waived by the orchestrator; the head's and trunk's counts are the PR's.
- [x] #99 measured (the suite grew) and fixed by the sessions' own job, limits by the house rule (R-sh34-1 B), no row
  dropped; `ci/tiers-test.py` red first, then green.
- [x] Friendly on by default (R-F-1, R-sh34-3 A, R-sh34-4 A); one row per off-condition, red first at trunk where trunk
  differs; the corpus, the scripts and the dash sessions unchanged; README, FRIENDLY, KEYS and CHANGELOG refreshed.
- [x] Two plants, draft PRs, red by name (pelt#101, pelt#102).
- [x] The gauntlet at `b1be241`, the code-final head (what follows it is notes only), on both hosts, both tiers:
  hasu (container, rows on CPUs 0-3) 44 `END` lines, every one `exit=0`, `GAUNTLET PASS`, no SKIP; nomad 41 `END`
  lines, every one `exit=0`, `GAUNTLET PASS`, 15 loud SKIPs, all host rows (the Linux `/proc` idle counters, the
  strace census, gen-width on Python's Unicode 14). `notes/sh34/logs/gauntlet-{hasu,nomad}-b1be241.txt`.
- [ ] `tier pr` green at the head; the orchestrator's label for the full tier (Footprint: cross-cutting).
- The PR fixes **pelt#99**. **pelt#98** stays open on wolf-lang#1006. Close nothing else.
- Not this lane's: pelt#65 (byte paths, wolf-lang#687, #912). `tools/interactive-census` and `tools/edit-bench`, which CI
  does not run, now measure an interactive pelt with friendly on by default; a follow-on may give them `+o friendly`.
