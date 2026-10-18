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

### 3.7 The result against the prediction

Measured on kasumi (linux x86-64, CachyOS, 16 cpus) by
`notes/sh18-evidence/gauntlet.sh` (every gate's exit status in
`logs/<tag>.status`): **trunk** `c435b9a` (`base`), the **bare pin**
`ab97fce` (`pin`), the **head** `2676879` (`head4`); and in CI (linux
x86-64, macOS arm64, linux aarch64).

| prediction | predicted | measured | held? |
|---|---|---|---|
| the bare pin | 950/0/44, 243/0/13, 487 of 545, every gate 0 | **950/0/44** both tiers and both under `taskset -c 0-3`; **243/0/13**; **487 of 545**; all 37 gates 0 (`logs/pin.status`) | held |
| corpus | (955 + new)/0/39; `c_wait_interrupted_term` stays | **956/0/38** both tiers, kasumi and CI linux and macOS (`ci/head-39162544747.txt`): the five predicted leave pending, and `signal/c_wait_interrupted_term` too | held but for that case: its `( sleep 1; kill -TERM $$ ) &` runs in-process to its end before `wait`, so the TERM is pending when `wait` looks and the answer is dash's, by another order (`tests/diff/PENDING.md`) |
| sessions | (254 + new)/0/2 | **264/0/3** both tiers, kasumi and CI: the eleven leave pending, ten new cases pass, one new case is pending (`c_jc_mixed_pipeline`, on fork) | held, with one more pending than predicted (below) |
| statements | at least 500 of 545 | **505 of 547** (92.3%; two new statements, `kill/7` and `2.11/18`, and three kind X); 2.11/11 and /12 stay gaps; 2.11/18 pending on fork | held |
| scripts | verdict for verdict as trunk | §3.8 | |
| memory | `loop-rss`, `shape-rss` flat; a typed program under `-m` flat | flat, both tiers, kasumi and CI: two new rows, a typed program (`env true`) and a typed pipeline of programs, each a job under `-m`: 140 and 192 B a turn native, 140 and 180 release, at 10,000 → 20,000 lines, inside the 2,000 KB bound (`logs/head4-shape-*.log`; the bare pin's own build gives 157 and 188 at 3,000 → 6,000) | held, after two fixes (not predicted, below) |
| idle prompt | 0 context switches | `edit-witness` 11 of 11 both tiers, kasumi and CI (its idle row: no context switch at an idle prompt with job control on) | held |
| lupin, checked | refuse | lupin 0.1.54 refuses at resolve naming `os_signal_default` (as at sh17); **the checked machine now runs pelt** to its end: `conform-run --checked` answers `exit(0)` with the native build's bytes for `sleep 0.1 & jobs; wait` (`logs/machines.txt`; s237's home-module methods at 0.2.31) | **not held** for the checked machine |
| plant | the job-control sessions red, `c_monitor_script_pgid` red, nothing else | CI **39160267977** on `sh18-plant` (`fa0972b`, ubuntu only, dispatched): corpus **955/1/38 on both tiers, only `jobsctl/c_monitor_script_pgid`** (`ci/plant-39160267977.txt`); the session steps do not run after a red corpus in CI; on kasumi the plant's binary fails **20 of the 25 job-control sessions and nothing else** (245/20/2, `logs/plant-sessions-native.log`): the five that pass ask for nothing a group or a stop decides (Ctrl-C reaches the job either way, the shell leads its group at start, ignores TSTP, takes the terminal back) | held |
| static pelt for PAX | ET_EXEC, no PT_INTERP | `76f3fc40…`, 15,198,832 bytes (§3.9) | held |

**Not predicted.**

- **dash ignores `TSTP` and `TTOU`, not `TTIN`**, interactive or not
  (`SigIgn` `0x284004` in every recording with `-m`, `0x280000` in s01);
  §2.1's "and `TTIN` when interactive" was wrong. pelt does the same
  (`e33efa6`).
- **The pipeline's last stage cost the fast path.** Starting the last
  stage "not waited for" sent a built-in there down the ordinary path,
  and a typed `true | true` kept 689 B a turn (CI 39157249383 red on
  `shape-rss` on linux and macOS). The last stage now keeps the fast
  path (`jc_last`), and a program there, or a foreground program, is
  started into its job from the fast path too (`6a46150`): a typed
  program would otherwise have kept 813 B a turn.
