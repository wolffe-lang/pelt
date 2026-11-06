# sh37 — the console again: an explicit friendly opt-in as `sh`, the prompt's identity, and the stalled `wait` (pelt#113, #115, #114)

Base: pelt trunk `b514e14a` (wolf 0.2.36, lupin 0.1.58, std `78b9d3cb`). Clean room: no shell's or line editor's
source; dash, bash and fish are black-box oracles only. wolf's runtime is read at the pin, as earlier lanes did.

## Prediction

Written 2026-11-06 at 19:43Z, before any change. The evidence read so far: the three issues, sh34's note and
witness, PAX's `shapes.keys` and its replay script, pelt's `src/sh/edit.lu`, `src/sh/edit_prompt.lu`, `src/sh/jobs.lu`,
and the runtime's signal hub at the pin.

### #113: `set -o friendly` under `sh`

- At trunk `friendly_active` asks `friendly_invocation_allowed`, which is false for argv[0] `sh`. So a shell invoked as
  `sh -i` that runs `set -o friendly -o suggest -o histsearch` records the three options and draws nothing. Expected
  red at trunk: a typed prefix of a history line draws no dimmed suggestion, and `bindings` answers 127.
- The fix (R-sh37-1 A): the invocation only withholds the default (`friendly_default`). `friendly_active` stops asking
  argv[0], and `--posix` stays a hard off. The three sh34 rows that pinned the hard off (`sh34_off_sh`,
  `sh34_off_login_sh`, `sh34_off_path_sh`) keep their step 2 (`default=127`), and their step 3 changes from
  `asked=127` to `asked=0`. Each is red at trunk under its new transcript. `sh34_off_posix` does not move.
- No session compared with dash moves: none of them types `set -o friendly`.

### #115: `?@?`

- At trunk, with USER, LOGNAME and HOSTNAME unset and no `hostname` on PATH, the friendly prompt starts `?@?`.
  Expected red: rows that want the effective uid's passwd name and the system's node name.
- wolf 0.2.36 has no call that answers uname(2)'s node name: `os_name` answers the system's name, not the node's.
  Linux keeps that same field as a file, `/proc/sys/kernel/hostname`, so pelt reads it there (R-sh37-3). PAX's
  `/proc/sys/kernel` holds only `core_pattern` and macOS has no `/proc`, so both fall through to `/etc/hostname` and
  then the probe. On PAX's test image (no `/etc/hostname` and no `hostname` program) I expect `root@?` after the
  fix: the user is fixed and the host is not, until PAX serves that file or wolf has a call for it.
- The order (R-sh37-2): the user is `$USER`, else `$LOGNAME`, else the passwd entry, else `?`. The host is
  `$HOSTNAME`, else the node name, else `/etc/hostname`, else the probe, else `?`. Each fallback gets a unit row on
  every host, and the passwd and node-name legs also get pty rows on Linux.
- The sh32 prompt rows set USER and HOSTNAME, so none moves. One older row does move: the probe descriptor check
  for `hostname`, which needs the probe to run. On Linux the node name now answers first, so the probe is not
  started. I expect that row to report zero `hostname` runs at the head. It changes on Linux to "not started, the
  node name shown", stays as it was on macOS, and the direct rig's checks of the probe's descriptors stay as they are.

### #114: `wait` after eight `true &`

- **H1 (the leading hypothesis): the runtime's lost drain thread, as in #98.** That is wolf-lang#1006, fixed in
  wolf 0.2.37 and not in pelt's 0.2.36 pin. With job control on (`-m`, or an interactive start), `jc_enable` listens
  for CHILD from the start. The `true` of each `true &` runs in a forked child that ends at once, so its SIGCHLD can
  land on the drain thread while a later `os_fork` holds it. The thread then exits, and `wait` parks for ever in
  `os_signal_wait`.
