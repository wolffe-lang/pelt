# sh37b — the loop's peak on CI's Linux (pelt#118)

Base: pelt trunk `f0761dc1` (wolf 0.2.36, lupin 0.1.58, std `78b9d3cb`). Clean room as for sh37: no shell's source;
wolf's runtime read at the pin only.

## Prediction

Written 2026-11-06 at 23:03Z, before any change or new measurement. The evidence read so far: pelt#118, the failing
job's log (run 42303595329, `gauntlet (ubuntu-latest, true, native)`), the same step's numbers in six earlier trunk
runs, and `tools/loop-rss`.

- **What the failing job itself says.** `tools/loop-rss` runs `i=0; while [ $i -lt N ]; do i=$((i+1)); done; echo $i`
  under `-c` in two separate processes (N = 10,000 and 20,000) and compares their peak resident sets
  (`/usr/bin/time`'s maximum RSS, file-backed pages included). The 10,000-turn run peaked at 6,616 KB, inside trunk's
  usual 6,340–6,876 KB. The 20,000-turn run peaked at 9,656 KB, where trunk's runs peaked at 6,800–7,420 KB. In the
  same job, `tools/shape-rss`'s in-process rows measured the anonymous memory of loops of `:`, `: $((j=j+1))`,
  `case` and `while false` at 50–51 B a turn, the same bytes a turn as at `b514e14` (run 42248806092), 12 KB higher
  at the start.
- **H1: nothing grows a turn; one process's peak jumped.** The loop is not interactive and runs no job, so neither
  `signal_park` (a job's wait) nor the prompt's identity (a friendly prompt) runs in it. I expect the same native
  build, on the runner's glibc and gcc, to show the same distribution of peaks at `f0761dc` as at `b514e14`. That
  means 20,000-turn peaks about 300–700 KB above the 10,000-turn ones, with an occasional step of a megabyte or more
  at either head, from a page-granular or allocator-granular jump that a two-process peak comparison cannot tell
  from growth.
- **H2 (if H1 fails): a per-turn copy grew.** sh37 added four fields to the shell's state (`prompt_user`,
  `prompt_passwd`, `prompt_passwd_read`, `park_fds`). If a path in the loop copies the state each turn, a list or a
  string field could cost an allocation a copy. Then `f0761dc`'s peaks sit consistently above `b514e14`'s at 20,000
  turns, and an in-process measurement of the same loop shows more bytes a turn.
- **The measurement:** on a Linux host, in a container with the hosted runner's exact glibc (2.39-0ubuntu8.9) and gcc
  (13.3.0-6ubuntu2~24.04.1), both heads built native, `loop-rss`'s two sizes interleaved over many rounds. Each run
  also reports, from inside the shell after its loop, `VmHWM`, `VmRSS`, `RssAnon` and `RssFile`. That says whether a
  high peak is anonymous memory or file pages.

### How the prediction held

H1 held, and H2 failed. Nothing in the loop grows a turn at `f0761dc` that did not at `b514e14`. The gate counted
file-backed pages, which vary from one process to the next.

- **On the runner-matched image.** This was an Ubuntu 24.04 container with the runner's glibc and gcc, on two CPUs,
  using both heads' native builds and 20 interleaved rounds of `loop-rss`'s two processes
  (`notes/sh37b/peaks-linux.txt`).
  - At `f0761dc` the 20,000-turn peak sat −4 to 904 KB above the 10,000-turn one. At `b514e14` it sat −540 to 972 KB
    above.
  - Inside each shell after its loop, `RssAnon` grew 304–324 KB over the 10,000 more turns at both heads, about 32 B a
    turn.
  - `RssFile` took any value from 5,376 to 5,964 KB at `f0761dc` and from 5,688 to 6,744 KB at `b514e14`, whatever the
    turn count. The swing in the peaks is file pages.
  - No comparison came near the bound, so the failing number did not reproduce here: 0 of 20 per head, and 0 of 24
    more below (the highest was 1,072 KB against 2,000).
  - The host's kernel is 7.2 and the runner's 7.0.0-azure. Both use ext4, and both set transparent huge pages to
    `madvise`. So this host's page cache is not the runner's, and what reproduces here is the mechanism, not the
    3,040 KB.
- **In the failing job itself** (`notes/sh37b/ci-runs.txt`).
  - All 52 of `tools/shape-rss`'s in-process rows grew within 8 KB of `b514e14`'s over their second 10,000 turns.
  - The same job's idle witnesses (one pelt process each) show `RssFile` from 5,740 to 6,824 KB at nearly the same
    `RssAnon` (7,324–7,476 KB). At `b514e14` it ran from 5,888 to 7,528 KB, a 1,032 KB difference between two
    processes of the same shape.
  - A peak taken across two processes carries that spread whole. The 3,040 KB the gate saw is about 300 KB of the
    loop's own memory plus a jump in file pages that those processes' range makes plausible on the runner's kernel.
    It is not proven: no CI job recorded the two processes' `RssFile`.
- **What the loop runs** (`notes/sh37b/metric-rows.txt`, `notes/sh37b/env-loop.txt`).
  - Under `strace`, the 1,000-turn `-c` loop opens only the dynamic loader's files: three opens, the same at both
    heads, with no open of `/etc/passwd`, `/proc/sys/kernel/hostname` or `/etc/hostname`. It makes one `poll`, the
    same at both heads.
  - That holds under `loop-rss`'s fixed environment, with `USER`, `LOGNAME` and `HOSTNAME` set, and with no
    environment at all.
  - The loop's kept memory does not vary with the environment either: 340–348 KB over 10,000 more turns in each of
    the three, three rounds each.
  - The prompt's identity fallbacks run only for a friendly prompt, and `signal_park` only for a job's wait. The loop
    is neither.
- **`signal_park`'s wait, measured where it runs.** These rows wait on a job every turn: `true & wait`,
  `env true & wait`, `true & wait $!`, the script and typed forms, and `set -m`'s `env true & wait $!`.
  - At `b514e14` a job's wait parked in `os_signal_wait`. At `f0761dc` it parks in `os_signal_wait_fds` on the shell's
    kept empty list (`sh.park_fds`).
  - CI measured those rows at the same bytes a turn at both heads: 110 B a turn in a loop, 64–65 B in a script, 191 B
    typed, and 170 B under `set -m`. So the call keeps nothing per call on a kept list.
  - The list literal that sh37 first passed per park did keep memory on macOS. The kept list is the reason it no
    longer does.
- **The two metrics, side by side.** Over 12 rounds on `f0761dc`'s builds, trunk's `loop-rss` and the fixed one gave:

  | build | trunk's `loop-rss` | the fixed `loop-rss` |
  |---|---|---|
  | native | 0 to 1,072 KB | 340–348 KB |
  | release | 52 to 696 KB | 324–328 KB |

  The fixed metric's spread is 8 KB.

### The fix (R-sh37-5 A)

On Linux, `tools/loop-rss` now measures what `tools/shape-rss` has measured since sh35: the loop's kept anonymous
memory. The loop runs in one process, which samples its own `/proc/self/smaps_rollup` (`Anonymous` + `Swap`) with
built-ins after 10,000 turns and again after 10,000 more. It never counts file-backed pages.

The bound is unchanged: 100 B a turn plus 1 MiB. The output keeps its `ok`/`FAIL` lines. A non-zero exit, a wrong
count, any standard-error byte or a missing sample is still a failure. macOS has no `smaps_rollup`, so it keeps the
two processes' peaks.

The rows that went red first are in `tools/shape-rss-test` (`LoopRssMetric`). A stand-in shell, a small C program
built by the test, counts its `-lt` turns and either maps 400 B of a file's pages a turn or keeps 400 B of
anonymous memory a turn.
- At `15a9956`, with trunk's `loop-rss`, the mapped-pages row FAILs: "10000 more turns grew 3884 KB (about 397 B a
  turn); the bound is 2000 KB". The kept-memory row is ok.
