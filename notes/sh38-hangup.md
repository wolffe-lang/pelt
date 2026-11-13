# sh38 — a hangup reaches the jobs, and a sweep of the open issues

Base: pelt trunk `b80d6570` (wolf 0.2.36, lupin 0.1.58, std `78b9d3cb`). Clean room: no shell's source. bash and
dash ran only as black boxes, through a pseudo-terminal, in containers.

## 0. The prediction (written before the first change)

**Why.** PAX's measurement of its installed shape found that when an ssh connection drops while a foreground
`sleep 100` runs, the session's pelt dies of SIGHUP and the sleep runs on until shutdown. bash(1) says an
interactive shell that receives SIGHUP resends it to all its jobs, running or stopped, and sends SIGCONT to the
stopped ones so they receive it, before it exits; `disown` takes a job out of that, and `disown -h` marks it. dash
resends nothing, and pelt has matched dash. On Linux the kernel covers part of the gap: when a session's
controlling process exits, its terminal's foreground group gets SIGHUP, and a process group left orphaned with a
stopped member gets SIGHUP and SIGCONT (POSIX `_exit`, XBD 11.1.3 and 11.1.10). Background jobs that run get
nothing. PAX's kernel did not send the foreground group anything, so there even the foreground job survived.

### The witness

`tools/hangup-witness` starts a shell on a fresh pseudo-terminal, as a terminal or an ssh server does: a new
session, the pty its controlling terminal, every signal at its default and nothing blocked. It types commands that
start a probe (`hw-probe NAME`, a small C program the tool compiles) as jobs: in the foreground, after `&`, stopped
by the suspend character (the byte 0x1a written into the pty), in a pipeline, in a subshell, `disown`ed, under
`nohup`. Then it hangs the shell up, either by sending SIGHUP to the shell's pid (`kill` rows) or by closing the
pty's master, as a dropped ssh connection does (`-close` rows). Each probe records every signal it gets and its
sender, from `siginfo`: `shell` is the shell's pid, `kernel` a signal the kernel made. Each probe then dies of the
first signal whose default would end it, 150 ms later, so that signals sent together are all seen. A probe started
with a signal ignored keeps it ignored. The `kill-*` rows send no hangup: they type `kill` at a stopped job and look
a second later. A row is one line: the shell's end, then each probe's signals and its end.

### The table, measured