- **Where the interactive path differs.** sh34 changed nothing on this path (pelt#98 is still open on the runtime's
  issue). A shell without job control listens for CHILD only at its first wait (`jc_listen`), after the forks. So no
  SIGCHLD is listened for while a fork holds the drain thread, and that shape never had the race. The shape just
  before the stalled one (`true & wait`) reaps each child before the next fork.
- **Expected witness:** pelt trunk, built static as PAX builds it, run on a four-CPU Linux container. The shapes line
  typed many times stalls at a rate of a few in a hundred lines. At every stall: `Threads: 1`, the main task in
  `futex_do_wait`, at least one zombie child, and SIGCHLD caught and not blocked. sh34's standalone witness
  (`notes/sh34/witness/drain_after_fork.lu`) is red in most runs at 0.2.36. The same pelt source built with wolf 0.2.37
  shows no stall in the same count, and the witness is green.
- **If H1 holds,** the cause is the runtime's, and pelt's fix is a ruling (R-sh37-4): a bridge in pelt's two signal
  waits, which survives a lost drain thread, or no pelt change until a pin carries the runtime's fix. I'll recommend
  from the measurements. **If a stall shows two tasks,** H1 is wrong, and pelt's job table is read first:
  `jc_take`'s deferred polls, `jc_record` and the stash.

### PAX

- PAX boots its console under KVM. The three rows typed there with pelt at this lane's head, built static the way
  PAX's `tools/mkpelt` builds it, should show the suggestion under `sh`, `root@?` in the bare console environment,
  and the shapes line completing. #114's PAX transcript already completed with trunk's binary. Under H1 that is
  timing: the race needs a SIGCHLD to land on the drain thread inside a fork's hold, and PAX's scheduler need not
  produce one.

### How the prediction held

- **#113 held.** At trunk, on Linux in the four-CPU container, both tiers: `FAIL sh37_sh_opt_in`, `FAIL sh34_off_sh`,
  `FAIL sh34_off_login_sh`, `FAIL sh34_off_path_sh` (no suggestion drawn, `asked=127`), and `sh34_off_posix` and
  `sh34_default_on` ok. At the head all of them pass on both tiers. No dash-compared session moved.
- **#115 held, with one correction.** At trunk: `FAIL prompt-user-passwd` (`?@box`), `FAIL prompt-host-node`
  (`tester@?`), `FAIL prompt-identity-bare` (`?@?`, #115's prompt exactly) and `FAIL probe-hostname-not-started` (the
  probe ran once); the `USER`, `LOGNAME` and `HOSTNAME` rows ok. At the head every one passes: the container's passwd
  name and its node name, and no `hostname` started. The correction: the passwd name is the container's own entry
  for the user id, which is not the host's user name; the rows read the expectation from the same file pelt reads.
