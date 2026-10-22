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

### 3.10 After the pause: a redirected subshell's process (2026-10-22)

At the pause one corner of `probe/corners.sh` differed from dash:
`( kill -TERM $(sh -c 'echo $PPID') ) 2>/dev/null`. dash says that the
signal ended the subshell on the shell's own standard error; pelt said
it inside the subshell's `2>/dev/null`. Black box, the difference is
wider than the notice (`probe/notice.sh`, `notice2.sh`, `notice3.sh`,
`notice4.sh`, `notice5.sh`, `trapwait.sh`; 81 shapes, dash's answers in
`logs/probe/notice*.dash.txt`): **a subshell's own redirections, and
those of braces that hold it alone (`{ ( … ); } 2>f`,
`{ { ( … ); }; } 2>f`, `{ ( … ) 2>/dev/null; } 2>f`), are the subshell
process's.** So in dash, while such a subshell runs, nothing the shell
does is under them: the notice of its end, a trap's action for a signal
the shell heard meanwhile (run after the subshell and before the next
command), the `Stopped` notice of `( … ) 2>/dev/null` stopped by
Ctrl-Z; and a failed redirection is the subshell's status 2, which
`set -e` acts on. A brace group with more in it (`{ ( … ); :; } 2>f`), a
loop's, an `if`'s, a `case`'s and a function call's redirections are
the shell's: there the notice goes into `f`, in dash and in pelt alike.
The same braces-around-a-subshell shape forked as a stage, a
substitution or after `&` is one process in dash (its stage's end is
said by the parent on its own standard error).

