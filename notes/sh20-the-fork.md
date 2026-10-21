# sh20 — the eighth pin and the fork (pelt#34; wolf 0.2.34 / lupin 0.1.55)

Contract: `sprints/pelt/23-the-fork/sh20-the-fork.md` in the planning
repo (ruling #90: "prioritize writing the fork"; ruling #95: the fork's
shape, R4 C for the checked machine). This file is the lane's record:
§1 to §3 are committed before the first change under `src/`, `tools/`,
`tests/`, `.github/` or `wolf-toolchain.toml`; the rest is filled in as
the work lands.

## 1. Forbidden

As the contract and `sprints/RULES.md` say. No shell's source is read or
searched for (dash, bash, busybox, mksh, zsh or any other), nor a libc's
or a kernel's. Behaviour comes from POSIX.1-2024 (XCU 2.9.2 Pipelines,
2.9.3.1 Asynchronous AND-OR Lists, 2.11 Job Control, 2.12 Signals and
Error Handling, 2.13 Shell Execution Environment, the `trap`, `wait`,
`jobs` and `exec` pages), dash's manual as documentation, wolf's spec at
`v0.2.34` (`spec/11-os.md` `[os.proc.fork]`, `[os.proc.fork.note]`,
`[os.proc.job]`, `[os.term.group]`), the probe fixture
`crates/wolf_driver/tests/fixtures/fork/subshell.lu` (the shape to copy,
never to edit), the maintainer's own `wolf_rt` read where the spec points
at it, and black-box runs of dash 0.5.13.4 and bash 5.3.20. No change to
`os_fork` or anywhere in wolf-lang: a defect there is an issue, listed,
with the row that shows it. No assertion deleted or weakened; no timeout
or retry as a fix. Toolchains from the release archives by digest, each
read twice. No build on nomad-1: kasumi under `~/lanes/sh20/`, detached
jobs by `setsid -f` with the pid recorded (`notes/sh20-evidence/launch.sh`)
and stopped by that pid only. **Every run that starts, signals, forks,
times out or kills a process runs inside this lane's own container**
(`notes/sh20-evidence/ctr.sh`: rootless podman, its own pid namespace
with an init, `--network none`, a pids limit, kasumi's `/usr` read only;
`ulimit -c 0` inside), never on kasumi's host process table (RULES §5);
measurements also under `taskset -c 0-3`. Only the compiles run on the
host. No merge, no tag, no issue filed or closed, no package installed on
a host, no other lane's CI run cancelled, nothing under `~/.claude`, no
attribution trailers. If the harness refuses an action, the lane stops
and reports.

## 2. Inputs, verified (2026-10-21, before any change)