- **#114: H1 held, and the measurement is far stronger than predicted.** pelt trunk, built static as PAX builds it,
  four CPUs:
  - the shapes line typed thirty times a run: **20 of 20 runs stalled**, each within its first eight lines;
  - pelt's replay of PAX's whole sequence: **4 of 10 stalled**, all at the shapes line;
  - at every one of the 24 stalls: `Threads: 1`, the main task in `futex_wait`, one zombie child, SIGCHLD caught and
    not blocked: the drain thread gone, as in pelt#98;
  - sh34's standalone witness at 0.2.36: 5 of 5 red (the drain thread gone at round 1 and round 23, and three runs
    hung in their reap until the 120 s bound).

  The same pelt source built with wolf 0.2.37 (the runtime's fix): **0 of 20 stalled**, the drain thread alive at
  every prompt of every run, and the witness green in 5 of 5. So the cause is the runtime's, and only the runtime's.
- **The interactive path.** The prediction's mechanism held: with job control on, CHILD is listened from the start,
  so the earlier children's SIGCHLD reaches the drain thread while a later `os_fork` holds it. The contract's premise
  that sh34 fixed a non-interactive case is not borne out: sh34 changed nothing on this path, pelt#98 is open on the
  runtime's issue, and a script without job control never had the race.
- **What the prediction missed: losing the thread is not yet a hang.** A `wait` hangs only when it must park after
  the thread is gone. When every child has already ended, its first poll reaps them all and it returns. On two CPUs
  the thread went in 3 of 3 replays and only one of them stalled. So the first form of the session row (the line
  three times, then a hundred rounds, `71f556b`) passed at trunk in 7 of 7 runs on four CPUs. Its second form
  (`074eab1`, committed before the fix) ends with a wait that must park (`sleep 1 & wait`). It was red at trunk in
  6 of 6 runs on two CPUs, each time hung at that last wait: the drain thread had gone somewhere in the rounds before.
- **The fix.** With the bridge the thread is still lost (it is the runtime's bug), but no wait hangs on it. Measured
  with the bridge's first form (it parked on a list made at each park; the committed `692391c` differs only there):
  the shapes line
  typed thirty times a run, **0 of 20 runs stalled**, though the thread went in 19 of them (first seen at prompts 3 to 21);
  PAX's sequence, **0 of 10 stalled** (the thread went in one); the session row's first form, 5 of 5 green. The
  second form's green is the gauntlet's, below. A first form of the bridge parked on a list
  literal made at every park; macOS's memory rows showed it (`jobs-set-m` 207 B a turn against its 160 B bound,
  `typed-background-wait` 234 B against 100 B and 1 MiB). The committed form parks on an empty list the shell keeps,
  and every wait shape's growth matches trunk's within a few bytes a turn.

### #110, the lost prompt of one shape run: not reproduced, a candidate named

- One cheap attempt, stopped early: the row's line, `( true; true )`, typed 3,000 times into trunk's static binary at
  1 ms a byte on four CPUs, the task count read at every prompt. Run 1 was green, with the drain thread alive at
  every prompt (`notes/sh37/w110.txt`); the next four runs were stopped to free the host for the record. The
  original failure (one whole-tool run in 128, no prompt after line 10962) left no snapshot, and sh35's instrumented
  proof was 200 of 200 green.
- A candidate, not a finding: the same runtime race. Each turn of that shape forks once (`( true; true )`), and the
  drain thread can be lost whenever a SIGCHLD is still undelivered when the next `os_fork` holds it, here only if
  the previous turn's SIGCHLD is late. Once the thread is gone, the next foreground wait parks for ever at trunk.
  That fits a failure seen once in about 2.5 million turns. It does not explain why the instrumented runs never saw
  it.
- At this head a foreground job's wait parks in `signal_park` too (`jc_wait`, and `fg_poll` on the fast path), so the
  same loss would cost at most a second there rather than the prompt. #110 stays open: a recurrence with a snapshot
  (`Threads: 1` would name it) or a causal proof closes it.

### PAX's console

PAX at trunk `84a1fde3` under QEMU with KVM, native tier, BIOS, with `user/pelt.pin` pointed at this branch's head
(`c24d5235`) and nothing else changed. PAX's own `tests/mpx5-pelt --only build` built the images, `tools/mkpelt`
built pelt (static, `bebcab46…`, 16,770,928 bytes, the same digest on both hosts), and `tests/mpx5-pelt --images`
booted them. The transcripts are in `notes/sh37/pax/`.

- **#113, the opt-in under `sh`** (`friendly-*.check.txt`). PAX's friendly rows run `/bin/env HOME=/ TERM=linux
  /bin/sh -i +m` and type `set -o friendly -o suggest -o histsearch`. On the framebuffer, on the zero-sized serial
  console and on the sized serial console, every row passes: 12, 12 and 13 of them. That includes the five #113
  listed as failing at `301e25e0`: default shadow SGR90, configured shadow SGR2, shadow erased, the Space abbreviation
  and history events with Alt-dot. The framebuffer's seven screen dumps match the reference cell for cell. PAX's
  prompt rows (F5) pass on both consoles: `pax@pax-test ~#` after `set -o friendly -o prompt_friendly`, the F5
  identity #113 listed as absent.
- **#115, the bare console** (`identity-and-prompt.txt`). One more boot: init is `/bin/pelt` by its own name, with
  kmain_console's environment (`HOME=/ TERM=linux PAX=1 PATH=/bin`), root's passwd entry as PAX's shell image has it,
  and no `hostname` program. The first prompt is `root@? ~# `, as predicted: the user is now the passwd entry's, and
  the host is still `?`. PAX serves no `/proc/sys/kernel/hostname`, the image has no `/etc/hostname`, and wolf 0.2.36
  has no call for uname(2)'s node name (R-sh37-3). So the contract's #115 row ("the system's node name") holds on
  Linux and not yet on PAX.
- **#114, the shapes** (`shapes-root.serial.txt`, `shapes-pax.serial.txt`). PAX's `shapes.keys` as root and as user
  1000, `/bin/sh -i -m`: all eleven `SHAPE:…:8` lines on both, `SHAPE:true-background:8` among them with its eight
  `Done` notices, and `PAX: init … ended with status 0` on both. mpx5-pelt's own verdict reads FAIL only for "missing
  Linux reference" (its Linux side was not run here; pelt's Linux rows are the gate).

## Forbidden

- No shell's or line editor's source was read (dash, bash, fish, readline, libedit, zsh, ksh, busybox). bash 5.3.20 and
  fish 4.9.3 ran only as black boxes, through a pseudo-terminal, for R-sh37-2; dash only for the background-wait
  row's transcript (Ubuntu's for its first form, 0.5.13.4 for its second: the same standard output). wolf's runtime was read at the pin (`crates/wolf_rt/src/signal.rs`, the signal
  hub, its drain thread and `wait_fds`), as sh34 did; nothing of it is copied.
