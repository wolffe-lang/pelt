# sh38c — the close rows' race: the kernel's SIGHUP to the foreground job

Base: pelt trunk `3e6d90b` (wolf 0.2.36, lupin 0.1.58, std `78b9d3cb`). Clean room: no shell's or kernel's
source; bash and pelt were asked from outside, through `tools/hangup-witness`, in the Ubuntu 24.04 image the
gauntlet uses.

## 0. The red, and the prediction

Trunk `3e6d90b`'s push run 43405897269, job `gauntlet (ubuntu-latest, true, native)` (job 131820136161), step
`tools/signal-witness`: `hangup-witness: 45 of 46 rows hold, 1 fail, 0 skipped`, the one

    FAIL mixed-close
      expected: … | mf CONT:kernel+HUP:kernel+HUP:shell dead:HUP
      got:      … | mf CONT:kernel+HUP:shell dead:HUP

The same row held in the full runs of #125 and #127 and on the run's other linux legs, and #127 changed no hangup
file: the foreground probe `mf` did not record the kernel's SIGHUP that time.

**Prediction.** On a close, the foreground job gets two SIGHUPs: the shell's, and then the kernel's (with a
SIGCONT) as the shell, its terminal gone, exits (POSIX `_exit()`: a controlling process's exit sends SIGHUP to its
terminal's foreground process group). A standard signal generated while one is pending is not queued again (POSIX
leaves it to the implementation; linux keeps one, and the first one's siginfo). So when the shell exits before the
job has taken the shell's SIGHUP, the two are one, which names the shell, and the kernel's goes unrecorded. If so:
the kernel's SIGHUP is the only one ever missing, the shell's is always first and always recorded, the kernel's
SIGCONT is recorded either way, bash's rows show the same, and the rate rises with contention for the CPUs. Every
`-close` row with a foreground job (`fg-close`, `mixed-close`, `pipe-close`, `subshell-close`) has it.

## 1. The race, measured

`notes/sh38c/race.py` boots rows through the witness's own row code again and again and tallies the lines; the
runs are on a 2-CPU light slot (the rows, the shell and the harness on two CPUs), in the Ubuntu 24.04 image.

**At trunk** (the witness and pelt of `3e6d90b`; the table's line, then each other line seen):

| row | N | holds | the line it failed with |
|---|---|---|---|
| `mixed-close` | 600 | 553 | `mf CONT:kernel+HUP:shell dead:HUP`, every time |
| `fg-close` | 200 | 194 | `fg CONT:kernel+HUP:shell dead:HUP` (6) |
| `pipe-close` | 200 | 174 | `pf1` or `pf2` or both `CONT:kernel+HUP:shell dead:HUP` (26) |
| `subshell-close` | 200 | 158 | `sf1 CONT:kernel+HUP:shell dead:HUP` (42) |

In every failure the kernel's SIGHUP is the one missing; the shell's SIGHUP and the kernel's SIGCONT are always
there, and every other probe in the rows reads as the table has it (`ms` received the shell's SIGTERM in every
one of the 600 `mixed-close` boots).

**When each comes.** The probe now records each signal's time (CLOCK_MONOTONIC, ms) and its parent then, and a
`stay` probe records every signal and outlives all (§2). Thirty boots of each of the four rows and of their
`-caught` twins (`notes/sh38c/close-timing.txt`, from `notes/sh38c/close-timing.py`): in all 240, the shell's
SIGHUP came first and the kernel's SIGHUP and SIGCONT after it, 0-1 ms later for a `stay` probe (10-11 ms for
a plain probe, which after its first signal takes the rest every 10 ms); never the kernel's first. The kernel's
SIGHUP went unrecorded for 47 of the 300 foreground probes (23 of 150 plain ones, 24 of 150 `stay` ones): a probe
that outlives every signal loses it as often, so it is not that the probe died first, and the kernel's SIGCONT, which
was recorded every time, shows it was alive and catching when the kernel's signals came. A SIGHUP it catches can
be lost only by joining one already pending: the shell's.

**bash 5.2.21** through the same witness shows the same in its own rows: in one take of the whole table
(`notes/sh38c/bash-5.2.21.table`, its `as seen` lines) `subshell-close`'s `sf1` and the `stay` probes of
`mixed-close-caught`, `pipe-close-caught` and `subshell-close-caught` read `CONT:kernel+HUP:shell`. It is the
system's, not pelt's.

## 2. The change

- The probe records, in each `sig` and `die` line, when (CLOCK_MONOTONIC, ms) and its parent then. A `stay`
  probe (`hw-probe NAME stay`) catches every signal and dies of none; it records each and ends itself 300 ms
  after its parent is gone (END `ended`).
- A `-close` row's foreground probe (the row option `hung`) is held to what the system promises: SIGHUP reached it,
  from anyone (`HUP`), and it died of SIGHUP; any other signal but SIGCONT as it came. `fg-close`'s line is
  `fg HUP dead:HUP`.
- Each of the four has a `-caught` twin whose foreground probes `stay`, held to every signal the shell (not the
  kernel) sent them, exactly: `fg-close-caught | shell signal:HUP | fg HUP:shell ended`. That proves the shell's
  own SIGHUP without depending on what the kernel's did: the shell's comes first, before the shell exits, and a
  later one joining it keeps its sender.
- A failing row prints what it saw with every sender (`as seen`), and `--measure` prints it as a comment.

Every other row and every probe that is not a close's foreground job is held as before; macOS skips the close
rows, as it did. The eight lines are bash 5.2.21's, measured through the changed witness (in that take bash's
`stopped` rows lacked the exit path's SIGTERM, bash's own race that sh38's note records for 5.3.20; the table
keeps pelt's, as before).

## 3. After

At `1ff4c43` (the change; pelt unchanged), the same slot:

| row | N | holds | the kernel's SIGHUP unrecorded underneath (the race, as seen) |
|---|---|---|---|
| `mixed-close` | 600 | 600 | 36 |
| `mixed-close-caught` | 600 | 600 | 43 |
| `fg-close` | 200 | 200 | 13 |
| `fg-close-caught` | 200 | 200 | 15 |
| `pipe-close` | 200 | 200 | 19 (`pf1`, `pf2` or both) |
| `pipe-close-caught` | 200 | 200 | 20 |
| `subshell-close` | 200 | 200 | 25 |
| `subshell-close-caught` | 200 | 200 | 26 |

(`notes/sh38c/after.tally`; `mixed-close` and its twin in two runs of 300, one on each of two slots.) The race is
still there underneath, at the rate it was (`mixed-close` 36 of 600 after, 47 of 600 before), and no row sees it:
every `-caught` probe recorded the shell's SIGHUP in every boot.

## Evidence index

The measurements, in `notes/sh38c/` (sha256):

- `race.py` `afac2036…`: boots rows through the witness's own code and tallies them.
- `before.tally` `8b57886f…` and `after.tally` `b2eee6c1…`: its tallies at trunk and after the change.
- `close-timing.py` `c5c232aa…` and `close-timing.txt` `9be573ed…`: the 240 boots' signals in order, with times.
- `bash-5.2.21.table` `887f7c48…`: bash through the changed witness, every row, with the `as seen` lines.

The gauntlet records at the head (linux's and the Mac's) and the plant's are cited in the pull request.

## Forbidden

- Read no shell's source and no kernel's: bash and pelt were asked from outside.
- Signal only pids this lane started, never a group; nothing in /tmp on any host.
- Change no row but the close rows' foreground probes; keep macOS as it is.

## Inputs verified

- The red: run 43405897269, job 131820136161's log, read once (the FAIL lines above).
- bash 5.2.21 (Ubuntu 24.04's 5.2.21-2ubuntu4) in the Ubuntu 24.04 image, linux 7.2.4.

## Done-when

- Every close row and twin holds in every boot after the change, and the rate before is measured (§1, §3).
- linux's and the Mac's witness hold every row at the head; the plant is red by name.