| input | contract says | measured | drift |
|---|---|---|---|
| pelt trunk | `3b0bab9` (sh22 at `01fec4d`, then tl30) | `origin/trunk` = `3b0bab9881f5…`; `01fec4d` is sh22's last commit, then tl30's five (`266757b`…`3b0bab9`); branch `sh20` cut from it in its own worktree; two kasumi clones at the same commit (`base`, `pelt`) | none |
| pelt's pin | the seventh, 0.2.32 / 0.1.54 | `wolf-toolchain.toml`: wolf 0.2.32 `72de141f…`, lupin 0.1.54 `0e536e8f…`, std `d37c911` | none |
| wolf 0.2.34 | `v0.2.34` at `9da7bdcf`, release 419552903 | tag object `38ab81cb…` → commit `9da7bdcf2aea9adf48df6570bedc58e16e9ef853`, read twice; release 419552903 | none |
| its digests | x86-64 `88a9dd3d…`, aarch64 `ca5cadf9…`, macOS `29c8331f…`, windows `77bb8403…` | the release API read twice: x86-64 linux `88a9dd3da1c9a0e3…c1821`, aarch64 linux `ca5cadf936dc0d43…c3ad0`, macOS arm64 `29c8331f5d188b00…36ee3`, windows `77bb8403aeeae9f0…f07` (pelt pins no windows archive) | none |
| lupin 0.1.55 | `v0.1.55` at `e642f26`, linux x86-64 `1152abc0…` | tag object `047184fb…` → `e642f2630ad4c7f53740428d5cca705f2e0d295b`, read twice; release 418932753 read twice: linux x86-64 `1152abc0bef65d33…48a38`, aarch64 linux `5854ab268a835bb7…45d7`, macOS arm64 `2eac1cccdc8a5bec…741a` | none |
| the bundled std | wolf-std `e036bec` | `crates/wolf_driver/STD-PIN` at `v0.2.34`: `e036bec318ad81ecd5a025612bc2c2adb17527f3`; `PAIRING`: lupin 0.1.55 at pin `294d626` | none |
| r39's measurement | pelt `be1a75d` on 0.2.34: 961 / 0 / 38, 264 / 0 / 3, every log byte-identical to the 0.2.33 control | `crawl-54.md` (r39's read-back): as the contract says. Trunk is five corpus cases and nine sessions past `be1a75d` (sh21 +1 and +9, sh22 +4): **966 / 0 / 38, 273 / 0 / 3** at the seventh pin | trunk's counts are not r39's: the pin is measured against trunk's own run on 0.2.32 |
| `[os.proc.fork]` | `os_fork() -> (int, int) ! {busy, io, unsupported}` | as said: `(pid, h)` in the parent (the handle every table call serves), `(0, -1)` in the child; one thread; every descriptor shared; dispositions and the mask kept, nothing pending; the hub re-made (its drain thread at the first wait or listen); empty wait tables (the parent's handles answer `io`); `busy` from a task or with one live; the checked machine `unsupported`; lupin 0.1.55 does not resolve the name (wolf-interp#269) | none |
| `[os.term.group]` | — | `os_set_pgid` moves the **calling** process only; a child's group is set at its spawn (`os_spawn_job`), never after. So a forked child must move itself, and the parent cannot repeat it: the parent waits for the child's word before it starts the next stage of the job (§3.2) | a constraint the contract does not name |
| `os_exit` | `_exit`'s path | `wolf_rt/src/os.rs`: `__wolf_rt_os_exit` dumps a profile (no-op), restores a registered terminal (pelt registers none; a fork's child "restores nothing", `[os.term.restore]`) and calls `std::process::exit`; no `defer` runs, no pelt exit path (`jc_leave`, the editor's mode) | none |
| the probe fixture | the shape | `fixtures/fork/subshell.lu` at `v0.2.34`: fork, the child `os_signal_default`s the listened set and runs, `os_exit(status)`; the parent `os_wait_status(h)` and prints `128 + N` for a signal | none |
| sh19 §6 | the adoption note | read whole (§6.1–§6.5); its `probe/shapes/shapes.sh` is this lane's acceptance probe | none |
| pelt#34 | open | open: "a pipeline with a stage pelt runs itself, and `( … ) &` / `{ …; } &`, are not jobs until subshells are processes" | none |
| pelt#47 | open | open: `wait %1` after a job was reaped prints a stale signal notice (sh22; the first recording of `wait/c_unwaited_many_status`, `notes/sh22-evidence/logs/red-41-pre.log`) | none |
| tasks in pelt | pelt runs none | `src/`: no `scope`, `.spawn(`, `spawn proc` or `channel[`; so `busy` is never answered (§3.4) | none |
| kasumi | `/home` tight | 27 GB free at the start, load 6.8 (other lanes); dash 0.5.13.4-1.1 and bash 5.3.20-2 (the oracle of record, `tests/diff/ORACLE`) | — |

### 2.1 What dash's subshell processes are, black box

`probe/childstate.sh` (each shape's process found as its child's
`PPID`, its `SigIgn` and process group read from `/proc` and `ps`), run
inside the container under dash 0.5.13.4 as a script, as a `set -m`
script, and typed at `dash -i -m` through a pty started with every
signal at its default (`probe/childstate-run.sh`, `probe/typein.py`;
`logs/probe/childstate.dash.txt`, bash's beside it). `SigIgn` in linux's
numbering: `0x6` INT and QUIT, `0x280000` TSTP and TTOU, `0x284004`
QUIT, TERM, TSTP and TTOU, `0x1` HUP.

| shape | script: ignored, group | `set -m` script | typed, `-i -m` |
|---|---|---|---|
| the shell | 0, — | `0x280000`, — | `0x284004`, — |
| `( … )` | 0, the shell's | 0, **leads its own** | 0, leads its own |
| `$( … )` | 0, the shell's | **`0x280000`**, the shell's | `0x280000`, the shell's |
| a program inside `$( … )` | 0 | `0x280000` | `0x280000` |
| `( … ) &`, `{ …; } &` | **`0x6`**, the shell's | 0, leads its own | 0, leads its own |
| a program after `&` | `0x6` | 0 | 0 |
| first stage `{ …; } \| cat` | 0, the shell's | 0, leads its own | 0, leads its own |
| last stage `: \| { …; }` | 0, the shell's | 0, **the first stage's group** | 0, the first stage's |
| `( … )` after `trap … USR1 TERM; trap '' HUP` | `0x1`; `trap` prints only `trap -- '' HUP` | the same, leads its own | the same |
| `( trap 'echo …' INT; kill -INT <itself> ) &` (started ignoring INT) | **caught** | caught | caught |

So: every subshell sets caught traps back to the default and keeps the
ignored ones (2.13); a subshell of an interactive shell drops the
shell's own ignores; with job control on, every subshell that is a job
or a job's stage gets the defaults and a group (its own, or the job's),
**a command substitution is not a job**: it stays in the shell's group
and keeps `TSTP` and `TTOU` ignored, and so do the programs it starts;
with job control off, an asynchronous list starts with INT and QUIT
ignored, and a trap it sets on them takes effect (they are not
"ignored on entry").

## 3. Prediction (committed before the first change)

### 3.1 The eighth pin alone (0.2.32 / 0.1.54 → 0.2.34 / 0.1.55, no source change)

What 0.2.33 and 0.2.34 change that pelt could see, read from the
CHANGELOG's "Read this before you bump": twelve new prelude names (pelt
declares none of them: W0304 cannot fire), one new mark (`busy`); a
program naming `os_signal_wait_fd` starts with two more descriptors (the
shared wake pipe; pelt's shell descriptors are its own table, and no
case reads the host's descriptor numbers); a mode int without bits 5–7
writes the usual setting (`ICRNL`, `OPOST` on, `ISTRIP` off; the pty a
session runs in starts there, and `tools/edit-witness` reads `ICANON`,
`ECHO`, `ISIG`, `IEXTEN`, `IXON`, none of the three); `os_signal_text(0)`
(pelt never asks); a SEGV another process sends ends a program (no case
sends one); `wolf test` runs a test file's own `test_*` (pelt's
`src/sh_test.lu` has only `main`, and 0.2.32 already ran
`./sh_test.lu::main`).