- At `f8cfe61`, with the fix, both rows are ok. The gate still fails a shell that keeps memory.

## Forbidden

- No shell's source was read, and no oracle was needed. wolf's runtime was not read again: the answer about
  `os_signal_wait_fds` comes from measurements, CI's and this lane's.
- No attribution trailer in any commit or in the PR. No label, merge, tag, release, or issue filed or closed. CI
  was not waited on: its run id was read once.
- Every Linux job ran in the runner-matched container, either on a light slot of two CPUs (the measurements) or on
  four CPUs behind both of its host's locks (the gauntlet and the plant). Each job had a pid file, a log and an exit
  marker, and stayed under two hours.
- No process was ended. Nothing was written to `/tmp`: each job's `HOME` and `TMPDIR` sat under the lane's own
  directory.

## Inputs verified

- Base pelt trunk `f0761dc1`, with the same pins as `b514e14a`: wolf 0.2.36 (`5adf3d9`), lupin 0.1.58 and std
  `78b9d3cb`. `wolf-toolchain.toml` is unchanged between the two.
- The failing job: run 42303595329, `gauntlet (ubuntu-latest, true, native)`, image ubuntu-24.04 20261101.360.1. The
  last green trunk job at `b514e14`: run 42248806092.
- The runner's glibc (2.39-0ubuntu8.9) and kernel (7.0.0-1017-azure) were read from a same-day ubuntu-latest job's
  apt log, and its gcc from the image's 13.3.0-6ubuntu2~24.04.1. The container carries the same glibc and gcc
  packages, version for version.