At `b448c1e` pelt applied a `( … )`'s redirections in the parent
(`sh.exec`'s `run`) around both forking paths (`run_paren` forking the
whole node, and `run_simple` forking a one-command body off the fast
path inside `run_subshell`'s frame), and around the in-process path of
`( program ) >f`; so the notice, the trap's output and the stop notice
went into the redirection, and `set -e; ( echo ) >/nonexistent/f` went
on. The attempt reverted at the pause (deferring the notice to after
`end_redirs`) covered only the first path and none of the trap, stop or
`set -e` cases. **The fix** (`9b04506`, on the branch `b4bca4a`; every
older sha is mapped in §4): `run` sends a node that is `paren_alone` (a
subshell, or braces holding one alone) with redirections of its own to
`run_paren_redir`, which forks the whole node whatever its body, a
foreground job of its own under job control as `run_paren`'s; the
child's `child_body` unwraps subshells and now braces that hold one
alone, applying each one's redirections in the child; the parent's
`node_end` (`run_node`'s tail, factored out) sets `$?` and runs the
traps after the command. A host that does not fork keeps the old
in-process path. The cost: `( program ) >f` is a fork and an `exec`
where it was a spawn (dash forks there too).

Rows from dash, each red at the pin and at `b448c1e` and green at
`9b04506` on both tiers (`logs/notice/new-rows-*.log`,
`logs/notice/sess-redir-stop-b448.log`), and red again in both plants
(§4): `signal/subshell_end_said_outside` (twelve shapes, three of them
the shell's own redirections), `signal/subshell_end_devnull` (the
corner), `signal/trap_after_redirected_subshell`,
`redir/subshell_redir_fails_set_e`, the session `jc_subshell_redir_stop`
(Ctrl-Z's notice, `err yes`), and `tools/shape-rss`'s
`fork-redirected-subshell` (`( true ) >/dev/null` in a loop). At
`9b04506` the 35 corners answer as dash's on both tiers but for the
notice's words (dash `Terminated`, pelt `pelt: ended by signal 15
(TERM)`; the corpus compares standard error by its presence),
`logs/probe/corners-9b04506.txt`; and of the 81 notice shapes all but
one, which is not the fork's: `sh -c 'kill -TERM $$' 2>f`, a simple
command's own redirection, where dash says the end inside `f` and pelt
on its own standard error, at trunk too (`notice.pelt-native-pin.txt`
row 07; §7).

### 3.11 The ~1.2 MB above the pin's peak: the binary's mapped pages, not pelt's memory

Pass 1 of the table (before the pause, `logs/table/`) had the head's
native loop peaks 1.2–1.3 MB above the pin's at the same turn count,
the bare loop too (`baseline` 6,588 against 5,268 KB at 10,000 turns,
7,064 against 5,856 KB at 20,000), with the same order of growth a turn
(48 against 60 B). It is not memory pelt allocates.
`probe/rss-split.sh` reads a pelt's own `/proc/self/status` after a
10,000-turn `:` loop, twice a binary, inside the container, in three
runs: `logs/rssgap/split-run1.txt` (2026-10-21 about 21:31; the head
then `251362c`'s build, `9a6baf2e…`), `split.txt` (about an hour later,
after `probe/table.sh` had copied the binaries; the head `0ca2ab2`'s
build `999936bc…`, beside snapshots of `8b8d470` and `b448c1e`) and
`split-final.txt` (2026-10-22 08:47, the final head `b05b0cf`'s
`ef5c6c66…` and `abee983c…`, every binary from its build tree,
`taskset -c 8-11`). In KB:

| | pin, native | the heads, native | pin, release | the heads, release |
|---|---|---|---|---|
| `RssAnon`, every run | 808–816 | 824–840 | 696–704 | 700–708 |
| `RssFile`, run 1 | 4,940–4,980 | 5,148–6,468 | 3,232–3,256 | 3,296–3,312 |
| `RssFile`, run 2 | 5,884–5,956 | 6,056–6,212; `0ca2ab2` 5,192–5,288 | 3,236–3,296 | 3,260–3,324 |
| `RssFile`, the final head | 5,800–5,888 | 5,320–5,332 | 3,264–3,284 | 3,284–3,292 |

The file-backed share follows the file's page-cache history, not the
build: the pin's binary, never rebuilt, mapped about 0.9 MB more in the
second run than in the first; two byte-identical copies of `251362c`'s
binary (`9a6baf2e…`, the build tree's written by the linker and
`snaps/fx1`'s written by `rsync` and read through by `sha256sum`)
mapped 5,164–5,216 and 6,212–6,468 KB in the same run; and in the final
run the head's native peak is *below* the pin's (6,144–6,160 against
6,608–6,700 KB `VmHWM`) with 12–20 KB more anonymous memory. Pass 1's
head ran from the frozen copy `snaps/t2` (made by `snap.sh` for the
table's second job at 19:04), the pin from its build tree. The bare
loop's peak by `tools/shape-rss` (`logs/rssgap/gap.txt`, its cpus not
recorded; `gap-cpus.txt`, cpus 8–15 and 0–15): at 20,000 turns
`8b8d470` +144 to +428 KB over the pin's, `b448c1e` +64, `9b04506` −72
to +268; `pelt -c :` starts at 4,468–4,836 KB for the pin, 4,684–4,996
for `8b8d470`, 4,700–4,936 for `b448c1e` and 4,588–4,916 for `9b04506`.
So `b448c1e`'s premise, that a `scope` named in pelt's own program made
a native pelt start 1.2–1.4 MB larger, was this artefact: `8b8d470`,
with the scope, starts within 0.2 MB of the pin. The task stays in
`src/selfcheck.lu` (pelt names no task, which costs nothing).

**Bound:** after 10,000 turns a head's anonymous memory is within 32 KB
of the pin's native and 12 KB release, every head measured; the final
head's is 12–20 KB above the pin's native and 0–4 KB release. The final
table copies every binary the same way before its passes
(`probe/table.sh`), but its peaks still carry the file's share, so the
gate (`tools/shape-rss`) and this note judge growth a turn, which the
mapping does not move.

### 3.12 Found on the way, not the fork's: a redirected compound command keeps ~690 B a turn

`tools/shape-rss` had no row for a compound command with a redirection.
`probe/compound-redir-rss.sh` (`logs/rssgap/compound-*.txt`, every
binary under `taskset -c 4-7`): at trunk `3b0bab9` (built at 0.2.32),
at the pin and at the head (`0ca2ab2`'s build), `{ true; } >/dev/null`,
`if true; then :; fi >/dev/null` and `while false; do :; done
>/dev/null` in a loop keep 644–721 B a turn on both tiers (11.6 → 18.3
MB native over 10,000 → 20,000 turns), where a simple command's
redirection keeps 18–67 B and dash nothing (−11 to 0). A redirected
subshell kept as much at trunk and at the pin (651–707 B) and keeps
42–65 B a turn since it forks (§3.10; the new `shape-rss` row holds
it). The frame `run` applies for a compound command keeps what it
allocates in the shell's root; that is the shell's own path, not the
fork's, so it is left for an issue (§7).

### 3.13 Two rebases, and R-sh23-4 taken here

sh23 (`set -o autocd`, pelt#51) landed first: trunk `2dc8dbe`; then
pelt#52 (the README made a map, the old record moved whole into
`docs/CHANGELOG.md`): trunk `c10bad1`. `sh20` was rebased onto each (the
heads before them kept on origin as `sh20-prerebase`, `fd20549`, and
`sh20-prerebase2`, `e87118a`); every sha this note cites from before is
mapped in §4. The conflicts were the README alone: sh20's README commit
(`4cac139`) fell away empty at the second rebase; the fork's record is
`docs/CHANGELOG.md`'s entry under `## Unreleased` (`9e24844`), and the
README says what is true at the head: the fork in "What works", the
checked machine's in-process shapes under "What it does not do yet"
(`b05b0cf`), the status table's counts at the head and the script
census's three fork-bound scripts no longer a gap (`0c77c22`, §3.14).
`exec.lu`'s `run_external` (sh23's one check before `unfound`) and
`builtin.lu`'s option table merged without a conflict.

**R-sh23-4** (sh23 §7: pelt autocds inside `( )`, `$( )` and pipeline
stages where bash 5.3 and zsh 5.9 do not; `x=$(DIR)` answers 0 in pelt,
127 in bash and zsh, `x=$(./DIR)` 0 against 126), **taken in sh20 as the
orchestrator recommended, bash's line** (reversible by one line):
`autocd_dir` refuses when `sh.sub > 0` (`866c2a6`), besides when the
shell is not interactive, which a forked child is not; the hook
(`command_not_found_handle`) keeps sh20's `sh.interactive ||
sh.sub_of_i`. Rows, both seen red: the session `autocd_subshell` (from
dash, which has no such option, so its answers are the refusal's;
bash 5.3 with `shopt -s autocd` agrees, and takes the option at the top
level from the same first line, `logs/autocd/bash-control.txt`): red at
trunk `2dc8dbe` on both tiers (seven of its eight rows: `cs-bare st=0`,
`cs-slash st=0`, `[/sub]` in the substitution, both subshells, the
group in a pipe and the last stage; `logs/autocd/sess-t23-*.log`) and
in the plant 39715917270, green at the head (`sess-rb-*.log`); and the
table check `want_autocd` (`sh.selftest`), red on both compiled tiers
and under `wolf test` with the `sh.sub > 0` line removed while the
session stays green there, the fork's child being no longer interactive
(`logs/autocd/plant-*.log` on kasumi; CI plant **39715919419**,
`logs/plant/plant-94ca885.txt`). `eval` and a function body take the
option, as bash's do.

### 3.14 Found on the way: three real scripts

`probe/zgrep.sh` runs kasumi's own `/usr/bin/zgrep`, `xzgrep` and
`zdiff` (gzip 1.15, xz 5.8.3; run, never read) six ways under each shell
(`logs/zgrep/zgrep.txt`). dash and the final head's release pelt
(`abee983c…`) answer alike, byte for byte; the pin's pelt prints `test:
-eq: unknown operator` for every file (the decompressor's status these
scripts read through `$( exec 4>&1; { …; echo $? >&4; } | … )` is empty
without a process per stage: census 2.13/12) and its `xzgrep` exits 2
where dash's exits 0. They are sh13's three fork-bound census scripts.
`tools/script-census` itself (its own pinned copies, in images built
from pinned bases, which needs the network) was not run again, so the
census's 76 of 80 stands as measured before the fork, and the README
says so.

### 3.15 The result against the prediction

| §3 | predicted | measured | |
|---|---|---|---|
| 3.1 the pin alone | no verdict moves; corpus 966 / 0 / 38, sessions 273 / 0 / 3, statements 505 of 547, every gate 0 on both tiers and under `taskset`; every corpus and session log byte-identical to the seventh pin's run of trunk; `wolf test` 1 passed | corpus 966 / 0 / 38 on both tiers and both under `taskset`, each log identical to trunk's but its binary-path line; sessions 273 / 0 / 3 on all four runs, identical but the first line; the pin's witnesses (glob-, loop- and shape-rss, exec, edit, hist, signal and reap on both tiers, edit and signal also under `taskset`) and oracle-check every one 0, as trunk's at 0.2.32; statements 505 of 547 and `wolf test` 1 passed at both (`logs/gauntlet/base-pin-summary.txt`, `logs/pin.status`: the run stopped at the pause and its rest taken on 2026-10-22, "rest from") | held |
| 3.3 the fork rows | the nine green with the fork alone, two with the trap reset, `c_jc_mixed_pipeline` with the group; `$(trap)` the lone-trap rule | all green on both tiers at every head gauntlet; red at the pin in both plants (§4) | held |
| 3.3 new cases | each from dash, red at the pin, green at the head | eleven corpus rows (five in `924fac7`, #47's two in `61f9cf9`, four for §3.10), five sessions (three in `bb83b6d`, `jc_subshell_redir_stop`, `autocd_subshell`) and a `shape-rss` row; every one red in the final plant 39715917270 (at the final head's tests: 20 corpus rows and 6 sessions on each tier, the row and the table checks) but `wait/waited_signal_said`, the control that is green at the pin by design | held |
| 3.3 corpus at the head | (966 + new) / 0 / 28 | **989 / 0 / 28** on both tiers and both under `taskset` (trunk `c10bad1` 968 / 0 / 38, sh23's +2; +10 from pending, +11 new) | held |
| 3.3 sessions at the head | (274 + new) / 0 / 2 | **289 / 0 / 2** on all four runs (trunk `c10bad1` 283 / 0 / 3, sh23's +10; +1 from pending, +5 new; `c_ignoreeof`, `c_mail` stay) | held |
| 3.3 statements | at least 515 of 547 | **516 of 548** (95.0%; one statement added, 2.11/20) | held |
| 3.4 `busy` | never met; a row proves the in-process answer | `tools/self-check` on both tiers: "a fork with a task live is busy and runs in process"; `wolf test` (the checked machine): `unsupported`, in process | held |
| 3.5 the parent's bytes a turn | 60–140 B a forked shape, both tiers; the existing rows unchanged | three passes at the final head (`logs/table-final/summary.txt`), every row ok on both tiers; the forked shapes **−18 to 123 B a turn** (`fork-substitution` 57–75, `fork-subshell` 24–67, `fork-background-group` 62–93, `fork-background-subshell` 36–116, `fork-stage` 22–74, `script-fork-substitution` 52–89, `typed-fork-subshell` 123, `fork-redirected-subshell` −18 to 83), the pin's in-process answers on the same rows 3–128 but `fork-redirected-subshell` 668–699 (red), dash −11 to 41; of the rows that fork since sh20, `background-nowait` (`true &`), `script-background-wait` and `typed-background-wait` keep 28–31 B a turn more than at the pin by the medians (113–150, 90–122, 188 against 74–105, 40–78, 159–160: the prediction's child-table slot a child), the typed one at 188 of its bound's 205 B at N = 10,000; `background-builtin-wait` and `substitution-pipeline` move both ways by tier (−31 to +35), the rest as at the pin | held for the forked shapes (some below the floor); **missed** for three existing rows, inside the bound |
| 3.6 cost | 150–300 µs a forked shape, 1.5–2.5× dash's; sh19's target (no slower than dash) not met; the in-process shapes stay at 5–45 µs | `logs/bench/bench-pin0-3.txt` (9 runs, median, a turn of 2,000 with the loop counter; load 0.08 at the start): forked, release **148–166.5 µs, 1.33–2.06×** dash's 77.5–120.5, native **196.5–245.5 µs, 1.97–3.00×**; in process at the head, release 8–9 µs (the pin 5–8.5), native 19–33.5; a program 245.5 µs (the pin 243.5, dash 152.5); the census loops, release: `fork` 0.494 s (the pin 0.491, dash 0.311), `pipeline` 0.420 (0.418, 0.319), `param` 1.725 (1.663, 0.340), `configure-shaped` **0.481** (0.335, 0.325; `bench-pin0-3-configure.txt`) | held on release (148 at the floor); the ratio **missed** on native (up to 3.00); the target not met, as predicted |
| 3.7 checked lane | `exit(0)`, in-process bytes, trunk's order | `logs/probe/final/machines.txt`: `exit(0)`, `a b` where native says `b a`, `bg-pid: none`, the redirected subshells in process; lupin 0.1.55 refuses at resolve (`os_signal_default`, wolf-interp#269) | held |
| 3.8 PAX | the rows to replay; census: more `clone` without `CLONE_VM`, `setpgid`, `exit_group`, `pipe2`, no new name | `logs/census/{pin,head}/census.txt`: 50 names at the pin and at the head, **the same 50**; more `clone` (1,445 → 1,984), `exit_group` (1,014 → 1,512), `pipe2` (3,993 → 5,544), `wait4` (1,877 → 2,471), `rt_sigaction` (15,424 → 18,546), `getpid` (208 → 1,133), `setpgid` (16 → 19); a fork is `clone(child_stack=NULL, flags=CLONE_CHILD_CLEARTID\|CLONE_CHILD_SETTID\|SIGCHLD)`, the call pelt's spawn already made (`logs/census/fork-trace.txt`); under `strace` 44 rows fail at the head, the pin's 64 being those and the twenty fork rows (timing and `strace` in the process tree, as sh22's 43) | held |
| 3.9 pelt#47 | `wait` silent for a job a poll reaped | `wait/reaped_signal_quiet` red at the pin (kasumi and both plants), green at the head; `wait/waited_signal_said` green both | held |

## 4. Evidence index

- Container, launcher, gauntlets: `ctr.sh`, `launch.sh`, `gauntlet.sh`, `gauntlet-ctr.sh`, `gauntlet-rest.sh`, `quick.sh`, `snap.sh`, `after.sh` (the final table, census and probes, cpus 8–15), `probe/final-runs.sh` (the split and the bench).
- Base and pin: `logs/base.status` (trunk `3b0bab9`, 39 gates 0), `logs/pin.status` (`0eabfaf`, its rest after the pause), `logs/gauntlet/base-pin-summary.txt`.
- The heads: `logs/g251362c.status`, `logs/g0ca2ab2.status` and **`logs/final.status` (the final head `b05b0cf`, 41 gates 0, no SKIP)**; their counts `logs/gauntlet/heads-summary.txt`; digests `logs/digests.txt`. The commits after `b05b0cf` are prose only (`notes/`, `docs/`, `README.md`: `ci/tiers.py`'s PROSE, read by no gate).
- Probes beside dash: `logs/probe/childstate.{dash,bash}.txt`; `logs/probe/head/` (at `b448c1e`) and `logs/probe/final/` (at `b05b0cf`): `shapes.*`, `checked.*` (identical to dash on both tiers), `childstate.*` (§7's rows), `machines.txt`, `threads.txt`; `logs/probe/corners-9b04506.txt`; `logs/probe/notice*.txt`, `trapwait.*.txt` (dash, the pin, `b448c1e`, `9b04506`); `logs/probe/trunk/childstate.pelt-native-base.txt`.
- New rows red: `logs/notice/new-rows-*.log`, `logs/notice/sess-redir-stop-b448.log`, `logs/autocd/` (kasumi); the plant runs 39689838304 (`sh20-plant` `a458710`, at `61f9cf9`'s tests), 39708887619 (`sh20-plant2` `59db4cb`: `src/` at the pin, the rest at `b08e6bd`; `logs/plant/plant-59db4cb.txt`), and at the final head **39715917270** (`sh20-plant3` `348706e`: `src/` at the pin `fd5a890`, i.e. trunk `c10bad1`'s, the rest at `b05b0cf`; `logs/plant/plant-348706e.txt`: 20 corpus rows, 6 sessions, `fork-redirected-subshell` and the table checks red on both tiers) and **39715919419** (`sh20-plant4` `94ca885`: the head without `autocd_dir`'s `sh.sub > 0`; `plant-94ca885.txt`: `wolf test` and both tiers' table checks red). No branch `sh20-plant*` is to merge.
- Memory: `logs/table/` (pass 1 before the pause), `logs/table-0ca2ab2/` and `logs/table-final/` (three passes each, summed in `summary.txt`), `logs/rssgap/` (§3.11, §3.12).
- Cost: `logs/bench/bench-pin0-3.txt`, `bench-pin0-3-configure.txt` (`configure-shaped.sh` written by `probe/bench/gen-configure-shaped`, sha256 `4f1f4096…`). Syscalls: `logs/census/`. Real scripts: `logs/zgrep/zgrep.txt`.

**The shas across the two rebases.** The note's §1–§3.9 and the evidence name the commits as they were made, on trunk `3b0bab9`; the branch holds them rebased onto `c10bad1`. The binaries measured were built from the first column's trees.

| on `3b0bab9` | on `2dc8dbe` | on `c10bad1` (the branch) | commit |
|---|---|---|---|
| `65734ae` | `900c8f2` | `e3ded99` | the lane's container, launcher and gauntlet |
| `59e06cd` | `9b1e5da` | `c2f0622` | inputs and the prediction |
| `0eabfaf` | `b91156a` | `fd5a890` | the eighth pin |
| `8060f41` | `be44f4f` | `9a3c39f` | sh.state |
| `33fd0c0` | `ad6ff61` | `662d01a` | `$$` read at start |
| `0b6d0e2` | `81807b6` | `e6dab63` | sh.fork, the door |
| `90b875a` | `510c0c6` | `b19d817` | sig_apply |
| `2d477d2` | `d433b1f` | `7cb7d5c` | sh.jobs |
| `d275650` | `9019854` | `75b3c29` | `( list )`, `$( list )` fork |
| `f39dfa0` | `4c1e5c3` | `6ca54a2` | stages and `&` lists fork |
| `1612b2d` | `3efdd44` | `ab851a0` | the last command takes the child's place |
| `f0c7ff9` | `41185b5` | `a6943b0` | sh.selftest |
| `389ad24` | `92eb41c` | `7793a37` | the hook in a subshell |
| `556b321` | `b54ff34` | `bea3d4a` | the nine rows leave pending |
| `157d3e7` | `ee02351` | `a712ad6` | `c_jc_mixed_pipeline` |
| `924fac7` | `08c4b27` | `90f78ba` | five corpus rows |
| `bb83b6d` | `0879506` | `086e2aa` | three sessions |
| `f17ce72` | `0178ca4` | `88f2ec2` | census |
| `c623bc4` | `9b20c46` | `6f71c40` | shape-rss's fork rows |
| `f9bbfc1` | `73aaa1a` | `7273966` | ci, the table checks |
| `9e2265c` | `01dfc85` | `57ea509` | pelt#47 |
| `61f9cf9` | `9d93fdb` | `71af117` | #47's rows |
| `4cac139` | `5985655` | — | README (empty at the second rebase) |
| `8b8d470` | `f5cc80d` | `14918d2` | check-test, ci |
| `b448c1e` | `4b5bd50` | `2f0f3af` | selfcheck in its own program |
| `e9e3506` | `40d386b` | `e4aeb6a` | evidence |
| `b626c83` | `4a9507e` | `f495c46` | evidence (the pause's head) |
| `9b04506` | `499c77b` | `b4bca4a` | a redirected subshell's process |
| `87c54f6` | `a6d912f` | `5c5c2f5` | its corpus rows |
| `ab1890f` | `0487700` | `9e96e53` | its session |
| `251362c` | `d21c58a` | `d3a530c` | evidence |
| `0c50ef0` | `2f66060` | `a167c84` | census |
| `b08e6bd` | `6471c90` | `b752aa9` | shape-rss's redirected row |
| `e39a70e` | `92af41c` | `6578b54` | sh.fork's doc |
| `0ca2ab2` | `ad48515` | `855f27e` | evidence |
| `fd20549` | `0afbbcf` | `5821c03` | evidence |
| — | `945330a` | `866c2a6` | autocd refused in a subshell (R-sh23-4) |
| — | `5698cfe` | `54d5c6b` | sh.selftest, autocd |
| — | `21e7eff` | `bf5bac6` | `autocd_subshell` |
| — | `904e7b9` | `c9185d1` | census ed/26 |
| — | `e87118a` | `9e24844` | docs/CHANGELOG.md |
| — | — | `b05b0cf` | README at the head (the final gauntlet's head) |

## 5. Done-when

- [x] the eighth pin, its own commit (`fd5a890`, measured as `0eabfaf`); corpus and sessions counted against the seventh pin's (§3.15)
- [x] the fork for the five shapes, #34's rows in the corpus and sessions, dash-identical on kasumi; a redirected subshell's process (§3.10)
- [x] the checked lane's in-process rows (`logs/probe/final/machines.txt`)
- [x] `shape-rss` green on both tiers (every head gauntlet and CI), three passes of the table at the final head (§3.15, 3.5)
- [x] the PAX list (§6)
- [x] pelt#47, its own commit and rows
- [x] the change record in `docs/CHANGELOG.md` under `## Unreleased`; the README true at the head
- [x] every new row red before green: kasumi (the pin, `b448c1e`, trunk `2dc8dbe`) and the plants 39715917270, 39715919419
- [ ] PR: five sections, shas as bullets, a test checklist, `Footprint: cross-cutting`; `tier pr` green at the final head; `full-matrix` at that head; lane-audit; the `tier full` run id (the PR body records them)

## 6. PAX: what a pax lane (px58 or after) replays with the forking pelt

Nothing was measured on PAX. The static pelt (`tools/build --static`) at
the final head, and:

- the corpus rows the fork moved or added: `builtin/c_s_dot_special_file`, `env/c_subshell_concurrent`, `env/subshell_is_process`, `exec/exec_replaces_subshell`, `jobs/subshell_jobs`, `pipe/c_concurrent_stages`, `pipe/c_shell_producer_ends`, `pipe/endless_producer`, `redir/c_s_cmdsub_fd_pipeline`, `redir/subshell_redir_fails_set_e`, `signal/subshell_signal`, `signal/c_subshell_trap_reset`, `signal/c_trap_ignore_pipe`, `signal/c_trap_cmdsub_shows_parent`, `signal/c_wait_interrupted_term`, `signal/trap_cmdsub_lone_exit`, `signal/subshell_end_said_outside`, `signal/subshell_end_devnull`, `signal/trap_after_redirected_subshell`, `wait/c_subshell`, `wait/reaped_signal_quiet`, `wait/waited_signal_said`;
- the sessions: `c_jc_mixed_pipeline`, `jc_subshell_stop`, `jc_subshell_redir_stop`, `jc_background_subshell`, `subshell_jobs`, `autocd_subshell`, `cnf_cd`, `cnf_contexts`, `cnf_redirect`;
- `tools/shape-rss`'s eight fork rows (`fork-substitution`, `fork-subshell`, `fork-background-group`, `fork-background-subshell`, `fork-stage`, `script-fork-substitution`, `typed-fork-subshell`, `fork-redirected-subshell`) and the rows that fork since sh20 (`true & wait`, `true &`, `x=$(echo a | cat)` in a loop, a script's and typed);
- `probe/shapes.sh`, `probe/childstate.sh`, `probe/corners.sh`, `probe/notice*.sh`, `probe/trapwait.sh`, each beside dash; `tools/self-check`;
- the system calls the fork uses, all of them names pelt already made before it (§3.15, 3.8): `clone` with `CLONE_CHILD_CLEARTID|CLONE_CHILD_SETTID|SIGCHLD` and no stack from the shell's main thread (the fork, as px17 serves it), `setpgid` from the child on itself, `pipe2` (the child's one-byte word to the parent, and its hub), `rt_sigaction` in the child before its body (the trap resets), `wait4` on the forked pid, `exit_group` from the child; and a forked child is one thread where the shell is two, its signal thread being the second (`logs/probe/final/threads.txt`).

