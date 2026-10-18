# sh18 — job control (pelt on wolf 0.2.32: H3e)

Contract: `sprints/pelt/18-job-control/sh18-job-control.md` in the
planning repo (`0f647e5`). This file is the lane's record: §1 to §3 are
committed before the first change under `src/`, `tools/`, `tests/` or
`wolf-toolchain.toml`; the evidence index (§4) is filled in as the work
lands.

## 1. Forbidden

As the contract. No shell's source is read or searched for (dash, bash,
busybox, mksh, zsh or any other), nor a libc's or a kernel's (rulings
#42–#45). Behaviour comes from POSIX.1-2024 (XCU 2.11 "Job Control",
2.9.3.1, 2.12, the `jobs`, `fg`, `bg`, `kill`, `wait` and `set` pages,
XBD 3 "Job ID", XBD 11), the shells' manuals as documentation, wolf's
`spec/11-os.md` at `v0.2.32`, and black-box runs of the reference
binaries **only inside throwaway `--network none` containers**
(`notes/sh18-evidence/refrun.sh`, kasumi's `/usr` read-only: dash
0.5.13.4, bash 5.3.20 as `bash --posix`). s240's strace of dash
(wolf-lang `docs/s240/ev/linux/dash-im.trace`) is a recorded run, read
as such. Signals go only to process groups a test made (every probe
runs under `setsid -w` in the container; every session's shell leads
its own session on its own pty). A signal's meaning is named, never a
literal bit. The toolchain from the release archives by digest, each
read twice. No merge, no tag, no issue filed or closed, no package
installed, no other lane's CI run cancelled, nothing under `~/.claude`,
no attribution trailers. No build on nomad-1: kasumi under
`~/lanes/sh18/`, detached jobs by `setsid` with the pid recorded and
stopped by that pid only; scratch under `~/lanes/sh18/`, never `/tmp`.
Strict evidence (#571); process, signal and terminal tests also under
`taskset -c 0-3`; SigBlk/SigIgn read before any signal row is called
red. If the harness refuses an action, the lane stops and reports.

## 2. Inputs, verified (2026-10-18, before any change)

| input | contract says | measured | drift |
|---|---|---|---|
| pelt trunk | `c435b9a` | `origin/trunk` = `c435b9ae616b…` (sh17's notes); branch `sh18` cut from it; no open PR | none |
| wolf 0.2.32 | `v0.2.32` at `72de141f` | tag object `d21c4b28…` → `72de141f6246…`; release 416327027 read twice by the API; `wolf --version` line 1 `wolf 0.2.32 (wolfgang, pin 72de141)`, line 2 `paired with lupin 0.1.54 (reference interpreter), pin 294d626` | none |
| lupin 0.1.54 | `v0.1.54` at `0e536e8` | tag object `9c98d445…` → `0e536e8fb451…`; release 415937354 read twice; `lupin 0.1.54 (wolf-interp, reference interpreter at pin 294d626)` | none |
| the digests | by digest, read twice | API, twice (`notes/sh18-evidence/logs/digests.txt`): wolf linux x86-64 `4c37f9c5…`, aarch64 linux `af27d426…`, macOS `061ea7e5…`; lupin `175df238…`, `5fb15e31…`, `9cd14db7…`; the linux x86-64 pair downloaded twice on kasumi and hashed equal (`logs/fetch-kasumi.txt`) | none |
| the bundled std | wolf-std `d37c911` | the archive's `std/STD-REV` reads `d37c911f12206c4bf5c8d3281a649bf31da3beef` | none |
| issues | pelt#18 (P12), #28 | #18 open: `jobs` not found, case `jobsctl/c_jobs_script`; #28 open: `trap -x`, unreported write errors, the census coin | — |
| the spec | `[os.proc.poll]`, `[os.term]`, `[os.term.group]`, `[os.signal.send.group]`, the spawn's group | read at `v0.2.32` (`spec/11-os.md`): `os_wait_poll() -> (int, int) ! {io}` (0..255, `-N`, `256 + N`, `(-1, n)`); `os_spawn_job(exe, args, map, group, tty, defaults)`; `os_term_set_foreground`; `os_set_pgid` on the caller; `os_signal_send_group(pgid > 1, m)`; `os_signal_send_all` | — |
| rulings | #69, #79, #84 | #69 R1 B (pelt re-executes itself for a subshell; **not done yet**), R8 PAX job control is pax's; #79 the group sends, `os_set_pgid`, the lane order; #84 the poll, `256 + N`, the interruptible wait composed of listen + poll + `os_signal_wait` | — |
| px48's notes | what job control calls on Linux | pax `notes/px48-job-control.md`: `setpgid` in child and parent, `TIOCSPGRP`, `kill(-pgid)`, `wait4(-1, WNOHANG\|WSTOPPED)`, never `WCONTINUED` | — |
| the baseline | sh17's 950/0/44, 243/0/13 | trunk `c435b9a` on kasumi (`logs/base.status`, every gate 0): corpus **950/0/44** both tiers and both under `taskset -c 0-3`; sessions **243/0/13**; statements **487 of 545** | none |
| kasumi | `/home` ~30G | 36G free at the start | — |

### 2.1 What the references do (black-box, `notes/sh18-evidence/refs/`)

Probes: `probe/keys/*.keys` typed into `dash -i -m` and `bash --posix
-i -m` through `tools/lib_session.py`'s pty by `probe/jcprobe.py`, every
byte of both streams kept; `probe/scripts/*.sh` run as scripts under
`setsid -w`. Where POSIX speaks it decides; where it is silent dash
decides.

- **Job numbers** are the lowest free number (p02). **`jobs`** lists the
  most recently used first (p02, p14): `[n] M state`, the mark `+`
  (current), `-` (previous) or a blank, the state padded so the command
  starts in column 33 (one blank when the state is longer), the command
  last. `-l` puts each process's id before the state, one line per
  process of a pipeline, a ` |` after all but the last (p01, p15).
  `-p` the group leader's id, one line a job. A finished job is shown
  once and forgotten.
- **States** (p03, p04): `Running`, `Done`, `Done(N)`, `Stopped`
  (TSTP), `Stopped (signal)` (STOP), `Stopped (tty input)`, `Stopped
  (tty output)`, and a signal's text for an end by signal (`Terminated`,
  `Killed`, `Interrupt`, `Hangup`, …; glibc's C-locale words, `(core
  dumped)` after a core). A pipeline's state is its last process's
  (p20).
- **The command text** is rebuilt from the tree (p01, p19): words as
  written, but a quoted part in double quotes, `$x` as `${x}`, `$(…)`
  and backquotes as `$(...)`, redirections with their descriptor
  (`1>/dev/null`), here-documents as `<<...`, `{ … }` as its body,
  `( … )`, `a | b`, `a && b`, `!a`. With job control off a job has no
  text at all (s02, s10).
- **Notices** go to standard error before the next prompt, for every
  background job that ended or stopped since (p03, p17, p18); with
  `set -m` in a script too (s01, s03). A foreground job ended by a
  signal gets the signal's text alone (`Terminated`), `SIGINT` a
  newline, `SIGPIPE` nothing; a stopped one its job line (p04).
  **`set -b` makes no difference to dash** (p11): the notice still
  waits for the next prompt; bash writes it at once. POSIX says at
  once; that is what pelt does (2.11/11 stays a gap the harness cannot
  type).
- **A stopped foreground job's `$?`** is `128 + N` (148 for TSTP on
  linux, 147 STOP, 149 TTIN, 150 TTOU; p04).
- **`fg`** writes the command, gives the terminal and sends `SIGCONT`
  to the group even when the job runs (p21, s240's trace); **`bg`**
  writes `[n] command`, also for a running job, status 0 (p05);
  either with no job: `No current job`, 2; a job id no job has: 2
  (p21). Without job control both fail, 2 (s08).
- **`kill %job`** with job control sends to the job's group; `kill --
  -pgid` to a group; a group no process is in: `No such process`, 1
  (p13). `kill %1` (TERM) leaves a stopped job stopped (no `SIGCONT`);
  it ends when continued (p06).
- **`wait`** (p12, s04, s05): with no operand it does not wait for a
  stopped job (0); `wait %n` of a stopped job answers `128 + N` at once;
  a trapped signal cuts it short with `128 + N` and the action runs.
- **Ctrl-C** with job control reaches only the job; when the job dies
  of `SIGINT` the shell acts as if it had heard it: with no trap the
  command (a loop) is abandoned and `$?` is 130, with a trap the action
  runs and a loop goes on (p09). **Ctrl-Z** in a loop stops that one
  job and the loop goes on (p10).
- **`exit` with stopped jobs** writes `You have stopped jobs.` and does
  not exit, unless the command before it was an `exit` that warned
  (p07, p08; c_jc_ctrl_z).
- **Signals** (s01, s07): with `-m` dash ignores `TSTP` and `TTOU` (and
  `TTIN` when interactive, sh06's `c_jc_shell_ignores_tstp`); its
  children start with none ignored. A background job's standard input
  is not `/dev/null` with job control on (p17: `cat &` stops on tty
  input).
- **`$-`** carries `m` with job control on and `b` with `set -b` (p11).

## 3. Prediction (committed before the first change)

### 3.1 The pin (item 1)

`wolf-toolchain.toml` to wolf 0.2.32 / lupin 0.1.54 / std `d37c911` in a
commit of its own, nothing else changed. 0.2.31 and 0.2.32 move no
behaviour pelt reaches (its eleven plain shifts gave no new trap in
s237's census; s245's descriptor move only matters for a program started
with 0–2 closed). **Predicted at the bare pin: corpus 950/0/44, sessions
243/0/13, statements 487 of 545, on both tiers**, every gauntlet gate 0.
Falsified by any case that moves.

### 3.2 The design (items 2–5)

- **The shell's group and the terminal** (`sh.jobs`, new): job control
  (`set -m`, on by default when interactive) at start reads the
  terminal (`/dev/tty`, else descriptor 0 or 2), waits until its group
  is the foreground one (sending itself `BG_READ` while not), leads a
  group of its own (`os_set_pgid(0)`) and takes the terminal
  (`os_term_set_foreground`); at exit and before `exec` it gives both
  back. With it on, an interactive pelt ignores `SUSPEND`, `BG_READ`
  and `BG_WRITE` (a script with `set -m` `SUSPEND` and `BG_WRITE`, as
  dash), and every program it starts gets them back at the default
  (`os_spawn_job`'s `defaults`).
- **A job is a pipeline of programs**: each program of a top-level
  pipeline (or of `cmd &`) is started by `os_spawn_job` into one new
  group (the first leads, `group` 0; the rest join its id), the
  terminal handed to it for a foreground job, taken back when the job
  ends or stops. A stage pelt runs itself stays in the shell (no fork;
  ruling #69 R1 is not done), and inside a subshell pelt runs in-process
  there is no job control, as in dash's subshells.
- **The wait**: `CHILD` is listened for once job control or a waiting
  `wait` needs it; `os_wait_poll` until `(-1, n)`, every answer
  recorded in the job table, then `os_signal_wait` on `CHILD` (a
  foreground job) or `CHILD` and the trapped set (`wait`). A stop is
  `256 + N`; `$?` is `128 + N`. A foreground job ended by `SIGINT` is
  answered as an interrupt the shell heard (`signal.raise`). The fast
  path keeps its own blocking wait with job control off and hands a
  program to the ordinary path with it on.
- **The table**: slots numbered from 1 and reused lowest first, a
  most-recently-used order for `+` and `-`, per job its group, its
  command text (rebuilt from the tree as dash writes it; none with job
  control off), its state, whether its change was told; per process its
  handle, id and status. A finished job is forgotten once told.
- **The built-ins**: `jobs` (`-l`, `-p`, operands), `fg`, `bg`, job ids
  `%n`, `%+`, `%%`, `%`, `%-`, `%string`, `%?string`; notices before
  each prompt; `set -b` writes the notice at once while a line is edited
  (the editor's wait takes `CHILD` too); `kill %job`, `kill 0` and
  `kill -- -N` through `os_signal_send_group` (`-1` through
  `os_signal_send_all`); `wait` interruptible by a trapped signal;
  `exit` with stopped jobs warns once; `$-` shows `m` and `b`.

### 3.3 The numbers

| | bare pin | predicted at the head |
|---|---|---|
| corpus | 950/0/44 | **(955 + new)/0/39** both tiers and under `taskset`: `jobsctl/c_jobs_script`, `jobsctl/c_fg_bg_no_monitor`, `jobsctl/c_monitor_script_pgid`, `pending/wait_interrupted`, `option/c_long_names` leave pending; `signal/c_wait_interrupted_term` stays (its sender is `( … ) &`, a subshell pelt runs in-process: moved to the fork row) |
| sessions | 243/0/13 | **(254 + new)/0/2**: the eleven `c_jc_*` leave pending; `c_ignoreeof`, `c_mail` stay; about ten new `c_jc_*` cases (one or more per built-in: `jobs -l`/`-p` and job ids, `fg` of a pipeline, `bg` of a running job, `kill` of a group, `wait` of a stopped job, `exit` with stopped jobs, Ctrl-C in a loop, the states, the numbering) |
| statements | 487 of 545 | **at least 500 of 545**: 2.11/1–10 and /15, `sh/16`, `jobs/1–3`, `fg/1–2`, `bg/1`, 2.12/4, `kill/6`, `set/18`; 2.11/11 and /12 stay gaps |
| scripts | 76/3/1 | verdict for verdict as trunk |
| memory | flat | `loop-rss`, `shape-rss`, `session-rss` flat; a typed program under `-m` (the ordinary path) also flat |
| idle prompt | 0 context switches | 0 (with `-b` too: a wait on `CHILD` makes none) |
| lupin, checked | refuse | unchanged: lupin refuses at resolve, the checked machine `unsupported` |

### 3.4 What stays pending, predicted

A subshell, a compound command after `&`, and a pipeline stage pelt runs
itself are not processes (ruling #69 R1 open): `( … ) &` and `{ … } &`
are not background jobs (they run to their end first); a pipeline with
such a stage is not stopped as one job by Ctrl-Z; `signal/c_wait_interrupted_term`
and the existing fork rows stay pending. The terminal's settings are not
saved per job (2.11/12, as dash).

### 3.5 Plant

On a branch `sh18-plant` (never to merge), CI narrowed to the ubuntu
job and dispatched once: the head with the spawn's group turned off (every
job left in the shell's group) and the stop read as an end. Predicted
red: the job-control sessions on both tiers (the plant's sessions
step), and `jobsctl/c_monitor_script_pgid` in the corpus; nothing else.

### 3.6 A static pelt for PAX

`pax/tools/mkpelt` at pax trunk inside Ubuntu 24.04 on kasumi with
`ld.lld`, as sh17; its sha256 in the report; the new system calls
(`setpgid`, `TIOCSPGRP`/`TIOCGPGRP`, `kill` to a group, `wait4` with
`WUNTRACED`) listed from `strace` for px48's successor.