- No attribution trailer in any commit or in the PR. No label, merge, tag, release or issue filed or closed. CI was not
  waited on: its run id was read once.
- Every Linux job ran in a container on four CPUs, behind its host's lock, with a pid file, a log and an exit marker;
  each took the lock once and stayed under two hours. The KVM boots ran as light jobs (QEMU, at most two busy CPUs).
  Processes were ended only by recorded pid or container id, and only ones this lane started: a stuck oracle probe,
  and the #110 attempt's container, stopped to free its host (its marker renamed `*.void-stopped`, with a note). Mac builds ran behind the Mac build lock,
  each in a worktree pinned to a commit, with the memory and disk gates inside the lock and the 60 s turn.
- PAX was not changed: its tree was cloned fresh and `user/pelt.pin` was pointed at this branch's head locally, the
  way a pin bump would, and never committed.

## Inputs verified

- Base pelt trunk `b514e14a`, pinned wolf 0.2.36 (`5adf3d9`), lupin 0.1.58, std `78b9d3cb`. `tools/fetch-toolchain`
  staged the pinned archives on Linux (x86_64) and macOS (aarch64), each checked by digest; `wolf --version` read
  `wolf 0.2.36 (wolfgang, pin 5adf3d9)` on both.
- wolf 0.2.37, for the runtime witness only (never pinned): the release asset's digest
  `9811d32e1dddcb743b96a14ea685faee06ba453242c1ae3deb90063f5bb9bcaa`, read twice from the release API and twice from
  the downloaded file; it bundles std `5b3a5994`. Its runtime carries the drain thread's fix (wolf-lang#1011, for
  wolf-lang#1006). pelt trunk's source builds with it unchanged.
- wolf 0.2.36 has no call that answers uname(2)'s node name: `spec/11-os.md` at the pin defines `os_name` and
  `os_arch` (`[os.uname]`) and nothing for the node, and trunk's spec adds none.
- PAX at trunk `84a1fde3`: its console starts init with `HOME=/ TERM=linux PAX=1 PATH=/bin`; `uname(2)` answers the
  node `pax`; `/proc/sys/kernel` holds only `core_pattern`; the pelt replay image (`tests/mpx5-pelt`) has no
  `/etc/passwd`, and the shell image (`tests/mpx3-shell`) has root's entry.