## 7. Findings (texts for the orchestrator to file; none filed)

1. **pelt: a simple command's own redirection and the notice of its end.** `sh -c 'kill -TERM $$' 2>f`: dash says `Terminated` inside `f`, pelt says it on its own standard error. Not the fork's: trunk `3b0bab9` and the pin answer the same (`logs/probe/notice.pelt-native-pin.txt` row 07, `notice.pelt-*-9b04506.txt` row 07). (The `( … ) 2>/dev/null` notice the pause named is fixed, §3.10.)
2. **pelt: a compound command with a redirection keeps 644–721 B a turn** (`{ true; } >/dev/null`, `if … fi >/dev/null`, `while … done >/dev/null` in a loop: 11.6 → 18.3 MB native over 10,000 → 20,000 turns; dash nothing), at trunk, the pin and the head, both tiers (§3.12, `logs/rssgap/compound-*.txt`). No `shape-rss` row covers it.
3. **pelt: an interactive shell keeps a job `wait` answered, its number and its `Done` notice, until the next prompt**; dash tells it right after the `wait` and frees the number. Typed `. ./childstate.sh` at `-i -m`: dash `[1] + Done` after each `… & wait`, pelt `[4]` and `[3]` together at the end (`logs/probe/final/childstate.*.txt`, typed section); at trunk too (`logs/probe/trunk/childstate.pelt-native-base.txt`: `[3] - Done`).
4. **pelt: a job's text keeps an assignment-only command that dash's leaves out.** `( p=$(…); show …; : ) &` is `(p=$(...); show …; :)` in pelt's `Done` line, `(; show …; :)` in dash's (`logs/probe/final/childstate.*.txt`, lines 20 and 22). dash's text is the odd one; whether pelt copies it is a ruling.
5. **pelt: a forked shape costs 1.3–3.0× dash's** (148–166.5 µs release, 196.5–245.5 native, against dash's 77.5–120.5; §3.15, 3.6), and the configure-shaped loop went from 1.03× to 1.48× dash's with the fork (its multi-command substitutions fork now). sh19's target (no slower than dash) is not met; a later lane's, if wanted.
6. Recorded, not issues: a pipeline whose first stage is a pure built-in pelt feeds has its first forked stage lead the job's group where dash's forked built-in leads (`stage-last: leads-own` against dash's `other-group`); nothing a job does differs. An interactive pelt catches QUIT and TERM where dash ignores them (`SigIgn` `0x280000` against `0x284004`, typed section), at trunk too; every child's mask is dash's. `tools/script-census` is owed a run after the fork (§3.14).

To close on the merge: pelt#34, pelt#47. To comment: pelt#17 (`$(trap)` keeps the shell's traps, `signal/c_trap_cmdsub_shows_parent`; its other items stay open).

## 8. Not verified, and inferred

- PAX: nothing run there (§6).
- macOS: no local run (no build on nomad-1); CI's `tier full` runs the macOS native leg.
- `busy` from a real task: pelt starts none; the row parks a task in `src/selfcheck.lu`'s own program.
- What makes a file's mapping count more or less of `RssFile` (§3.11): measured, not explained further than "the file's page-cache history"; the anonymous memory is the bound.
- The real-script census after the fork (§3.14): kasumi's own copies of the three scripts only.
- The bench ran alone on cpus 0–3 (load 0.08 at its start, 1.08 at its end, other lanes' jobs on other cpus); sh19's numbers were taken at load 7.7, so its dash column (100–156 µs) is not this one's (77.5–120.5).