## Rulings recommended (R-sh37-N), implemented as recommended

- **R-sh37-5 (#118): what does `loop-rss` measure on Linux?**
  - (A) The loop's kept anonymous and swapped memory, in one process, as `shape-rss` measures every other shape. File
    pages are never counted.
  - (B) Keep the two peaks and widen the slack past the file pages' spread, which is at least 1 MB on the runner. The
    gate would then pass real growth of up to about 300 B a turn.
  - (C) Keep the two peaks and take the smallest of several runs of each size. That is slower, and still exposed to a
    page-cache jump that lasts across runs.
  - **A**: it measures what the gate is for ("each command's scratch dies with it"), and its spread is 8 KB where the
    peaks' is over 1 MB. It also follows sh35's rule for `shape-rss` (never count file-backed pages on Linux). The
    planted growth rows (`LoopRssMetric`) show it still fails a loop that keeps memory.

## Evidence index

Commits (base `f0761dc1`):
- `95ff390`: the prediction, before any change or new measurement.
- `15a9956`: the rows, red first. `LoopRssMetric`'s stand-in shell maps file pages (must pass) or keeps anonymous
  memory (must fail).
- `f8cfe61`: the fix. `loop-rss` measures the loop's kept memory in one process on Linux.
- The note and its evidence, in `notes/sh37b/`, with paths removed:
  - `ci-runs.txt`: the failing job's and `b514e14`'s `loop-rss`, job-wait and loop rows, and their idle witnesses'
    `RssFile`;
  - `peaks-linux.txt`: the two-process peaks with `RssAnon` and `RssFile`;
  - `metric-rows.txt`: the rows red then green, the two metrics side by side, and the traces;
  - `env-loop.txt`: the loop under three environments.

## Done-when

- [x] Reproduced on the CI shape as far as a host other than the runner allows. The mechanism reproduced: file pages
  swing the two-process peak by up to a megabyte at either head. The 3,040 KB did not, in 64 two-process comparisons.
  How the loop's memory varies with the environment was measured too: it doesn't, and neither identity fallback nor
  `signal_park` runs in the loop.
- [x] What grows per turn since `b514e14`: nothing. The loop's kept memory is 31–35 B a turn at both heads.
  `os_signal_wait_fds` on the kept list keeps nothing per call (CI's job-wait rows, same bytes a turn).
- [x] A row red first on that shape (`test_mapped_program_pages_are_not_growth` at `15a9956`), then the fix
  (`f8cfe61`, per R-sh37-5 A).
- [x] The changelog. The README is unchanged: its memory row still names `tools/loop-rss` and says "almost nothing".
- [ ] The gauntlet at the head and the plant, red by name. Their END lines are in the PR body, taken after this note.
- Fixes pelt#118.
- Left for a cross-cutting change: the workflow's comment above the `loop-rss` step still says the larger run "may
  peak" above the smaller, which now holds on macOS only.