- The Linux container: Ubuntu 24.04 (python3 3.12, cc, clang, strace, dash, bash). The oracle container: Arch with
  dash 0.5.13.4-1, bash 5.3.20-1 and fish 4.9.3-1.

## Rulings recommended (R-sh37-N), each implemented as recommended

- **R-sh37-1 (#113): may a shell invoked as `sh` turn friendly on?** (A) an explicit `set -o friendly` turns it on
  whatever argv[0] is, and argv[0] `sh` only withholds the default; (B) PAX's console runs pelt by its own name; (C) a
  `PELT_FRIENDLY=1` environment opt-in. **A**: it restores PAX's documented opt-in, keeps the default off as `sh`, and
  needs no PAX change. `--posix` stays a hard off. This reverses R-sh34-4 A's hard off as `sh` and keeps its default.
- **R-sh37-2 (#115): the identity's order.** Measured black-box in a pseudo-terminal, with the environment varied (`USER`,
  `LOGNAME`, `HOSTNAME` unset, set alone and set together): bash 5.3.20's `\u@\h` and fish 4.9.3's default prompt both
  show the passwd name and the kernel's node name every time, and ignore all three variables (with `USER=envuser
  LOGNAME=envlog HOSTNAME=envhost`, both still show the container user's passwd name and the container's node
  name). (A) the environment
  first, then the system: `$USER`, `$LOGNAME`, the passwd entry, `?`; `$HOSTNAME`, the node name, `/etc/hostname`, the
  probe, `?`; (B) the oracles' rule, the system only. **A**: pelt has taken the environment since sh32, a console or a
  login can name itself (PAX's shipped consoles export `USER`), and the sh32 rows stay deterministic; the oracles
  decide the fallbacks' sources and their order (the passwd name for the user, the node name before any file or
  program for the host). An empty value counts as unset.
- **R-sh37-3 (#115): where the node name comes from at wolf 0.2.36,** which has no call for it. (A) Linux's
  `/proc/sys/kernel/hostname`, the same field uname(2) answers, then `/etc/hostname`, then the probe; (B) start
  `uname -n` as a second probe; (C) wait for a wolf call. **A**, with C asked for: a file read costs nothing, B is a
  program start per shell and is no help where `uname` is absent, as on PAX's test images. Two gaps stay, stated: on
  macOS (no `/proc`) the host is the probe's, and on PAX, whose `/proc/sys/kernel` serves only `core_pattern` and
  whose test images carry no `/etc/hostname` and no `hostname`, the host stays `?` until PAX serves the file or wolf
  has the call.
- **R-sh37-4 (#114): the stall is the runtime's (wolf-lang#1006, fixed in 0.2.37, not pinned). What does pelt do?**
  (A) a bridge: a job's wait parks in `os_signal_wait_fds([], set, 1000)`, the calling thread's own `poll(2)`, which a
  signal delivered to that thread interrupts and which reads the delivery itself, so a lost drain thread no longer
  hangs it; the bound covers a signal that lands between the last look and the `poll`, at a cost of one wake a second
  while a job runs; removed at the pin that carries the fix; (B) nothing until that pin (PAX's console keeps hanging
  until PAX takes a pelt on 0.2.37 or later); (C) pin 0.2.37 here, a cross-cutting change that carries the release's
  other changes. **A**: the hang is user-visible today on PAX's console and on every Linux interactive shell with job
  control, the bridge is two call sites and one helper, and the runtime's own fix is proven separately below. R-sh34-2
  chose B when the runtime's fix did not exist; it exists now, so the bridge hides nothing.

## Evidence index

Commits (base `b514e14a`):
- `cef67c0` the prediction, before any change.
- Rows, before the fixes:
  - `4965579` `sh37_sh_opt_in`, the explicit opt-in under `sh` (#113); `57d8390` its screen shows the `bindings`
    not-found line at step 2;
  - `5e37636` the three sh34 rows expect `asked=0` under `sh`, their `default=127` kept (R-F-1's default);
  - `7bb1a14` six identity rows in `tools/prompt-witness` (#115); `671a9d2` the probe row on Linux: no `hostname`
    started where the kernel names the node, the node name shown;
  - `fb30c9d` a session case may bound its prompt wait (`prompt_wait=`); `71f556b` and `074eab1`
    `sh37_jc_true_background`, PAX's shapes line, a hundred rounds of it twice, then a wait that must park (#114).
- Fixes: `f47eb6a` #113 (argv[0] `sh` withholds only the default; the table checks with it); `42f254e` #115 (the
  passwd name, the node name, `/etc/hostname`, then the probe); `8cd09d4` a unit row for each fallback in order;
  `692391c` #114 (a job's wait parks in `signal_park`).
- Docs: `4838e92` FRIENDLY, `2d78173` the changelog, `c24d523` README only (the opt-in, the identity, the bounded
  waits, 593 sessions).
- Evidence kept in the tree: `notes/sh37/`, the replays' verdict lines, the stalls' snapshots with their paths
  removed, the oracles' prompts, and PAX's console transcripts.

Rows, red then green (Linux, four CPUs in the container, both tiers):
- #113: `sh37_sh_opt_in`, `sh34_off_sh`, `sh34_off_login_sh`, `sh34_off_path_sh` FAIL at trunk, ok at the head; the
  corrected `sh37_sh_opt_in` (`57d8390`) FAIL again at trunk.
- #115: `prompt-user-passwd`, `prompt-host-node`, `prompt-identity-bare`, `probe-hostname-not-started` FAIL at trunk,
  ok at the head; `prompt-user-USER`, `prompt-user-LOGNAME`, `prompt-host-HOSTNAME` ok on both. The unit rows
  (`prompt-user-*`, `prompt-host-*` in `src/sh/selftest_prompt.lu`) run in `tools/self-check` on both tiers.
- #114: `sh37_jc_true_background` (`074eab1`) FAIL at trunk in 6 of 6 runs (two CPUs), each hung at its parking
  wait; at the head in the gauntlet below.

## Done-when

- [x] Rows red first on Linux pty sessions: #113 (`sh37_sh_opt_in` and the three sh34 rows), #115 (the identity rows
  and the probe row), #114 (`sh37_jc_true_background`, red at trunk only in its second form); `--posix` and the
  default off as `sh` kept as rows.
- [x] #113's fix per R-sh37-1 A; #115's per R-sh37-2 A and R-sh37-3 A, each fallback with a row, the sh32 prompt rows
  green; #114 diagnosed from the witness (the runtime's lost drain thread, not pelt's job table), the fix one commit
  (`692391c`, per R-sh37-4 A).
- [x] PAX's console under KVM with pelt at this head, built by PAX's own `tools/mkpelt`: the transcripts are above.
- [x] #110: not reproduced (one run of 3,000 typed subshells, green); a candidate named.
- [x] The changelog; README read and refreshed (a README-only commit: the opt-in, the identity, the bounded waits,
  593 sessions); FRIENDLY refreshed.
- [ ] The gauntlet at the head and the plant, red by name: their END lines are in the PR body, taken after this note.
- Fixes pelt#113, pelt#114 and pelt#115. pelt#98 is the same runtime bug: at this head its replay no longer hangs (0 of
  10, with the drain thread lost in one), and its own closing condition is a pin carrying wolf-lang#1011. pelt#110
  stays open.
- Issues to file: wolf-lang, a call for uname(2)'s node name; PAX, `/proc/sys/kernel/hostname`
  (or an `/etc/hostname` in the console images) so the friendly prompt names the node there; pelt, remove
  `signal_park` at the pin that carries wolf-lang#1011.