- **The notice raced the host.** On macOS a job `kill` ends is gone
  before the next prompt's look, on linux not yet, so a notice landed a
  step early (CI 39157808792, `ci/pr-39157808792-macos.txt`; the bytes
  in `ci/macdiag-39160238181.txt`). The look taken as a line is read is
  now written into the table only after the line has run (`04f1fc3`):
  `exit` still reads the table as dash does, and the notice comes at
  the same step on both hosts (`ci/macdiag-39160994608.txt`).
- **macOS ends a stopped process on `SIGTERM`**; linux keeps it stopped
  until it is continued (dash on linux sends no `SIGCONT`, p06): the
  host's rule, so `c_jc_stopped_term` was dropped (`71fa22c`).
- **BSD `cat` and `head` end with EINTR when continued** on macOS
  (`cat: stdin: Interrupted system call`, `ci/macdiag-39160994608.txt`),
  where a shell's `read` goes on: `c_jc_fg` (sh06's) continues
  `sh -c 'read x && echo "$x"'` now, and BSD `wc -l` pads its count, so
  two cases cut the blanks (`d726186`, `6d04483`).
- **A pipeline with a stage pelt runs itself could not be stopped**:
  Ctrl-Z stopped its programs and the shell, running the other stage,
  waited on their pipe for ever (`probe/keys/p27`). Such a pipeline is
  now no job: its programs keep `SUSPEND` ignored and Ctrl-Z does
  nothing (`9b06c8e`); dash stops the whole pipeline
  (`c_jc_mixed_pipeline`, pending on fork).
- **dash's own `kill %1` fails without job control** (`kill: No such
  process`, s12 row A): `kill/c_job_id`'s stderr was that failure, so the
  case now hides it (`9da57c7`); pelt signals the job (XCU `kill`).
- **`jobs -l | sed` padding is host-bound**: the pid's width moves the
  column; `c_jc_jobs_l_pipeline` squeezes blanks.

### 3.8 The script census

`tools/script-census` with the bare pin's static build (`sc/pelt-pin`)
and the head's (`sc/pelt-head4`), each unaided and aided, the images
built afresh (`--build`) and every script run with the network off
(`notes/sh18-evidence/scripts/`): **76 same, 3 differ, 1 unstable of 80 in three of
the four passes, and 75/4/1 in the bare pin's aided pass**: the three
that differ are trunk's (xzgrep, zgrep, zdiff: a process per pipeline
stage), pfetch is the known unstable one, and the fourth in the pin's
aided pass is `configure-sed`, the timing coin pelt#28 names (a
filesystem timestamp-resolution check), same at the head. Unaided, the
`id` and `verdict` columns of pin and head are identical (`diff` empty);
aided they part on `configure-sed` alone. Held, the coin aside. The
binaries: `sc-*.bin` (pin `a3a1451f…`, head `30e6fec7…`).

### 3.9 A static pelt for PAX, and what it asks of a kernel

pax `b274030`'s `tools/mkpelt` in a throwaway Ubuntu 24.04 container on
kasumi with clang 18.1.3, **lld 18.1.3 (`ld.lld` on `PATH`)**, gcc 13.3
and glibc 2.39 (`mkpelt-job.sh`, `mkpelt-run.sh`), at pelt
`26768793a3e7115782facd1ceb2e18368481e82a`: **sha256
`76f3fc40702af01b6381d01a7f81de2ebe701787ee29ef61484dc7ad1ec29849`,
15,198,832 bytes**, ET_EXEC, no PT_INTERP, hashed twice
(`logs/mkpelt-head.log`); `-c 'sleep 0.1 & jobs; wait; set -m; sleep
0.1 & jobs; wait'` answers as on the dynamic build. The same container
built trunk `c435b9a` to **`07bb5156…`, the digest sh17 measured and
px49 pinned** (`logs/mkpelt-trunk.log`), so the method is PAX's.

