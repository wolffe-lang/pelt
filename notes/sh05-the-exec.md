# sh05 — the exec (pelt at wolf 0.2.27)

Contract: `sprints/pelt/05-the-exec/sh05-the-exec.md` in the planning
repo. This file is the lane's record: §2 is written first, §3 is
committed before either 0.2.27 archive is unpacked, and the evidence
index (§4) is filled in as the work lands.

## 1. Forbidden, absolutely

As the contract's §1: no `rm` outside `~/lanes/sh05/` and this lane's
own clones, on any host; no `git add -A`; nothing under `~/.claude`; no
merge to trunk, no tag; no `2>/dev/null` on a checkout; no attribution
trailers; the toolchain from the release archives by digest; no "seen
red" without a run id, sha, path or digest; strict evidence (#571), and
`wolf build` exit 2 read as a compile error; detached kasumi jobs by
recorded pid, never by process group; no build on nomad-1; no package
installs; at most two CI runs at once. **No shell's source is read**
(rulings #42–#45): POSIX.1-2024 XCU, the man pages, and black-box runs
of `dash`. Scratch lives under `~/lanes/sh05/` (`TMPDIR` points there
for every tool run), never in `/tmp`.

## 2. Inputs, verified (2026-10-11, re-derived from origin)

| input | contract says | measured | drift |
|---|---|---|---|
| wolf 0.2.27 | wolf-lang `0ddda6b7`; linux x86-64 `5e17eebe…`, linux aarch64 `c475e5dc…`, macOS arm64 `ea461a76…`, windows `ac784416…` | tag `v0.2.27` (annotated `d5f9597a…`) → commit `0ddda6b7ab9f899aeeea13a66b3427f8422b8a0f`; release 409367590, published 2026-10-11T04:12:05Z, not a draft; the API's asset digests: x86-64 linux `5e17eebed7ffbb3e…`, aarch64 linux `c475e5dc0a3748d1…`, aarch64 darwin `ea461a7668d98604…`, windows `ac78441650a6375c…` | none |
| lupin 0.1.50 | wolf-interp `32b970d`; x86-64 `e2867a35…`, aarch64 `a0c0c707…`, macOS `2cbd192d…`, windows zip `420e02c0…`, `lupin.exe` `b37b13bf…` | tag `v0.1.50` (annotated `b30a6d16…`) → commit `32b970da7f3a50e0b82825985a39b52b74da59dc`; release 409303515, published 2026-10-11T00:53:58Z; x86-64 linux `e2867a3515d4691f…`, aarch64 linux `a0c0c7071f0a2779…`, aarch64 darwin `2cbd192d2f4fa8b9…`, windows zip `420e02c00aa580c6…`, `lupin.exe` `b37b13bf6555c1be…` | none |
| "Read this before you bump" | the archive carries `std/` (wolf-std `87ba162`); 17 prelude names; pax and muzzle need `ffi` | read in the release notes of 409367590. **`tools/fetch-toolchain` is the layout the note warns about**: it copies the whole wolf archive into `.wolf-bin/` and then unpacks its own std pin with `tar -x` over it, so at 0.2.27 a `.wolf-bin/std` would be the archive's tree with the pin's files laid over. A grep of pelt `3e7516c` for a declaration of any of the seventeen names finds none. pelt has no `wolf.pkg` and declares no C | the fetch must change (§3.1) |
| Known issues #660, #665 | two soundness holes shared with 0.2.26; check the tree for both shapes | both OPEN. #660 needs a call under `in r { … }` handing a `mut` outer value and a string built in the enclosing region block; #665 needs a callee sending its argument on a channel. pelt `3e7516c` has **no `in r { }` block and no channel, `spawn` or `scope`** (grep of `src/`: the only region forms are `copy region` ×5 and one `region scratch`), so neither shape is in the tree | none |
| the bundled std | wolf-std `87ba162`, one red row (`x/json/dom_typed_reads`) | wolf-std trunk is `87ba16208da8ea642dd463fa89ff3a1ec80ceba1` today; pelt pins `2f389a7` and reaches only `std.map` (`Map.keys`, `Map.has`); it reads no json | pelt's std pin moves to the bundled commit (§3.1) |
| pelt trunk | `3e7516c` (sh03); 0.2.26 / 0.1.49; corpus 350/0/4, sessions 71/0/2; a CI memory gate | origin/trunk `3e7516c9f47e2ac01ed3650db0100d060aee4bc0`; push run 37984780360 green. sh03's own record says the corpus was `349 0 4` at `b3d7204` and gained one case after; the count is re-taken at the pin (§4) | to be measured |
| the four corpus skips | by name, and what each waits on | `pending/signal_status` (the signal's number: `os_wait` answers `signal` with none), `pending/unset_env` (no environment removal), `pending/pid` (`$$` on macOS: no getpid, wolf-lang#141, OPEN), `tilde/user` (no user database) | none |
| the two session skips | by name | `ctrl_c_prompt`, `ctrl_c_child` (no `SIGINT` meaning, wolf-lang#622, now CLOSED) | none |
| ruling #62 (s225) | `env_unset`; `os_exec(argv, env, fd map)` | `spec/11-os.md` at the tag, `[os.host.sigs]`: `env_unset(str) -> () ! {invalid}` and **`os_exec(str, List[str], List[str], List[int]) -> () ! {denied, invalid, io, not_found, unsupported}`** — four arguments, the program named apart from its argv (`exe`, then argv with argv[0], env, map) | the contract's three-argument shorthand omits `exe` |
| s219 (wolf-lang#622, PR #636) | signals, terminal control, process jobs | the same table: `os_signal_listen/ignore/default/poll/wait/raise` over nine MEANINGS (`RELOAD`=HUP 1, `TERMINATE`=TERM 2, `QUIT` 4, `UPGRADE`=USR2 8, `INTERRUPT`=INT 16, `SUSPEND`=TSTP 32, `BG_READ` 64, `BG_WRITE` 128, `CHILD` 256); `os_spawn_job`; `os_proc_pid(h)`; `os_wait_status(h)` (the code, or `-N`); `os_pgid`; `os_term_*`. Native and release serve all of it on linux and macOS. **What it does not reach** (`[os.term.note]`, read before the first change): no meaning for any other signal (USR1, ALRM, PIPE, ABRT, CONT, …); no non-blocking or interruptible child wait; no stop reporting, no `SIGCONT`, no signal to a group; no query of a disposition; still no getpid and no signal to an arbitrary pid | shapes §3.4 |
| the oracle | dash on kasumi | `dash 0.5.13.4-1.1`, `bash 5.3.20-2`, `strace 7.2-1` (`pacman -Q`); `tests/diff/ORACLE` names the first two | none |
| PAX | runs pelt as pid 1 | `pax/tools/mkpelt` at pax `638ecaa`: pelt's release tier linked through a `cc` that adds `-static`, with the wolf archive and the std commit **read from pelt's `wolf-toolchain.toml`** (`[wolf]` version, digest, version_line; `[std]` repo, rev) | the `[std]` section must stay, with a full commit |

## 3. Prediction (committed before either 0.2.27 archive is unpacked)

### 3.1 The pin alone (0.2.26 / 0.1.49 → 0.2.27 / 0.1.50), trunk's code

- `tools/fetch-toolchain` accepts the six archives at §2's digests. It
  removes `.wolf-bin/std` after the archives are copied and before the
  pinned std is unpacked, so the tree is one commit's; the std pin
  moves `2f389a7` → `87ba16208da8ea642dd463fa89ff3a1ec80ceba1`, the
  commit the archive bundles (`std/STD-REV` in the archive names the
  same commit: checked after unpacking, reported if not).
- `wolf fmt --check` clean; both tiers build under `--deny-warnings`
  (no W0304: none of the seventeen names is declared; no new E1010:
  s227's census had pelt byte-identical); `wolf test` passes.
- **No verdict moves at the pin alone**: the corpus and the sessions
  answer exactly as on trunk on both tiers (the same four PEND and two
  PEND rows; `pending/pid` PEND-ok on linux only), `glob-rss` and
  `loop-rss` ok; linux aarch64 still refuses both tiers by name (#614
  OPEN), so that job stays green unchanged.
- **Every binary moves**, because `libwolf_rt.a` is linked into each and
  changed (s222's root arena, s225's exec module, s219's signal and
  terminal modules, s224's json kernel). Stripped size (`strip`ped
  release, linux x86-64) moves by **less than 5%** either way.
- **RSS**: `tools/loop-rss` (10,000 and 20,000 turns) stays green; the
  20,000-turn peak, sh03's 3,352 KB release and 3,864 KB native, moves
  by **less than 25%** (s222 changed how the root arena takes memory
  from the host: bump windows over a chunk list, so the floor may move
  by a chunk; the slope may not). Falsified by a peak above 4,800 KB
  release, or by growth over 10,000 more turns above sh03's bound
  (100 B a turn + 1 MiB).

### 3.2 `exec cmd args`

- At the top level of the shell (not inside `( )`, `$( )`, a pipeline
  stage or `&`, which pelt runs in-process with no fork) `exec cmd`
  calls `os_exec` and **the pid does not change**: a new tool,
  `tools/exec-pid`, starts `pelt -c 'exec sleep N'`, and the process
  with pelt's pid becomes `sleep` (read with `ps`), on both tiers, on
  linux and macOS. Assignments before `exec` are made first and reach
  the new program's environment; redirections are applied first and
  the new program has them, an `exec 3>f` made earlier included;
  standard output is flushed; the `EXIT` trap does not run.
- When it cannot: **127** when the command is not found and **126**
  when it is found and cannot be run (a directory, a file with no
  execute bit), pelt's own message on standard error, and the shell
  ends there, interactive or not (dash, black-box: `exec /nonexistent`
  in `dash -i` ends it with 127). A file the kernel refuses for want
  of `#!` (`ENOEXEC`) is run by pelt itself, as XCU 2.9.1.4 says.
- Inside an in-process subshell `exec cmd` stays what sh03 made it: the
  program is spawned, waited for, and the subshell ends with its
  status. The pid there is a child's, not the shell's: named, not
  hidden (no fork).
- `exec` with only redirections: unchanged, no case moves.
- Corpus: `builtin/exec` stays green; new cases (assignment reaches the
  program, redirection applied first, 127, 126, descriptor 3 inherited,
  no `EXIT` trap, `ENOEXEC`, exec in a subshell and in a substitution)
  all pass on both tiers. One new session case (`exec` typed at the
  prompt) passes.

### 3.3 `unset` and the environment

- **`pending/unset_env` leaves PENDING and passes** on both tiers.
- A child's environment is exactly the exported variables that have a
  value: before every spawn pelt removes (`env_unset`) each name in the
  process environment that is not one of them, and `os_exec` is handed
  the list itself. So `unset VAR`, a variable never exported, a
  temporary `A=1 cmd` after `cmd`, a name that is not a shell name
  (dash drops `a.b=1`), and `unset PATH HOME LC_ALL PWD` (an empty
  environment: `/usr/bin/env` prints nothing) all match dash. New
  cases for each pass on both tiers.
- Named limit, unchanged: the process environment is one per process,
  so a child started by `&` and a later `unset` do not race, but
  nothing here isolates a subshell's environment beyond what the
  reconciliation before each spawn gives (it gives all of it: a
  subshell's `unset` is undone with its variables).

### 3.4 Signals

**Rows that move, by name:**

- `pending/signal_status` **leaves PENDING and passes** (143, and a
  line on standard error) on both tiers: `os_wait_status` answers `-15`.
  pelt writes its own words for a child a signal ended (not for
  `SIGINT` or `SIGPIPE`, where dash writes nothing).
- `ctrl_c_prompt` and `ctrl_c_child` **leave PENDING and pass** on both
  tiers on linux and macOS: an interactive pelt listens for `INTERRUPT`
  (so it survives and its children, which start with the default, do
  not), polls after the line is read and after the child is reaped,
  and answers 130 for the child.
- `pending/pid` **stays pending** (PEND-ok on linux, PEND-fail on
  macOS): 0.2.27 has no getpid (#141 OPEN). `tilde/user` stays pending.
- So the corpus goes from trunk's count to **(trunk's pass + 2)/0/2**
  before any new case, and the sessions to **(trunk's pass + 2)/0/0**.

**`trap`** (new cases, each recorded from dash; signals sent with
`/bin/sh -c 'kill -S $PPID'`, since `$$` is pending on macOS):

- `trap 'action' S` for HUP, INT, QUIT, TERM and USR2 **runs the
  action** after the foreground command ends, with `$?` kept across it;
  `trap '' S` ignores, and the ignore is inherited by a child; `trap -
  S` and `trap N` put the default back (the shell dies by the signal:
  status 128+N to its parent); a caught signal is the default in a
  child; an `exit` in an action ends the shell and runs the `EXIT`
  trap; a death by signal does not run it.
- `$!` **becomes a process id** (`os_proc_pid`), so `kill $!` reaches
  the job and `wait $!` still answers its status; a list pelt runs
  itself (no fork) has no process and gets a number no process can
  have. A background child starts with `SIGINT` and `SIGQUIT` ignored,
  as dash's does (`/proc/$!/status`, black-box).
- **Gaps predicted, each to be filed with a witness and a pending
  case:** (a) a condition with no meaning (`USR1`, `ALRM`, `PIPE`, …)
  is recorded and printed by `trap` but never caught or ignored: the
  shell dies where dash runs the action; (b) `wait` is not interrupted
  by a trapped signal (dash: the action runs and `wait` answers 128+N
  at once; pelt: after the job ends), because no child wait is
  non-blocking or interruptible; (c) a signal ignored when a
  non-interactive shell starts cannot be told apart from the default
  (no disposition query), so `trap` does not refuse it as XCU `trap`
  says.

**No job control in this lane** (`fg`, `bg`, `jobs`, Ctrl-Z). No corpus
or session row waits on it (`tests/session/PENDING.md` lists it under
"gaps with no session case"), and the surface is not whole:
`[os.term.note]` leaves stop reporting, `SIGCONT` and a signal to a
group to "the next job-control lane". The sessions are recorded from
`dash -i +m`, job control off.

### 3.5 Counts, memory and syscalls at the head

- Corpus: every non-pending case passes on both tiers; pending is
  `pending/pid`, `tilde/user` and the gap cases of §3.4 (at most
  three). Sessions: 0 pending.
- `loop-rss` green on both tiers, both hosts, with the same bound: the
  loop sets no trap, so no poll is made in it; the reconciliation runs
  only before a spawn.
- A loop of 2,000 spawns (`/usr/bin/true`) is at most **15% slower**
  than at the pin with trunk's code (one `env_vars()` per spawn).
- The static release build, straced over the corpus, asks for these
  syscalls trunk's build at 0.2.26 does not: **`execve` from the shell
  process itself** (no `fork`/`clone` before it), **`rt_sigaction`**
  for the trapped and ignored signals (and its `rt_sigreturn`),
  **`rt_sigprocmask`** around them, the self-pipe's **`pipe2`** and a
  second **thread** (`clone3` or `clone` with `CLONE_THREAD`, plus
  `futex`) from the first listen, and **`wait4`/`waitid`** unchanged.
  **Not** `tcsetpgrp`/`ioctl(TIOCSPGRP)`, `setpgid` or `tcsetattr`: no
  job control and no line editing here.

## 4. Evidence index

Every log named here is in `notes/sh05-evidence/` (kasumi, linux x86-64
7.2.8, 16 cpus; every job started with SigBlk 0 and SigIgn 0, printed at
the top of its log, except the baseline's, which says SigIgn 7 and
runs no signal case that passes). Digests are sha256, first 16 hex.

**Archive digests.** §2's table, from the release API; all six archives
this repo pins re-hashed after download on kasumi and equal to
`wolf-toolchain.toml` (`5e17eebe…`, `c475e5dc…`, `ea461a76…` for wolf;
`e2867a35…`, `a0c0c707…`, `2cbd192d…` for lupin). The archive's
`std/STD-REV` is `87ba16208da8ea642dd463fa89ff3a1ec80ceba1`, the std
pin.

**The prediction commit:** `d7c4a72`, before `baaa022` (the fetch) and
`9312eae` (the pin), the first commits that unpack an archive.

**The move table** (`base-3e7516c.log` `c648190f…`, `pin-alone-9312eae.log`
`d22e59ec…`, `head-8aecb7c.log` `20d91072…`):

| | trunk `3e7516c` at 0.2.26 | trunk's code at 0.2.27 (`9312eae`) | head `8aecb7c` |
|---|---|---|---|
| corpus, both tiers (pass/fail/pending, PEND-ok) | 350/0/4 (1) | 350/0/4 (1) | **443/0/7 (2)** |
| sessions, both tiers | 71/0/2 (0) | 71/0/2 (0) | **85/0/0** |
| stripped size, native | 1,467,856 | 1,475,648 (+0.5%) | 1,709,576 (+16.5%) |
| stripped size, release | 723,000 | 733,792 (+1.5%) | 846,400 (+17.1%) |
| static release (`cc -static`, glibc) | 12,784,624 | 13,480,456 | 13,762,928 |
| loop, 20,000 turns, release, median of 3 (KB) | 3,276 | 3,384 | 3,504 |
| loop, 20,000 turns, native, median of 3 (KB) | 3,804 | 3,876 | 4,012 |
| `loop-rss` growth over 10,000 more turns, release / native | 384 / 408 KB | 236 / 548 KB | 188 / 324 KB (bound 2,000) |
| 2,000 spawns, release, interleaved on a quiet host (s) | 0.47 | 0.47 | 0.47–0.48 (`spawn-and-gaps-aab5b78.log`) |

Rows that moved, by name: `pending/unset_env` → `env/unset_var` (pass),
`pending/signal_status` → `signal/child_term` (pass), `ctrl_c_prompt`
and `ctrl_c_child` (pass, no longer pending); 91 new differential cases
pass (25 `exec/`, 15 `env/`, 50 `signal/`, `simple/script_no_shebang`);
12 new session cases pass; 5 new pending cases, each named in
`tests/diff/PENDING.md` (`pending/exec_pid`, `pending/trap_usr1`,
`pending/trap_ignore_usr1`, `pending/wait_interrupted`,
`pending/subshell_signal`). `pending/pid` and `tilde/user` stay.

**Strict evidence (#571).** Every count above is a tool's exit status
read bare, with the per-case log kept
(`difftest-head-8aecb7c-release.log` `9b0c1923…`,
`session-head-8aecb7c-release.log` `f654da48…`); a pending case runs
and is printed `PEND-ok` or `PEND-fail`, never skipped. The spawning
rows also ran under `taskset -c 0-3` (`head-8aecb7c.log`: corpus
443/0/7 and sessions 85/0/0 on both tiers, pinned), and
`stress-8aecb7c.log` (`4a315d22…`) repeats the `signal`, `exec`, `env`
and `jobs` areas five times and the sessions twice, free, on 4 cpus and
on 1 cpu, both tiers: 0 failures in 30 corpus passes and 12 session
passes.

**Red before green.**

- *The pid witness.* `tools/exec-witness` against trunk's code at the
  pin: `pid FAIL … is 'pelt' with 1 children`, `env FAIL` (`GONE=x`
  still there, `MINE` missing), `status FAIL returncode 128`; against
  the head, and against dash: four rows ok, the pid the same before
  and after (`head-8aecb7c.log`, both tiers, free and pinned).
- *The poll race.* At `aab5b78` (the head before the barrier), pinned
  to 4 cpus: corpus native `436 7 7` — `signal/trap_eval`,
  `trap_exit_no_operand`, `trap_in_function`, `trap_in_subshell`,
  `trap_quit`, `trap_replaced`, `trap_usr2`, each "stdout" with the
  action never run — and session release `84 1 0` (`ctrl_c_trap_child`)
  (`head-aab5b78-before-the-barrier.log` `ce6c38ff…`,
  `difftest-head-aab5b78-native-taskset-red.log` `b526b6cf…`,
  `session-head-aab5b78-release-taskset-red.log` `616cde63…`); the same
  commit unpinned was green, which is why the pinned run is in the
  rule. The cause in a 15-line wolf program: `os_signal_poll` straight
  after `os_signal_raise` answers 0 in 2000 rounds of 2000
  (`poll-race-wolf-0.2.27.log` `adef7361…`, wolf-lang#691). Green at
  `8aecb7c` with the barrier (`sh.signal`'s `settle`).
- *The planted break in CI.* `c6ba091` (exec never replaces the shell;
  no variable is removed from the environment): run **38113174561**,
  linux job 114392768223, red at exactly four steps — "exec replaces
  the shell (same pid)" on both tiers and "the differential corpus" on
  both tiers — with `wolf test`, the memory gates and every earlier
  step green. Locally first: `plant-c6ba091-release.log` `b7822bbc…`
  (the witness's three FAIL rows; corpus `439 4 7`: `env/empty`,
  `env/only_pwd`, `env/subshell_export`, `env/unset_var`). Reverted in
  the next commit.
- *macOS.* Run **38112926258** at `a35afda`: linux x86-64 and linux
  aarch64 green; macOS green through the exec witness and the corpus
  on both tiers and red at "the session corpus, native tier" on one of
  this lane's own new cases, `ctrl_c_pipeline`, which named
  `/usr/bin/cat` (macOS has `/bin/cat`). Fixed in `aab5b78`.

**The syscall list of the static build** (`tools/build --static`,
`tools/syscall-census`: the whole corpus and every session under
`strace -f -ff`, counting only calls made in pelt's own image — the
shell, its threads, and each forked child up to its `execve`;
`census-head-8aecb7c.txt` `59e8ccf7…` against
`census-trunk-3e7516c-at-0.2.26.txt` `d6b75225…`; under strace the head
is still 443/0/7 and 85/0/0). Trunk at 0.2.26 makes 31 distinct calls
and the head 41. **New at the head:**

| call | why | when |
|---|---|---|
| `execve` in the shell's own process, no `clone` before it | `exec cmd` (`os_exec`) | each top-level `exec cmd` |
| `clone3` with `CLONE_VM\|CLONE_FS\|CLONE_FILES\|CLONE_SIGHAND\|CLONE_THREAD\|CLONE_SYSVSEM\|CLONE_SETTLS\|CLONE_PARENT_SETTID\|CLONE_CHILD_CLEARTID` | the runtime's signal thread (`wolf-signal`) | the first listen: any `trap` of a signal, and **every interactive start** |
| `mmap` (`PROT_NONE` then `MAP_STACK`), `mprotect`, `madvise(MADV_GUARD_INSTALL)`, `munmap` | that thread's stack and guard (glibc) | with the thread |
| `prctl(PR_SET_NAME, "wolf-signal")` | the thread's name | with the thread |
| `futex` (`FUTEX_WAIT_BITSET_PRIVATE`, `FUTEX_WAKE_PRIVATE`) | the queue between that thread and the shell | every poll that waits, every barrier |
| `rt_sigreturn` | a handler returning | every caught signal |
| `kill(getpid(), SIGTTIN)` and `getpid` | pelt's barrier (`os_signal_raise` of `BG_READ`) | after each child is reaped while a signal is listened for |
| `readlink` (`/proc/self/exe`) | `os_exe`, to run a script with no `#!` line through `exec` | that case only |

Already made by trunk and made MORE at the head: `rt_sigaction` (now
with a handler and `SA_RESTART` for HUP, INT, QUIT, TERM, USR2 and
TTIN, with `SIG_IGN` and `SIG_DFL`; trunk's are the spawn's own in the
child), `rt_sigprocmask` (`SIG_UNBLOCK` of each listened signal),
`pipe2(O_CLOEXEC)` (the self-pipe), `read`/`write` on it. **Not
asked for:** `setpgid`, `tcsetpgrp` (`ioctl(TIOCSPGRP)`), `tcsetattr`,
`sigaltstack`, `waitid`, `tgkill`; `ioctl` is still only `TCGETS` (10
calls, `os_isatty`), `wait4` is unchanged in kind. The list is glibc's
on kasumi (CachyOS): a PAX build links another libc and should re-take
it with the same tool.

**Gaps filed, each with its witness** (`spawn-and-gaps-aab5b78.log`
`e20903f9…` holds the dash and pelt runs): wolf-lang#679 (no meaning for
USR1, ALRM and the rest; and `os_signal_listen(512)` answers `ok`),
#680 (no non-blocking or interruptible child wait), #681 (no read of a
disposition), #682 (`os_spawn_fds` hands a file with no `#!` line to
`/bin/sh` where `os_exec` answers `io`), #691 (the poll race).

## 5. Prediction against result

| predicted (§3) | result |
|---|---|
| the pin alone moves no verdict | **right**: 350/0/4 and 71/0/2 on both tiers, the same PEND rows |
| the archive's `std/STD-REV` is the std pin | **right** |
| stripped size at the pin moves < 5% | **right**: +0.5% native, +1.5% release |
| the 20,000-turn peak at the pin moves < 25%, `loop-rss` green | **right**: +3% release, +2% native |
| `exec cmd` keeps the pid, on both tiers, linux and macOS | **right** on linux (kasumi, CI) and on macOS (run 38112926258's two witness steps) |
| no `EXIT` trap after `exec` | **half wrong**: none when the program runs; when the exec FAILS dash runs the `EXIT` trap as the shell ends, which the first build did not (`exec/exit_trap_when_it_fails`) |
| 126 and 127; the shell ends even when interactive | **right** (`exec/not_found`, `not_executable`, `directory`; session `exec_missing`) |
| a file with no `#!` is run by pelt itself | **right for `exec`**; for a plain command it never reaches pelt: `os_spawn_fds` hands the file to `/bin/sh` itself (wolf-lang#682, not predicted) |
| `pending/unset_env` passes; an empty environment is exact | **right** (`env/empty` prints nothing; a name dash drops, `a.b=1`, is dropped: by hand, `spawn-and-gaps-aab5b78.log`) |
| `pending/signal_status`, `ctrl_c_prompt`, `ctrl_c_child` pass | **right**, on linux; on macOS in CI |
| corpus pending at the head: `pid`, `tilde/user` and at most three gap cases | **wrong**: seven. The USR1 gap took two cases (caught, ignored), and two were not predicted at all: `pending/exec_pid` (the corpus cannot see a pid without `$$`) and `pending/subshell_signal` (a signal sent to a subshell's process reaches the shell: no fork) |
| `trap` catches HUP, INT, QUIT, TERM, USR2; ignore inherited; reset; a caught signal default in a child | **right**, with one thing not predicted: two signals that arrive together run in the order of their NUMBERS under dash, and wolf's queue had them in the order their handlers finished (`signal/trap_two` red on the first build); pelt polls by number |
| `$!` a process id; a background child ignores INT and QUIT | **right** (`signal/bang_is_a_process`, `background_ignores_int`) |
| gaps (a) no meaning, (b) uninterruptible `wait`, (c) ignored-at-entry | **right**, filed #679, #680, #681 |
| — | **not predicted: the poll race** (wolf-lang#691). Every trap case passed on 16 free cpus and seven failed on four; found only because the contract demands the pinned run |
| — | **not predicted:** the harness itself decided signal cases: a corpus started under `nohup` or from a background job inherits HUP, INT and QUIT ignored, and dash then refuses to trap them. `tools/lib_cases.py` now starts every case with the defaults, and the whole corpus re-recorded with 0 drift |
| — | **not predicted:** at an empty prompt, dash 0.5.13.4 loses the newline of the line typed after Ctrl-C (`^C`, `echo after`, `exit` runs `echo afterexit`). Not copied; no case |
| `loop-rss` green at the head; 2,000 spawns at most 15% slower | **right**: 188 KB over 10,000 turns (release); 0.47 s against 0.47 s. With a trap set the barrier adds nothing measurable (0.64–0.68 s against 0.56–0.67 s on a loaded host) |
| new syscalls: `execve` without a fork, `rt_sigaction`, `rt_sigreturn`, `rt_sigprocmask`, `pipe2`, a thread and `futex`; not `tcsetpgrp`, `setpgid`, `tcsetattr` | **right as far as it went**; `rt_sigaction`, `rt_sigprocmask` and `pipe2` were already in trunk's list (the spawn's), so they are more, not new; **not predicted:** the thread's `mmap`/`mprotect`/`madvise`/`munmap` and `prctl`, `readlink`, and `kill` + `getpid` from the barrier |
| — | **not predicted:** the head's binary is 15–17% larger stripped than the pin's code (the signal thread, the task park behind `os_signal_wait`, the exec module) |

**What was not verified.** The `exec-witness` rows and the session
cases on macOS are CI's, not a local run (no build on nomad-1). The
syscall list is from a glibc static build on kasumi, not from the
binary PAX builds. The checked machine and lupin run no pelt (pelt
builds on the native and release tiers only). Gap (c), a signal
ignored at entry, has a hand witness and no corpus case. Whether dash's
order for simultaneous signals is by number in general, or only for
the pair measured (HUP and TERM), was not explored further.

## Done-when

Branch `sh05`, one pull request, unmerged; the commit list, the test
checklist and the CI run at the head are in its body. Nothing is
closed by this lane. To close at merge: nothing in pelt (pelt#6 is
untouched). wolf-lang#679, #680, #681, #682 and #691 stay open for a
compiler lane.

**For sh06.** Job control (`fg`, `bg`, `jobs`, Ctrl-Z) waits on stop
reporting, `SIGCONT` and a signal to a group (`[os.term.note]`), and on
#680 for a `wait` a trap can interrupt and for reaping without
blocking. Line editing can start now: `os_term_mode` and
`os_term_set_mode` are in 0.2.27 and unused. `settle` retires when
#691 is fixed. `$$` waits on #141. `kill` as a built-in (job ids)
waits on #141 too.
