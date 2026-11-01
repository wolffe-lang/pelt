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