**The system calls** (`tools/syscall-census` over the corpus and the
sessions, the bare pin's static build against the head's;
`sysc/pin/census.txt`, `sysc/head/census.txt`): **48 distinct calls at the bare pin, 50 at the
head: the two new are `setpgid` (162 calls: the shell's own group at
start and every job's group, in the child and the parent) and `getpgrp`
(136: `os_pgid`).** The rest of job control rides calls pelt already
made, counted by name only (the census keeps no arguments): `ioctl`
(13,859 → 15,562; job control asks and sets the terminal's foreground
group, `[os.term]`), `kill` (146 → 168; a group is `-pgid`,
`[os.signal.send.group]`), `wait4` (1,416 → 1,755; `os_wait_poll` is
`WNOHANG | WUNTRACED` per live child, `[os.proc.poll]`), `tgkill` (1 → 7,
`signal.raise`). Each of these is what px48 gave PAX (groups and sessions,
`TIOCSPGRP`, `kill(-pgid)`, stops reported by `wait4`), so PAX's next pin
needs no kernel call it lacks; PAX's own job-control sessions are
px48's. Under strace the timing-sensitive cases part as at sh17
(reported, not judged: `logs/sysc-*.log`).

## 4. Evidence index

- **The prediction:** `ccb83c5`, before the pin (`ab97fce`) and the
  first change under `src/` (`03c8b00`).
- **The references:** `notes/sh18-evidence/refrun.sh` (the container),
  `probe/jcprobe.py`, `probe/run.sh`, `probe/keys/p01`–`p27`,
  `probe/scripts/s01`–`s12`; the answers of dash and bash in `refs/`.
- **The cases:** recorded by `tools/session-record` (and
  `tools/oracle-record` for `kill/c_job_id`) through `refrun.sh` (dash
  0.5.13.4, bash 5.3.20).
- **The gauntlets:** `gauntlet.sh`; `logs/base.status` (trunk
  `c435b9a`), `logs/pin.status` (`ab97fce`), `logs/head4.status`
  (`2676879`), every step's log beside them; all gates 0 in all three.
- **Seen red:** the bare pin's binary on the head's 25 job-control
  sessions: 20 fail (`logs/red-sessions-pin.log`; the five that pass are
  the ones that passed at trunk too); the plant in CI, run **39160267977** on `sh18-plant`
  (`fa0972b`; `ci/plant-39160267977.txt`) and its sessions on kasumi
  (`logs/plant-sessions-native.log`, `logs/plant-diff-native.log`);
  reds CI found and fixed: **39157249383** (`shape-rss`, the last
  stage), **39157808792** (macOS: the notice race, BSD `cat`, BSD `wc`;
  `ci/pr-39157808792-macos.txt`); the bytes from macOS runs
  **39160238181** and **39160994608** on `sh18-macdiag` (diagnostic
  only, `ci/macdiag-*.txt`).
- **CI green:** run **39162544747** at `2676879` (`ci/head-39162544747.txt`:
  corpus 956/0/38 and sessions 264/0/3 on both tiers of linux and
  macOS, every witness green, aarch64's refusals asserted), and the run
  at the PR's head (the PR body).
- **The machines:** `logs/machines.txt`. **Memory:** `logs/head4-shape-*.log`,
  `logs/head4-loop-*.log`. **PAX:** `logs/mkpelt-head.log`,
  `logs/mkpelt-trunk.log`. **System calls:** `sysc/`.

## 5. Done-when

- Branch `sh18`, PR #32 open and unmerged, CI green at the head;
  `wolf/tools/lane-audit.sh pelt sh18 32` run from the org directory,
  its exit status read directly.
- pelt#18 (P12, `jobs` in a script) is **close-ready**: `jobsctl/c_jobs_script`
  passes on both tiers and hosts. pelt#28 is not touched. None filed or
  closed by the lane.

## 6. What pelt does, item by item

| item | pelt now | reference |
|---|---|---|
| 1 the pin | wolf 0.2.32 / lupin 0.1.54 / wolf-std `d37c911`, its own commit; nothing moved at the bare pin | — |
| 2 groups and the terminal | with `set -m` (on when interactive, `+m` off, also in a script): at start the shell waits for the foreground (sending itself `BG_READ` while it is not), leads its own group (`os_set_pgid(0)`) and takes the terminal (`/dev/tty`, else 2 or 0); each program of a top-level pipeline, or of `cmd &`, is started by `os_spawn_job` into one new group, the first leading; a foreground job is handed the terminal and the shell takes it back (`os_term_set_foreground`) when it ends or stops; at exit and before `exec` the shell gives back the terminal and the group it was started in; `TSTP` and `TTOU` ignored for the shell, back at the default in its children | XCU 2.11; dash (`SigIgn`, s240's strace) |
| 3 the wait and stops | `CHILD` listened for; `os_wait_poll` until `(-1, n)`, then `os_signal_wait` on `CHILD` (a foreground job) or `CHILD` and the trapped set (`wait`); a stop is `256 + N`, `$?` `128 + N`; a stopped foreground job becomes the current job and is told at once; a job ended by `SIGINT` is answered as an interrupt the shell heard (a loop abandoned, or the trap run) | XCU 2.11, `wait`; dash p09, p12 |
| 4 the built-ins | `jobs` (`-l` one line a process with its id, `-p` the group leaders; operands), `fg`, `bg` (also of a running job), `%n`, `%+`, `%%`, `%`, `%-`, `%string`, `%?string` (the first process's text, as dash); a job's number the lowest free; `+`/`-` by most recent use; notices before the prompt, most recent first, an ended job forgotten once told; `set -b` writes the notice at once while a line is edited and edits the line again; `exit` with stopped jobs warns once; `$-` has `m` and `b`; with job control off a job has no text, `wait` with no operand forgets the ended ones, `fg`/`bg` fail 2 | XCU `jobs`, `fg`, `bg`, `set`; dash p01–p23, s02, s08, s10; POSIX for `-b` (dash waits for the prompt, bash does not) |
| | the job text rebuilt from the tree as dash writes it: quoted parts in double quotes, `${x}`, `$(...)`, `N>file`, `<<...`, `!cmd`, `else if … fi; fi` | dash p19; pelt keeps `5<&-` and every `case` pattern where dash writes `5<&/` and the first |
| | the states' words are glibc's C-locale texts on every host (`Terminated`, `Stopped (tty input)`, `Done(3)` …) | dash on linux; macOS's `strsignal` would say `Terminated: 15` |
| 5 `kill`'s groups | `kill %job` to the job's group (`os_signal_send_group`), or to each process with job control off; `kill 0` the shell's group, `kill -- -N` group N, `kill -1` every process (`os_signal_send_all`); a group no process is in: no such process, 1 | XCU `kill`; dash p13 |
| 6 sessions, census | 22 job-control sessions pass (11 from sh06, 10 new), one pending on fork; the corpus's six; 505 of 547 statements | — |

## 7. Wolf findings

- **The checked machine runs pelt** at 0.2.32 (`conform-run --checked`
  answers `exit(0)`, the native build's bytes for a job script;
  `logs/machines.txt`), where it was `unsupported` at 0.2.30 (sh17): s237's
  home-module methods. Not a defect; the census of what it answers is a
  later lane's.
- Nothing refused, no new issue against wolf-lang. `os_pid()` is
  infallible (a stray `else` is E0608, as it should be).

## 8. Pending, not verified, named out

- **Pending on ruling #69 R1 (a subshell is still in-process):**
  2.11/18, a pipeline with a stage pelt runs itself stopped as one job
  (`c_jc_mixed_pipeline`): pelt makes such a pipeline no job, so Ctrl-Z
  stops nothing there rather than hang; `( … ) &` and `{ …; } &` are not
  background jobs (they run to their end first, then count as a finished
  job); a subshell's commands and a command substitution's run without
  job control, as dash's subshells do, but in the shell's process; the
  existing fork rows (`tests/diff/PENDING.md`).
- **Gaps the harness cannot type:** 2.11/11 (`set -b`'s notice between
  two keys: pelt writes it at once, `probe/keys/p24`, `p25`; dash does
  not); 2.11/12 (the terminal's settings saved per job: pelt does not, as
  dash does not).
- **Recorded differences:** `$(jobs -p)` at an interactive dash prompt
  is empty, pelt's lists the leaders; dash numbers a foreground job when
  it starts and pelt when it stops (a background job ending in between
  changes which number it gets); `kill %1` without job control signals
  the job where dash's own fails; `case` texts keep every pattern.
- **Not verified:** macOS by CI only (no build on nomad-1); linux
  aarch64 still builds no tier at 0.2.32 (asserted in CI); a shell
  started in a background group (the `BG_READ` loop at start) is not
  driven by any session (every session's shell leads its own session);
  the move out of a parent's group and back was run once, by hand, not
  in CI (`probe/keys/p28`, `logs/p28-child-shell.txt`: under `sh -c`
  pelt leads a group of its own and holds the terminal, and after
  `exit` the terminal is the parent's group again); `kill -1` is not run
  anywhere (it would reach every process the user may signal).
- **Disclosed:** one scratch file on nomad-1 went to `/tmp` (the
  regenerated census table, written and removed in one command); every
  other scratch file is under `~/lanes/sh18/`. Four of my own
  superseded CI runs were cancelled (39160365802, 39160979591,
  39161398985, 39161578832); no other lane's. Two diagnostic and
  plant branches are on origin, never to merge: `sh18-plant`,
  `sh18-macdiag`.
- **Found, not job control's:** `cmd & wait` in a loop keeps about
  1.7 KB a turn at the bare pin and at the head (a `shape-rss` row
  measured on kasumi, 1,809 B a turn at the pin, and left out; an issue
  to file).