bash 5.2.21 (Ubuntu 24.04's 5.2.21-2ubuntu4) and dash 0.5.12 (Ubuntu's 0.5.12-6ubuntu5), in an Ubuntu 24.04
container, every row; bash took the first 38 rows twice, identical. pelt at trunk `b80d6570` (native) in the same
container. The full lines are in `notes/sh38/` (`bash-5.2.21.table`, `dash-0.5.12.table`, `pelt-b80d6570.table`,
and bash's raw probe logs). In short (S = from the shell, K = from the kernel):

| row: what is typed, then the hangup | bash | dash, and pelt at trunk |
|---|---|---|
| `fg`: a foreground job | HUP(S); dies of HUP | HUP(K) when the shell exits |
| `bg`: two jobs after `&` | each HUP(S) | nothing; both run on |
| `stopped`: two jobs stopped by ^Z | each HUP, CONT, TERM (S) | HUP, CONT (K): the orphaned group |
| `mixed`: one of each | as above, each by kind | the background one runs on |
| `pipe`: `a \| b &` and `c \| d` | every process HUP(S) | the background pipeline runs on |
| `subshell`: `(a; b) &` and `(c; d)` | a and c HUP(S); b and d never start | the background subshell runs on |
| the six again with the pty closed | the same from the shell; the foreground also HUP, CONT (K) | the same as `kill`, from the kernel |
| `disown`: `a &`, `disown`, `b &` | a nothing, runs on; b HUP(S) | `disown` not found; both run on |
| `disown -h`, `disown -a` | the marked or removed job nothing | not found |
| `disown` of a stopped job | bash warns, deletes it; K sends HUP, CONT (orphaned) | not found |
| `disown -h` of a stopped job | no HUP; TERM, CONT (S) as the shell exits | not found |
| `nohup a >/dev/null 2>&1 &`, `b &` | a ignores HUP, runs on; b HUP(S) | both run on |
| `trap 'echo trapped' HUP` at the prompt, a job | the action runs, the shell then exits 0; the job nothing | the action runs, the shell goes on |
| the same with a foreground job | the shell goes on; the job nothing | the shell goes on |
| the shell started with HUP ignored | dies of HUP; the job (HUP ignored, inherited) runs on | the shell lives |
| `exit` with a job running | exits 0; the job runs on (`huponexit` is off) | the same |
| `exit` twice with a job stopped | warns once; exits 1; TERM, CONT (S) to the job | warns; exits 0 (dash), 148 (pelt); HUP, CONT (K) |
| Ctrl-D twice with a job stopped | warns once; exits 148; TERM, CONT (S) | dash warns once, then exits 148; pelt exits at the first Ctrl-D, no warning |
| a script: `a &` then `b` | dies of HUP; a and b HUP from K (the shell's own group was the terminal's) | the same |
| `kill %1` (also `-TERM`, `-s TERM`, `-HUP`) on a stopped job | TERM (or HUP) then CONT (S): it dies | it stays stopped, TERM pending |
| `kill -INT`, `-QUIT`, `-USR1`, `-STOP %1` on a stopped job | no CONT: it stays stopped | the same |
| `kill -CONT %1`; `kill -KILL %1` | continues; ends | the same |
| `kill PID` (the job's pid) | no CONT: stays stopped | the same |
| `kill -- -PGID` (the job's group) | TERM then CONT: dies | stays stopped |
| `kill %1` on a pipeline, `kill %1 %2` | every process TERM, CONT | all stay stopped |
| `kill %1` on a background job stopped by `kill -STOP %1` | TERM, CONT | stays stopped |

The friendly prompt (pelt invoked as `pelt`), `TERM=dumb` (no line editor) and a half-typed line at the hangup
are rows of their own, the same as `bg` for bash.

### What pelt will do (the rows it is held to)

`tests/hangup/expected` is bash's table line for line, except three fields, each a recommended decision (below):

1. **A hangup (R-sh38-6).** An interactive pelt listens for SIGHUP from its start (unless it was started ignoring
   it, or a trap names it), wherever it is: at the line editor, reading a line without one, waiting for a
   foreground job, in `wait`, or between commands. On SIGHUP it sends SIGHUP to the group of every job it has not
   disowned or marked with `disown -h`, and SIGCONT after it to each stopped one; it ends its stopped jobs as an
   exit does (item 4); it gives the terminal back to its own group; and it dies of SIGHUP, so its parent sees the
   signal (`os_exit_signal`). Predicted: every `kill` and `-close` row red at trunk (`bg`, `stopped`, `mixed`,
   `pipe`, `subshell`, `fg` by its sender, the friendly, dumb and half-typed rows), green after.
2. **`disown`** (pelt has none): bash's built-in, `disown [-h] [-ar] [job ...]`. Without operands the current job;
   `-a` every job, `-r` the running ones; `-h` marks a job so a hangup does not reach it and keeps it in the table.
   A removed job is no longer listed, waited for or named by a job id, and its processes are still reaped. A stopped
   job removed draws pelt's own warning. Red at trunk (not found), green after.
3. **`kill` continues a stopped job (R-sh38-1).** After `kill` sends SIGTERM or SIGHUP to a job's group (a job id,
   or `-PGID` naming a job's group), a job that is stopped gets SIGCONT, so the signal is delivered. A process id,
   and every other signal, stay as they are. Red at trunk for `kill-stopped`, `-term`, `-s-term`, `-hup`,
   `-group`, `-pipe`, `-two`, `kill-bg-stopped`; green after. The others are green at trunk and stay so.
4. **The exit with stopped jobs.** As bash: the second `exit`, the second Ctrl-D and a hangup send each stopped job
   SIGTERM and SIGCONT. Ctrl-D with a stopped job warns once first, as `exit` does (dash and bash both; pelt left at
   the first). Red at trunk for `exit-stopped`, `exit-stopped-bg`, `eof-stopped`, `disown-h-stopped`.
5. **Unchanged**: the script rows (a non-interactive shell resends nothing: bash's own rule), `exit` with a
   running job, `nohup`, the `kill` rows bash leaves stopped, and both trap rows' jobs.

Expected red at trunk: 30 of the 46 rows (`fg`, `bg`, `stopped`, `mixed`, `pipe`, `subshell` and their six
`-close` rows, `disown`, `disown-h`, `nohup`, `disown-h-stopped`, `exit-stopped`, `exit-stopped-bg`, `eof-stopped`,
`friendly-bg`, `dumb-bg`, `editing`, and the eight `kill` rows of item 3). `disown-stopped` and `disown-all` are green
at trunk by accident (pelt has no `disown`, sends nothing, and the kernel's orphaned-group rule gives what bash's
removal leads to). After the change, all 46 green on Linux. On macOS the six `-close` rows and `script-close` are
skipped by name (the kernel's part of a hangup is the host's).

The rows run in pelt's gauntlet through `tools/signal-witness`, which runs the hangup witness after its own rows,
so CI's step list is untouched (R-sh38-7).

### Recommended decisions

- **R-sh38-1, `kill` on a stopped job.** (A) bash's: SIGTERM or SIGHUP to a stopped job by job id or by its group
  is followed by SIGCONT; (B) dash's: the signal waits until something continues the job. **A**, as the hangup
  follows bash: on PAX's measured console a `sleep` stopped by Ctrl-Z stayed stopped after `kill %1`, so the
  command did nothing until `fg`. Reversing it is one call in `bi_kill`.
- **R-sh38-2, a shell started with SIGHUP ignored.** bash -i dies of a SIGHUP even so (its jobs inherit the
  ignore and run on); dash and pelt keep it ignored, as XCU `trap` requires of a non-interactive shell and allows of
  an interactive one. (A) keep pelt's rule: a signal ignored at entry stays ignored in every shell, so `nohup pelt
  -i` outlives a hangup on purpose; (B) bash's. **A**: the rule is pelt's for every signal and `signal-witness`
  holds it (`ignored-i`); the table's `ignored` row says `shell alive`.
- **R-sh38-3, a trapped SIGHUP at the prompt.** bash runs the action and then leaves at once with status 0, as if
  its line had ended; with a foreground job it runs the action and goes on. (A) pelt runs the action and goes on in
  both (POSIX `trap`, and bash's own foreground row); (B) leave after the action at the prompt. **A**; the `trap`
  row says `shell alive`.
- **R-sh38-4, `$?` after a refused `exit`.** bash 1, dash 0, pelt at trunk the status before it (148 after a
  ^Z). (A) dash's 0, which the session corpus is recorded from (`c_jc_ctrl_z` and `c_jc_exit_stopped` exit with
  it); (B) bash's 1, which would make `c_jc_ctrl_z` differ from its transcript. **A**; the two `exit-stopped` rows
  say `exit:0`.
- **R-sh38-5, `disown`'s reach.** (A) a regular built-in in every shell, as `jobs`, `fg` and `bg` are; (B) only
  when interactive. **A**: bash has it in scripts too, and a script with no job control still has jobs.
- **R-sh38-6, where the shell listens.** (A) from the start, an interactive shell's own meaning like INT, QUIT and
  TERM (one disposition, every wait adds it); (B) only while jobs exist. **A**: one rule, no window in which a
  job starts unheard; a shell with no job dies exactly as before.
- **R-sh38-7, the witness's place in CI.** (A) inside `tools/signal-witness`'s step, which CI already runs on every
  leg that builds; (B) a CI step of its own, a change to the workflow (cross-cutting). **A** for this change; B can
  ride the next change that touches the workflow.
- **R-sh38-8, the friendly prompt's `den status`** (measured in §4; the default is unchanged). (A) keep it as it is:
  synchronous, bounded at 50 ms, the last value dimmed when late; (B) asynchronous: start the probe as the prompt is
  drawn and redraw the segment when it answers; (C) keep (A) and stop asking in a directory where it has missed its
  deadline a few times in a row, until the next `cd` or a later prompt (a back-off). Recommendation in §4.
- **R-sh38-9, pelt#69's image.** `bash-5.3.20-2`, the package the second opinion was recorded with, never reached
  archive.archlinux.org, so `tools/oracle-image` refuses by design. (A) pin `bash-5.3.20-1` (same upstream release,
  an earlier package build; in the archive, digest `73a67dc5…`) and build the image; (B) wait for `-2`, which the
  archive still lacks, as when sh33 asked for it; (C) move the second opinion to the newest bash in the archive and
  re-record. **A**, in the change that adds the CI job (a workflow change, so cross-cutting); not done here.

The sweep's outcomes are in §3; its two changes (pelt#93's witness, pelt#97's case) were each predicted in their
commit's own row, not in this section (a correction to the contract's order, said here).

## 1. How the prediction held

It held, row for row. At trunk `b80d6570` pelt's table was dash's (`notes/sh38/pelt-b80d6570.table`) but for two
rows: `exit-stopped` answered 148 where dash answers 0, and at `eof-stopped` pelt left at the first Ctrl-D, where
both oracles warn once. The 30 rows named above differed from `tests/hangup/expected`, the 16 others matched. pelt
has no `disown` at trunk, so its `disown` rows ran with `disown: not found`.

The first build of the change (`d5eb28b`, the tree of `2655b6c`) held all 46 rows (`hangup-witness: 46 of 46 rows
hold`), with no row adjusted after the fact. Two rows of other steps went red with it and were mended in their own
commits: `self-check`'s two `interactive_set` table checks (they counted three meanings; there are four now) and
`check-fmt` (one condition wolf fmt writes on five lines).

The same rows taken after the change with bash 5.3.20-1 and dash 0.5.13.4-1 (the Arch oracle image in Inputs verified;
`notes/sh38/bash-5.3.20.table`, `dash-0.5.13.4.table`, one take each): dash 0.5.13.4's table is 0.5.12's line for
line. bash 5.3.20's differs from 5.2.21's in five rows, all in one way: a foreground job (`fg`, `mixed`'s `mf`,
`pipe`'s `pf1` and `pf2`, `subshell`'s `sf1`, `friendly-bg`'s `ff`) gets SIGHUP from the kernel as well as from the
shell, so 5.3 dies with the terminal still the job's, where 5.2 hands it back to its own group first. Every job gets
the shell's SIGHUP in both. pelt follows 5.2's table, which is the one it is held to: the terminal goes back first,
so the host's hangup of the foreground group does not repeat the shell's.

Where pelt listens: an interactive shell's SIGHUP is its own meaning from the start, like INT, QUIT and TERM
(`sh.signal`'s `interactive_set`), so a program it starts begins with the default. A SIGHUP is answered at the line
editor (its wait already took it), in the read without an editor (a wait on the terminal and the signal, then the
read), in a job's wait and the fast path's foreground wait (the signal joins the park), and between commands
(`poll_traps`). The answer is `sh.jobs`'s `hangup`, which reads the job table with the changes `jc_take` holds
counted (a job stopped by `kill -STOP` while a line was typed is stopped there), sends, gives the terminal back to
the shell's group, and ends the process with `os_exit_signal`, so the parent reads a death by SIGHUP. A subshell pelt
runs in process answers a SIGHUP only when the top level would (`hup_own`): one the top level traps stays queued
until that shell runs again, as `trap`'s other signals do.

## 2. The proof on PAX (a row for the pax lane)

PAX's system-log rig (`notes/px130/rig/measure.py` on pax's `px130` branch) already has the shape: session `s3`
types `sleep 100` in the foreground and then kills the ssh client, so the connection drops. pax is not edited here.
With pelt at this branch's head pinned on the image, its `table.txt` should hold, under `s3:end`, within the four
seconds the rig pumps after the drop:

```text
s3:end	user: pelt pid P killed: SIGHUP
s3:end	user: sleep pid S killed: SIGHUP
```

where `S` is the `sleep` the session started (narrated as `exec` without `quiet`). At trunk the second line is
missing and `sleep` runs until the machine stops. A second row, for the jobs a foreground row does not cover:

```python
session(con, 's3b', [('sleep 100 &', b'sleep 100 &\r', P), ('sleep 200 &', b'sleep 200 &\r', P),
                     ('sleep 300 (Ctrl-Z)', b'sleep 300\r', 1.5), ('Ctrl-Z', b'\x1a', P)], out, 'drop')
```

expects three `user: sleep pid N killed: SIGHUP` lines under `s3b:end` beside pelt's, one per sleep. (On Linux the
stopped one also gets SIGTERM after SIGHUP and SIGCONT; it dies of whichever is delivered first, SIGHUP on Linux.)
`s2` (`sleep 100 &`, then `exit`) keeps its sleep running after a clean exit, as bash's does (`huponexit` is off):
under `quiet` no line, and without it the sleep's `exit_group 0` about 100 s later. The rig's own measurement
showed PAX's kernel not hanging up the terminal's foreground group when the controlling process ends (XSH `_exit`:
the foreground sleep ran on); whether it sends SIGHUP and SIGCONT to a process group orphaned with a stopped member
(XBD 11.1.10) is not measured, and is worth a row of its own (`disown` a stopped job, then drop the session). pelt
now covers both for its own jobs, not for a `disown`ed one.

The commit to pin on PAX is this branch's head, named in the PR.

## 3. The sweep: pelt's ten open issues

Each was looked at against trunk `b80d6570` (native, Linux, in the container, unless named).

| issue | at trunk | outcome |
|---|---|---|
| #93 nightly red | The last three scheduled runs are green (43263891708, 43058026087, 42855089225). The two reds since sh37 were each a macOS leg: run 42678757228 (11-09) failed `prompt-vcs-real-probe` in `tools/prompt-witness`, and run 42066187159 (11-05) failed the same row and timed out `tools/shape-rss` (20 minutes), the second the hang sh37 bridged (pelt#114, merged the next day). | **Fixed, and closable.** The row's stand-in `den` was a Python script, whose start alone outran the first prompt's 50 ms probe budget on a macOS runner (the prompt showed no `[vcs:1]`). It is a POSIX sh script now (`ae55dd6`): on this Mac, warm, 5 ms against Python's 24 ms. Seen red: the two runs above, by name. |
| #97 `printf %a` uncounted | `printf '%a %a %a' 1 0.5 -2.75` answers `printf: %a: conversion not supported`, status 1, and the census counted printf/8 as met. | **The case and the count.** `printf/c_hex_float` (pending `printf-hex-float`) names the gap; printf/8 is pending and the census reads 532 of 548. The issue says dash has no `%a`: dash 0.5.13.4 has it, a binary64 conversion (`0x1p+0 0x1p-1 -0x1.6p+1`), and `bash --posix` agrees, so the case is dash's like any other; only plain bash, outside POSIX mode, converts with a long double (`0x8p-3` for 1 on x86-64). `%a` itself is a later lane's. |
| #117 remove `signal_park` | The bridge is in trunk (`sh.signal`'s `signal_park`, two call sites). wolf 0.2.37, 0.2.38 and 0.2.39 are released. | **Not this lane's.** It is the toolchain pin's: moving pelt to 0.2.37 or later is a cross-cutting change (pins, CI). Then remove the bridge, and show the #114 row red with it removed at 0.2.36 and green at the new pin. |
| #98 the stalled `wait` | `tools/wait-replay --runs 3` at trunk: 3 green, 0 stalled (each 30.5 s). The bridge holds it. | **Closes with #117's pin**, as its own text says. |
| #110 a lost prompt in shape proof run 89 | Not reproduced: `tools/shape-rss --only typed-fork-subshell` twice at trunk, 20,000 typed turns each (ok, 126 B a turn); the gauntlet's two `shape-rss` steps at the head type it twice more. | **Stays open**: one red in 128 whole runs, and none in the 200 instrumented ones or these. It needs a failure caught with sh35's snapshots, not a code change. |
| #83 `script-simple` jumped on a runner | The jump was the old metric: peak RSS of two processes, file pages included. Since sh35 `tools/shape-rss` reads the shell's own `Anonymous + Swap` in one process (`metric=Anonymous+Swap`): at trunk `script-simple` grew 44 KB over 10,000 turns, twice. | **Closable**: the instrument no longer counts the page cache that made the step; no shape-rss red on a hosted runner since, but for the 11-05 hang above. |
| #69 a pinned oracle image | `tools/oracle-image` exits 2 at its first check: `BLOCKED: exact archive unavailable` for `bash-5.3.20-2`. The archive still has no `-2`; it has `5.3.20-1`. | **Not small**: the CI job is a workflow change (cross-cutting), and pinning `5.3.20-1` is a decision (R-sh38-9). This lane built such an image for its own recording (Inputs verified), which shows `-1` installs at the pinned base. |
| #65 `$'\377'` | `$'\377'` and `$'\xff'` are refused: `a byte that is not UTF-8 cannot be carried yet (pelt#65)`. | **Not small**: neither wolf 0.2.36 nor 0.2.39 can pass a byte that is not UTF-8 to a program (`os_spawn_fds`, `os_exec`, `env_set` take `str`). It waits on wolf's byte arguments (W06, wolf-lang#687, #912). |
| #20 bytes cannot leave pelt | The three `non-utf8-bytes` cases are `PEND-fail` (`quote/c_s_high_bytes`, `c_ds_octal_high`, `c_ds_hex_high`). | **Not small**, the same wait as #65. |
| #57 forked shapes cost | Unchanged code since sh26 measured it. | **Not small**: it needs a cheaper start for a stage pelt runs itself (a `vfork`-shaped or `posix_spawn`-shaped path, or not forking for a pure built-in stage), a design of its own with the bench. |

Issues to close by hand at the merge: pelt#93 (nightly green three nights; the flake's cause fixed here) and
pelt#83 (the metric it asked about is gone). pelt#97 stays open for `%a` itself.

## 4. The friendly prompt's `den status`, by repository size

`notes/sh38/den-cost.py`: den built (release) at its trunk `a749692d` with the same wolf 0.2.36 pin, pelt at this
branch (native), in the Ubuntu 24.04 container on two CPUs. Each repository has N files in directories of 200,
committed, then 60 changed. `status` is `den status --porcelain` run directly (median of 15); `prompt` is Enter to
the next friendly prompt with `true` typed (median of 15), and what the segment showed; `baseline` the same prompt
with no `den` on `PATH`.

| files | `den status --porcelain` (median, max) | the prompt with den (median, max) | the segment, of 15 prompts | the prompt with no den |
|---:|---:|---:|---|---:|
| 10 | 0.9, 1.1 ms | 2.8, 3.0 ms | fresh 15 | 4.3 ms |
| 100 | 2.2, 2.9 ms | 4.1, 4.3 ms | fresh 15 | 4.3 ms |
| 400 | 6.7, 6.9 ms | 11.2, 11.7 ms | fresh 15 | 4.3 ms |
| 2,000 | 30.7, 32.0 ms | 31.5, 36.7 ms | fresh 15 | 4.4 ms |
| 3,000 | 43.4, 47.8 ms | 46.0, 52.2 ms | fresh 15 | 4.2 ms |
| 5,000 | 79.1, 85.5 ms | 57.4, 58.1 ms | none 15 | 4.6 ms |
| 10,000 | 161.7, 165.6 ms | 54.8, 63.2 ms | none 15 | 4.5 ms |
| 20,000 | 330.6, 352.1 ms | 57.3, 67.2 ms | none 15 | 4.0 ms |

What it says:

- **den's own cost grows about 16 µs a file** on this Linux host: under 7 ms at 400 files, 31 ms at 2,000, 43 ms at
  3,000, and past the prompt's 50 ms deadline from about 3,300 files.
- **The bound holds.** Past the deadline every prompt costs 55–63 ms with den on `PATH` (the 50 ms budget, then the
  probe's kill and reap), against about 4.5 ms without, however large the repository grows: 10,000 files cost what
  5,000 did, and 20,000 (330 ms for den alone) about the same. The prompt never waits for den's full answer.
- **Past the deadline the cost buys nothing.** In a repository den cannot answer within 50 ms the segment is never
  drawn (`none` on all 15 prompts: with no earlier answer in that directory there is no dimmed value to show), and
  each prompt still spends its 50 ms.
- **On PAX the line is lower.** PAX's own system-log rig (pax's `px130` branch) built its large case at 400 files
  because den status ran past the deadline there, where this host answers in 7 ms; the same pelt there pays the full budget at every prompt in any repository of a
  few hundred files.
- Two things in den, seen on the way and not pelt's (to file there): `den add .` of 5,000 or more new files ended by
  SIGKILL under the container's 6 GiB memory cap (each `den add` of one 200-file directory grew to about 620 MB),
  and one commit of 3,000 new files answers `den: not yet implemented: commit rename summary budget` (exit 2), so
  the rows past 2,000 commit a directory at a time.

**R-sh38-8, recommended: (C), a back-off on top of the bound.** Keep the 50 ms bound (A); after two misses in a row
in one directory, stop starting den there until the directory changes, and draw nothing (or the last answer,
dimmed) meanwhile. That turns 50 ms a prompt into nothing in a repository den cannot answer in time, which on PAX is
most of them, and keeps every answer that is in time. (B), an asynchronous probe, would show the late answer but
needs a child running while the prompt is idle and a redraw of the prompt from under the line being typed; that is
what `docs/FRIENDLY.md` rules out today ("no background process or idle cache refresh"), and a cost an idle PAX
console would pay. The default is unchanged in this branch, as the contract asks; C is a small change in
`sh.edit_prompt`'s `prompt_prepare` once ruled.

## Forbidden

- No shell's source was read: bash and dash ran only as black boxes, through a pseudo-terminal, in containers;
  wolf's spec was read at the pin (`spec/11-os.md`), and its runtime not at all. den's source was not read either:
  it was built and run.
- No attribution trailer in any commit or in the PR. No label, merge, tag, release, or issue filed or closed. CI was
  not waited on.
- Signals went only to processes this lane started, inside containers: the shells under test (each this lane's
  child), and the probes they started, which the witness ends by pid after checking each one's command line; the
  suspend character was a byte written into the pty. Nothing by process group, `pkill` or `pgrep -f`. Nothing in
  `/tmp`: every job's `HOME` and `TMPDIR` sat under the lane's own directory.
- No build ran on the Mac (it had 15 GB free, at the floor). Every Linux job ran in a container behind its host's
  locks, with a pid file, a log and an exit marker; the light jobs on two CPUs, the gauntlet on four behind both of
  a block's locks. On the hosts themselves only git, the toolchain fetch, the oracle image's build (through the
  light slot) and one read-only `den log` (to see a job's progress) ran. No process was ended but the witness's own
  probes.

## Inputs verified

- Base: pelt trunk `b80d6570`. Toolchain staged by `tools/fetch-toolchain`, each archive checked against its pin:
  wolf 0.2.36 `d383c74c…` (`wolf 0.2.36 (wolfgang, pin 5adf3d9)`), lupin 0.1.58 `34f52792…`, std `78b9d3cb`.
- The containers: `localhost/r41-toolchain:1`, id `77fdad6b…`, Ubuntu 24.04 (bash 5.2.21-2ubuntu4, dash
  0.5.12-6ubuntu5, gcc 13.2, python 3.12.3), the same id on both Linux hosts used; and `localhost/sh38-oracle:1`,
  id `71776517…`, built by this lane from the Arch base pelt's `tools/oracle/Containerfile` pins
  (`archlinux@sha256:8185e444…`) with `dash-0.5.13.4-1` (`e6170d47…`, the digest `tools/oracle/packages.sha256`
  names) and `bash-5.3.20-1` (`73a67dc5…`) from archive.archlinux.org, each read twice, and python 3.14. Re-recording
  the `jobs` and `printf` areas there changed no existing case's expectation: the image answers as the oracle of
  record does on them (dash 0.5.13.4; bash 5.3.20, the second opinion, as package `-1` where `tests/diff/ORACLE`
  names `-2`).
- wolf 0.2.36 and 0.2.39 have no way to pass a byte that is not UTF-8 to a program (`os_spawn_fds`, `os_exec`,
  `env_set` take `str`; only `env_args_bytes` answers bytes), read in their `spec/11-os.md`.
- archive.archlinux.org has `bash-5.3.20-1` (sha256 `73a67dc5…`, read twice) and no `bash-5.3.20-2`.

## Evidence index

Commits (base `b80d6570`):
- The prediction and its rows, before any change: `5ffa317` the prediction (bash's table, what pelt will do);
  `b466290` `tools/hangup-witness`; `637fcd9` the measured tables (bash 5.2.21, dash 0.5.12, pelt at trunk);
  `5516975` `tests/hangup/expected`; `b2f106b` the rows run in `tools/signal-witness`'s step.
- The hangup: `167f458` (`hup_own`), `efbcb4c` (SIGHUP an interactive shell's own meaning; `poll_traps` hangs up),
  `13e7ca7` (`hangup`, `disown`, `kill_continue`, `jc_end_stopped` in `sh.jobs`), `8fe1585` (the line editor),
  `d80f758` (the read without an editor; Ctrl-D with a stopped job warns once), `9c00b9e` (the fast path's wait;
  `disown` a regular built-in), `9066d8b` (`disown` run; a refused `exit` answers 0), `ec2c96e` (`kill` continues a
  stopped job), `958aa8d` (the stopped jobs end with the shell), `2655b6c` (completion's description).
- Mended after the first build: `7975235` (`check-fmt`), `10e91da` (`self-check`'s `interactive_set` rows, and new
  ones for HUP's subshell rule and `hup_now`), `5fc06ab` (comments point at this note), `788d74e` (the witness never
  writes a bare `SKIP` at column 0).
- Mended after the first gauntlet take: `d44406b` (the idle rows of `shadow-witness`, `colour-witness` and
  `prompt-witness` compare the shell's own resident pages, not its file pages; see below).
- The sweep: `ae55dd6` (pelt#93: the prompt witness's `den`); `6695b69`, `c46a70e`, `b405e85`, `e1fcc03` (pelt#97:
  `printf/c_hex_float`, recorded from dash 0.5.13.4 with `bash --posix` agreeing; printf/8 pending, 532 of 548).
- `disown` in a script: `1258408`, `49e8720` (`jobs/disown_script`, from bash 5.3.20; dash has no `disown`).
- Evidence: `135d78e` bash 5.3.20's and dash 0.5.13.4's tables; `43f2f07` the den measurement's rig and rows.
- Docs: `5187c48` and `60c0a5f` the changelog; `4a6686e` README only (`disown`, the hangup, `kill`, the stopped
  jobs' end, 532 of 548; sessions unchanged at 593).
- Evidence kept in the tree: `notes/sh38/` (the three tables measured before the change, bash 5.3.20's and dash
  0.5.13.4's taken after it with the same rows, bash's raw probe logs, `den-cost.py` and its rows).

Rows, red then green (Linux, in the container):
- `tools/hangup-witness`: at trunk `b80d6570` 16 of 46 rows hold (`notes/sh38/pelt-b80d6570.table`); at `d5eb28b`,
  the tree of `2655b6c`, 46 of 46; at the head, in the gauntlet's `signal-witness-native` and `-release` steps.
- `tools/self-check`: `interactive_set = 23` and `interactive_set with QUIT ignored at start = 19` red at `5fc06ab`,
  green at `10e91da`.
- `tools/prompt-witness`'s `prompt-vcs-real-probe`: red on macOS in nightly runs 42066187159 and 42678757228 (the
  Python stand-in); green on Linux at `5fc06ab` with the sh one. A macOS green is the next nightly's to show.
- `printf/c_hex_float` is `PEND-fail` at trunk's pelt (`printf: %a: conversion not supported`), by design.
- The idle rows (`shadow-witness`, `colour-witness`, `prompt-witness`): the first gauntlet take at `a7f4fdb` (record
  sha256 `4a6b5f06…`) went red at `shadow-witness-native` (resident pages 3266 → 3154 over the 10 s) and
  `prompt-witness-release` (`Rss` 6004 → 5876 kB), and its resume at `shadow-witness-native` again (3031 → 3029). In
  each the shell made no context switch, no fault and no tick, its anonymous memory was unchanged, and the pages
  that went were file-backed (`RssFile` 5668 → 5220, 3012 → 2884, 4728 → 4720 kB): the host, with about 1 GB free
  and its page cache under reclaim, took them from an idle process. The rows now compare the anonymous resident
  pages with the activity counters (`d44406b`), as `loop-rss` and `shape-rss` measure kept memory since pelt#118;
  a shell that woke or kept memory still fails them. The take and its resume are kept beside the green one.

The gauntlet record at the head and the plant record are in the PR's body, taken after this note.

Also seen, not this lane's to change: bash 5.3.20's table taken a second time (another host, the same package)
differed from its first in two fields that race in bash itself (whether a stopped job also gets the exit path's
SIGTERM after the hangup's SIGCONT has woken it, and whether a foreground job also gets the kernel's SIGHUP as bash
dies); bash 5.2.21's two takes were identical, and that table, stable, is the one pelt is held to.

## Done-when

- [x] Item 1: bash's table measured black-box in containers and committed as the prediction before any change
  (bash 5.2.21 twice, and 5.3.20 after), with dash's and pelt's at trunk.
- [x] Item 2: pelt follows the table, red first, in its own suite with a pty harness (`tools/hangup-witness`, 46
  rows, inside `tools/signal-witness`); `disown` added as bash defines it (`-h`, `-a`, `-r`); `nohup` works.
- [x] Item 3: `kill %N` on a stopped job continues it after SIGTERM or SIGHUP (R-sh38-1).
- [x] Item 4: the PAX row, as a note for the pax lane (§2).
- [x] Item 5: the ten issues, each looked at against trunk, two changed red first, the rest said why (§3); the
  prompt's `den status` measured by repository size, R-sh38-8, the default unchanged (§4).
- [ ] Item 6 and the delivery: the gauntlet at the head, the plant red by name, the PR, the audit: in the PR.
- Issues to close by hand at the merge: pelt#93, pelt#83. Issues to file (not filed here): den, `den add .` of
  5,000 new files killed under a 6 GiB cap and one commit of 3,000 new files "not yet implemented"; pax, the
  controlling process's exit and an orphaned stopped group get no SIGHUP from PAX's kernel (§2).
- README read and refreshed (a README-only commit).

