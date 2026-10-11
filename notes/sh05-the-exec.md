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
