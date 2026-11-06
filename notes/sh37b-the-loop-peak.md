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