**Predicted:** no verdict moves. Corpus **966 / 0 / 38**, sessions
**273 / 0 / 3**, statements **505 of 547**, every gate 0, on both tiers
and under `taskset -c 0-3`; every corpus and session log byte-identical
to the seventh pin's run of the same tree; `wolf test` "1 passed". r39's
`be1a75d` counts (961 / 0 / 38, 264 / 0 / 3) are that commit's; the five
corpus cases and nine sessions since are sh21's and sh22's. lupin 0.1.55
still refuses pelt at resolve (it refused at `os_signal_default` at
0.1.54, sh18); the checked machine still runs pelt to its end.

### 3.2 The shape (sh19 §6.5, made concrete)

One door in `sh.exec`: the parent flushes `sh.out`, makes the pipe the
child's output goes to where there is one, and forks. **The child**
(before anything of the body runs, in this order): moves into its job's
group when job control says so (its own for a job's first process, the
job's for a later stage) and, for a foreground job's leader, takes the
terminal; tells the parent it has (one byte's pipe, closed: the parent
cannot repeat a forked child's `setpgid`, §2); points every descriptor
that names one of the parent's captures at its pipe; closes the parent's
handles it does not name (a pipeline's other ends, the job table's
terminal handle, the captures' temporary files); empties the job table
(`jb_*`, `pr_*`, the stash) and turns job control off; is not
interactive; sets every caught trap back to the default and keeps the
ignored ones, then lets `sig_apply` put the process's dispositions where
that table says (the interactive shell's own INT, QUIT, TERM and job
control's TSTP, TTOU back to the default for a job; a command
substitution keeps TSTP and TTOU ignored as dash's does); after `&` with
job control off holds INT and QUIT ignored unless a trap of its own says
otherwise; then runs the body with `$$` still the shell's (now a field
the fork copies, no longer `os_pid()` at each `$$`); runs its own `EXIT`
trap; flushes; and ends by `os_exit` with the subshell's status, never
by pelt's exit path. **The parent** records the child as a job's process
like any spawned program (`$!` its pid; a foreground job waited for by
the poll, Ctrl-Z seen as a stop), or waits for it (`os_wait_status`), or
reads its pipe to the end first (`$( … )`).

**Which shapes fork:**

- `( list )`: forks, unless `list` is one simple command that the fast
  path finishes (a program or a pure built-in: in-process today at
  4.5–6 µs, and what can be seen of it is the same, sh19 §6.1's second
  row). Such a command that the fast path does not finish (a function,
  `cd`, `exec`, `eval`, `read`, `wait`, `jobs`, a word with a
  substitution in it) forks at the point it would have taken the
  ordinary path.
- `$( list )`: the same rule; except **`$(trap)`**, one `trap` command
  alone, which keeps the parent's traps (the exception POSIX's `trap`
  page allows, dash's answer: `signal/c_trap_cmdsub_shows_parent`).
- `list &`: forks, but for a simple command the fast path starts as a
  program (as today). A built-in after `&` forks too (`true &`), as
  dash's does.
- a pipeline stage: forks, but for a simple command the fast path
  finishes (a program, started on the stage's pipe; a pure built-in,
  its output fed). The last stage forks by the same rule.
- on the checked machine (`unsupported`) and on `busy`, every shape
  runs in process exactly as at trunk; `pipe_is_job`'s rule (a
  pipeline with an in-process stage is no job) is kept for that case
  alone.

### 3.3 The rows

**Green with the fork alone** (a process, its own descriptors): 
`env/c_subshell_concurrent`, `pipe/c_concurrent_stages`,
`pipe/c_shell_producer_ends` (the producer's own copy of its pipe's read
end closed, SIGPIPE at the default), `builtin/c_s_dot_special_file` (the
`&` inside the subshell forks, so the subshell ends before `.` reads the
FIFO), `redir/c_s_cmdsub_fd_pipeline` (the substitution's descriptor 4
is its pipe in the child), `wait/c_subshell` (the child's job table is
empty: 127), `signal/c_trap_ignore_pipe` (the ignored PIPE kept, the
write fails with status 1).

**Need the trap reset as well:** `pending/subshell_signal` (the child's
TERM at the default: 143, the parent's trap does not run),
`signal/c_subshell_trap_reset` (`( trap )` lists nothing, the parent's
`EXIT` trap does not run in the child, TERM at the default: 143).

**Need the group:** `session:c_jc_mixed_pipeline` (the `while` stage
joins the job's group with SUSPEND at the default; the pipeline is a
job; Ctrl-Z stops it; `jobs` says `Stopped`).

**Not the fork's:** `signal/c_trap_cmdsub_shows_parent` (the lone-`trap`
choice above, P10's `$(trap)`, pelt#17).

**Recorded differences that move:** `signal/c_wait_interrupted_term`
stays green, now by dash's order (its sender runs concurrently and cuts
`wait` short); sh19 §6.1's probe (`probe/shapes/shapes.sh`) answers as
dash's on every row.

**New cases** (each recorded from dash, each red at the pin, green at
the head): the endless producer `while :; do echo y; done | head -n 1`
(the "no case" item of `tests/diff/PENDING.md`: at the pin it never ends
and the harness times it out); `exec` in a subshell replaces the
subshell's process (the other "no case" item); a program started inside
`( … )`, `$( … )` and after a shell stage has the subshell, not the
shell, as its parent; `$!` of `( … ) &` and `{ …; } &` is a live
process. Sessions: a foreground subshell `( … )` stopped by Ctrl-Z and
brought back by `fg`; a backgrounded subshell the prompt comes back
before; `$(jobs -p)` at a prompt with a job running answers empty.

**Counts at the head, predicted:** corpus **(966 + new) / 0 / 28** on
both tiers and under `taskset` (the nine fork rows and the `$(trap)`
row leave pending); sessions **(274 + new) / 0 / 2** (`c_ignoreeof` and
`c_mail` stay); statements **at least 515 of 547** (the nine `pending
(fork)` statements, 2.9.2/8, 2.9.2/9, 2.11/18, 2.13/6, 2.13/7, 2.13/11,
2.13/12, wait/7, dot/8, and trap/10).

### 3.4 `busy`

pelt starts no task (§2), and `busy` is answered only from a task, with
a task live, or under the deterministic scheduler, so it never reaches
pelt. Were it to (a task started for some later reason), a shell cannot
wait for its own tasks inside a subshell's start, so pelt would do what
it does on the checked machine: run the shape in process, to its end.
**The row that proves it:** a table check (`sh.selftest`) that calls
pelt's fork door with a task parked in a scope and wants the in-process
answer and no child; and pelt's syscall census at the head shows a fork
from `main`'s thread with no worker threads made.

### 3.5 What the parent keeps a turn (`tools/shape-rss`'s method)

A fork costs the parent what a spawned program costs it: the runtime's
child-table entry (a `Vec` slot per child, never reused: about 40 B, and
the vector's doubling between N and 2N), the pipe's two handles, and the
job slot where the shape is a job. The bare loop keeps 36–59 B a turn
(sh22). **Predicted, both tiers, at N = 10,000 → 20,000:** a forked
`$( … )` (`x=$(true; true)`), a forked subshell (`( true; true )`), a
backgrounded group (`{ true; } & wait`) and a forked stage (`{ true; } |
true`) each **60–140 B a turn**, the same order as the `env true & wait`
row (85–120, sh22), inside the gate's bound (100 B a turn plus 1 MiB);
the existing 39 rows unchanged within their noise. dash keeps 0–16. The
child's memory is not the parent's; **its exit leaves nothing the parent
sees**: no temporary file, no descriptor, no terminal mode or group
change (`tools/edit-witness`, the sessions' mode check).

### 3.6 Cost (sh19's bench, information)

`probe/bench` under `taskset -c 0-3` in the container, per turn: dash
forks at 100–156 µs a shape; s247 measured a toy's fork, exit and wait
at 119 µs. pelt's resident set is larger than the toy's and its child
does more before the body (the dispositions, the closes), so predicted
**150–300 µs** a forked shape, **1.5–2.5× dash's**: sh19's target (no
slower than dash) is predicted **not met**, and said with the number.
The shapes kept in process stay at today's 5–45 µs.

### 3.7 The checked lane (ruling #95 R4 C)

`wolf conform-run --json --checked src/pelt.lu < script` for a script
of the five shapes answers `exit(0)` with the in-process bytes: the
ordered outputs equal to the native head's, the concurrency rows in
trunk's order (`a b` where native says `b a`), `$!` of a background
subshell a number no process has; recorded as sh18's machines rows.

### 3.8 PAX

Nothing measured there. The list of rows a pax lane (px58 or after) must
replay with the forking pelt: the nine fork rows, the `$(trap)` row, the
new cases and sessions, `probe/shapes/shapes.sh`, and the syscalls the
census adds (predicted: more `clone` without `CLONE_VM` from pelt's own
forks, `setpgid` and `exit_group` in the children, `pipe2` for each
child's hub, and no new name).

### 3.9 pelt#47 (if in reach)

`wait` says "ended by signal" only when the wait itself saw the job end;
a job a poll reaped earlier (as the next job started) answers its status
silently, as dash's does. A case without `2>/dev/null` on that `wait`,
red at the pin, green after; `wait/c_unwaited_many_status` unchanged.
