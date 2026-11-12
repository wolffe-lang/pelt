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
  follows bash: on PAX, where a stopped process does not receive a pending TERM, `kill %1` otherwise does nothing
  until `fg`. Reversing it is one call in `bi_kill`.
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

The sweep's predictions are in §3, written before each issue's first change.
