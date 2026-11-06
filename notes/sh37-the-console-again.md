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
