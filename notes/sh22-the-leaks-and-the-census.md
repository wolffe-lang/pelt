# sh22 — the leaks and the census (pelt#39, #41, #27)

Contract: `sprints/pelt/22-the-leaks-and-the-census/sh22-the-leaks-and-the-census.md`
in the planning repo, at trunk `560c78f`. This file is the lane's record:
§1 to §3 are committed before the first change under `src/`, `tools/`,
`tests/` or `.github/`; the rest is filled in as the work lands.

## 1. Forbidden

As the contract and `sprints/RULES.md` say. No shell's source is read or
searched for (dash, bash, busybox, mksh, zsh or any other), nor a libc's
or a kernel's. Behaviour comes from POSIX.1-2024 (XCU 2.9.3.1
"Asynchronous AND-OR Lists", 2.11 "Job Control", 2.13 "Shell Execution
Environment", the `set`, `jobs`, `wait`, `read`, `eval`, `cd`, `command`
and `umask` pages), dash's manual (`set -m`, job notices) as
documentation, wolf's spec at the pin (`spec/02-memory-model.md`
`[mem.region.copyout]`, `spec/11-os.md` `[os.proc.poll]`), and black-box
runs of dash 0.5.13.4 and bash 5.3.20. No change to the hook (sh21) or
to command search. No assertion deleted or weakened; no timeout or retry
as a fix. The toolchain from the release archives by digest, each read
twice; pelt's pin stays. No build on nomad-1: kasumi under
`~/lanes/sh22/`, detached jobs by `setsid -f` with the pid recorded
(`notes/sh22-evidence/launch.sh`) and stopped by that pid only. **Every
run that starts, signals, times out or kills a process runs inside this
lane's own container** (`notes/sh22-evidence/ctr.sh`: rootless podman,
its own pid namespace with an init, `--network none`, a pids limit,
kasumi's `/usr` read only), never on kasumi's host process table
(RULES §5): the corpus, the sessions, the witnesses, `shape-rss`, the
census, the probes, the references. Only the compiles run on the host.
No merge, no tag, no issue filed or closed, no package installed on a
host, no other lane's CI run cancelled, nothing under `~/.claude`, no
attribution trailers. If the harness refuses an action, the lane stops
and reports.

## 2. Inputs, verified (2026-10-20, before any change)

| input | contract says | measured | drift |
|---|---|---|---|
| pelt trunk | `90d7c64` | `origin/trunk` = `90d7c649b171…` (sh21's notes); branch `sh22` cut from it in its own worktree; kasumi clone at the same commit | none |
| pelt's pin | stays | `wolf-toolchain.toml`: wolf 0.2.32 `v0.2.32` → tag object `d21c4b28…` → `72de141f6246…`; lupin 0.1.54 `v0.1.54` → `9c98d445…` → `0e536e8fb451…`; std `d37c911`; each tag read twice through the API; the release API's digests (releases 416327027, 415937354) read twice, equal to the file for all six archives (`logs/tags.txt`); `tools/fetch-toolchain` on kasumi hashed the linux x86-64 pair OK (`gauntlet/base-fetch.log`) | none |
| the crawl's toolchain | wolf 0.2.33 `v0.2.33` at `85dab5d7`, lupin 0.1.54, std `cceda63` | `v0.2.33` → `56110e4f…` → `85dab5d7e597…`, read twice (`logs/tags.txt`); pelt is not built with it: "pelt's pin stays" (the 0.2.34 pin is sh20's), as sh21 read the same line | reported: pelt builds at 0.2.32 |
| `src/sh/builtins/` | the built-ins | no such directory: the built-ins are `src/sh/builtin.lu` (and `umask.lu`, `kill.lu`); the ordinary path is `src/sh/exec.lu`'s `run_slow`/`run_fields`, the job table `src/sh/jobs.lu` and `src/sh/state.lu` | the path; nothing else |
| pelt#39 | five built-ins and the job slot | open; measured below | the numbers re-taken |
| pelt#41 | measure dash, then decide | open; dash measured below | — |
| pelt#27 | the census leaves a shell behind | open; seen at trunk below | — |
| kasumi | `/home` ~43 GB | 42 GB free at the start; load 2.2; podman 5, `archlinux:base-devel` present | — |

The counts at trunk (kasumi, both tiers, in the container): the
baseline gauntlet's `logs/base.status` (filled in §4).

### 2.1 What is kept at trunk, measured

**By `shape-rss`'s own method** (`probe/shapes22.py` imports
`tools/shape-rss`'s `run_file`: peak RSS from `/usr/bin/time` at 10,000
and 20,000 turns of a `while` loop, the answer checked), inside the
container, bytes a turn (`logs/base-shapes.log`; the job rows again with
a pids limit of 65,536, `logs/base-shapes-bg.log`):

| shape | native | release | dash |
|---|---|---|---|
| `:` (the bare loop, the floor) | 35–63 | 38 | 11 |
| `wait` (sh19's, the control) | 7 | 70 | 0 |
| **`read x </dev/null`** | **1,700** | **1,675** | −13 |
| **`eval :`** | **710** | **742** | 2 |
| **`cd .`** | **579** | **543** | 0 |
| **`command true`** | **172** | **147** | 1 |
| **`umask 022`** | **135** | **131** | −11 |
| `read x <<E` (a here-document) | 1,913 | 1,854 | −1 |
| `eval 'y=1'` | 717 | 692 | −3 |
| `cd /` | 236 | 210 | −20 |
| `command -v true >/dev/null` | 1,533 | 1,524 | 4 |
| `umask >/dev/null` | 1,426 | 1,411 | −6 |
| `jobs` | 111 | 115 | 5 |
| `true >/dev/null` (the fast path's redirection) | 61 | 42 | 4 |
| **`true &`** (no `wait`) | **176–206** | **217–218** | 36–39 |
| **`env true &`** (no `wait`; pids limit 65,536) | **369** | **353** | 7 |
| `true &` as a script of N lines | 135–165 | 165–181 | 26 |

The runs are noisy by some tens of bytes a turn (the same `wait` row
read 7 and 70); sh19's three passes read the same spread. Every row but
the controls is the ordinary path or the job table.

**Where the root grows** (`probe/heapprof.py`, sh08's, under gdb in the
container: the process root is a bump arena over 64 KiB chunks never
freed, so after warm-up each chunk grab samples the allocations by
bytes; `probe/prof22.sh` 3,000 turns, `probe/prof22b.sh` 20,000;
`logs/prof-base/`, `logs/prof-base-b/`; native):

| shape | innermost frames of the chunk grabs |
|---|---|
| `read x </dev/null` | `[list_slice] < bi_read` 33% (`args[i..]` copies), `[list_push] < redirs_of < run_fields` 33%, `[list_new] < run_fields` 33%: a redirection sends a built-in down the full ordinary path (sh19's lean path takes only a built-in with no redirection), nine lists again |
| `umask >/dev/null` | `[list_new] < enc_fields < run_slow` 100%: the same path |
| `eval :` | `[list_new] < new_parser < eval_from < eval_string` 100%: a fresh parser per `eval` (thirteen lists; the top level keeps one parser, pelt#19, `eval` does not) |
| `cd .` | `[strbuf_finish] < bi_cd` 100%: `canon`'s buffer and text, the joined path, `os_cwd()`'s answer and both values set again, every turn, in the root |
| `command true` | `[list_slice] < bi_command` and `[list_new] < args_of < builtin < bi_command`, a third each (the remaining third is the loop's own `[str_repeat] < run_simple`) |
| `umask 022` | `[str_chars] < mask_from < bi_umask` 100%: `for c in s.chars()` materializes a `List[char]` (the wolf guide's own warning) |
| `true &` | `[list_push] < jb_new < run_async` 56% (the loop's own the rest) |
| `env true &` | `[list_push] < jb_new` 38%, `[list_push] < jb_add_proc < jb_join` 32% |
| `:` | `[str_repeat] < run_simple` 100%: the loop's own counter, the floor every row carries |

**What a job slot costs** (`witness/jobcost/main.lu`, pelt's wolf on
both tiers, peak RSS at 100,000 and 200,000 slots; `logs/jobcost.txt`):
a slot of one `List[int]` costs **17–19 B** (8 B an element, the rest
the abandoned buffers of doubling: `[mem.region.account.1]`'s "a grown
container's abandoned buffers stay charged"), a `List[bool]` 2 B, a
`List[str]` 36–38 B; the job table's nine parallel lists (six `int`,
three `bool`, one `str`) **137–138 B a slot**. A list cut from a
template and written by index (`tpl[0..512]`, the "chunk" row) costs the
same 18–19 B as one pushed: there is no cheaper way to grow a list in
the root, so a slot costs what its fields are. The process entry of a
program's job is five more parallel lists (four `int`, one `str`), ~109
B.

**The job a script never waits for** (black box, `probe/setm/rss.sh` at
5,000 and 10,000 jobs, pids limit 65,536, `logs/setm-rss-base.txt`):

| loop of | dash | pelt release |
|---|---|---|
| `true &` | **24 B a job** | **221** |
| `env true &` | **16** | **306** |
| `true &`, after `set -m` | 14 | 715 |
| `env true &`, after `set -m` | 16 | 812 |

dash keeps every one of those jobs too: `jobs` after 5,000 of either
lists 5,000 `Done` lines in dash and in pelt (sh19's w09, again here:
`probe/jobs/keep.sh`, `logs/keep-base-65536.txt`). And **pelt reaps no
job nobody waits for**: in the container with a pids limit of 4,096,
6,000 `env true &` in a loop made dash 6,000 jobs and pelt 1,910 times
"env: cannot be run" (`logs/keep-base-4096.txt`): its ended children
are never reaped before `wait`, so the kernel's process table fills with
them; dash reaps them as they end. `shape-rss`'s method run on `env
true &` at 20,000 turns there answers wrongly for that reason
(`logs/base-shapes.log`: 684,087 bytes on standard error).

### 2.2 pelt#41: dash's `set -m` in a script, black box

`probe/setm/m01`–`m08` under dash 0.5.13.4, `bash --posix` 5.3.20 and
pelt trunk, each without a terminal (standard input `/dev/null`,
standard error into the same pipe as standard output) and with one
(`probe/setm/ttyrun.py`: a fresh pseudo-terminal as the controlling
terminal), in the container (`probe/setm/run.sh`; every answer in
`refs/setm-base/`). bash `--posix` writes no notice in a script at all;
dash writes them; with and without a terminal dash answers the same.

| probe | dash | pelt trunk |
|---|---|---|
| m01: a loop starting a program job each turn, `sleep` between | **no notice until the loop (the complete command) ends**; then all three, newest first, before the next command | the same, byte for byte |
| m02: the same with `true &` | the same | **the notices come one complete command later**: after the command after the loop |
| m03: separate commands, a brace group, `cmd & sleep; echo` on one line | a notice after each complete command (after the group, not inside it; after the whole line) | the same |
| m04: `jobs` inside the loop | `jobs` lists the ended job (and so it is forgotten); nothing after the loop | the same |
| m05: 500 jobs in a loop | 500 notices after the loop; the table empty after | the same |
| m06: m01 without `set -m` | no notice | the same |
| m07: `wait $!` inside the loop | **the waited jobs are still told after the loop** | the same |
| m08: jobs in a function called twice | after each complete command that called it | the same |

So dash, like pelt, **keeps a slot for every job a `set -m` script's
loop starts until the loop ends**, and tells them then; it reaps the
processes as they end (the pids-limit run above). The difference is the
size of the slot (14–16 B a job against 715–812, §2.1) and m02's late
notice.

### 2.3 pelt#27: the census leaves a shell behind, seen at trunk

`probe/reap/leak.sh` in the container: a corpus of one case
(`PELT_DIFF_DIR`) whose shell starts `sleep 300 &` and then blocks
opening a FIFO nobody writes, so the case times out (10 s), run by
`tools/syscall-census --no-session` and then by `tools/difftest` alone;
after each, every process left in the container is listed
(`logs/reap-base.log`, `logs/left-census.txt`, `logs/left-difftest.txt`):

- **under the census, the shell and its child are left** (`pelt ../s.sh`,
  re-parented to the container's init, and `sleep 300`): the case's
  timeout ends the process `subprocess.run` started, which is `strace`
  (the wrapper `exec`s it), and a traced process whose tracer dies is
  let go, not ended;
- **under `difftest` alone the shell is ended but its child is left**
  (`sleep 300`): the timeout ends one process, never what it started;
- `tools/session`'s timeout ends the session's process group, which a
  shell with job control leaves for every job it starts, and which
  under the census holds `strace`, not the shell.

The probe then ended what it listed, by pid, inside the container.

## 3. Prediction (committed before the first change)

### 3.1 pelt#39: the five built-ins (each its own commit)

1. **A built-in with redirections, on the lean path.** sh19's lean
   ordinary path (`run_builtin_enc`) takes a built-in with no assignment
   and no redirection; it takes one with redirections too (no
   assignment, `-x` off, not `exec`): the redirections applied straight
   from the tree (no `redirs_of` list), in the frame `run_fields` would
   open, a special built-in's failed redirection still ending the shell
   as `special_redir_failed` says, a regular one's status 2. That is
   most of `read x </dev/null`, `umask >/dev/null` and `command -v …
   >/dev/null`.
2. **`read`** walks its operands in place (no `args[i..]` copy) and
   builds its line in a buffer the state keeps and clears.
3. **`eval`** takes its parser from a pool in the state (taken, reset,
   given back: an `eval` inside an `eval` takes another), and one
   operand is the text itself (`join_args` builds nothing for it).
4. **`cd`** computes the new path inside `copy region`; `PWD`,
   `OLDPWD` and the physical directory are set only when they change, so
   `cd .` keeps nothing.
5. **`command`** hands the utility's operands to the built-in in a
   pooled list (no slice, no `args_of`).
6. **`umask`** reads its operand by index, not through `chars()`.

| shape | trunk (native / release) | predicted at the head, both tiers |
|---|---|---|
| `read x </dev/null` | 1,700 / 1,675 | **≤ 100 B a turn** |
| `eval :` | 710 / 742 | **≤ 100** |
| `cd .` | 579 / 543 | **≤ 100** |
| `command true` | 172 / 147 | **≤ 100** |
| `umask 022` | 135 / 131 | **≤ 100** |
| `umask >/dev/null`, `command -v true >/dev/null` | 1,411–1,533 | ≤ 100 (by item 1) |
| `eval 'y=1'`, `cd /` | 210–717 | ≤ 100 |
| `read x <<E` | 1,854–1,913 | **still over** (the here-document's body is expanded and fed in the root; not this lane's shape, reported) |
| `jobs` | 111–115 | unchanged (reported) |

"≤ 100" is `shape-rss`'s own bound (100 B a turn + 1 MiB over 10,000
turns) and includes the loop's own 35–63 B: each built-in then keeps
nothing of its own but noise, dash's order (dash: 0–2 B on every row).

### 3.2 pelt#39: the job slot (each its own commit)

1. **Ended children are reaped when the next job starts** (a script,
   job control on or off): `jb_new` polls the children
   (`[os.proc.poll]`: one `waitpid` per live child) and writes what
   ended into the table, as the waits already do; how often it polls
   follows how many children were still live at the last poll, so a
   loop of jobs that never end costs O(1) polls a job, not O(n). The
   statuses are kept exactly as before (`wait $p`, `jobs`); an
   interactive shell is left as it is (its notices read the table after
   each line, `jc_take`).
2. **With job control off, a job whose one process has ended keeps its
   status in its slot and gives its process entry back**, so the process
   table holds the processes still live; `wait`, `jobs`, `kill` and `$!`
   answer as before.
3. **The slot is two `int`s.** The job table's nine parallel lists
   become two packed `List[int]` (state, status and the three flags in
   one; `$!`'s number and the use stamp in the other) behind accessor
   functions; the process group and the command text, which only job
   control writes, live in lists that grow only when it writes them.
   Every reader goes through the accessors; no behaviour changes.

| shape | trunk | predicted at the head |
|---|---|---|
| `true &` in a loop, by `shape-rss`'s method (no wait) | 176–206 / 217–218 B a turn | **≤ 100 B a turn**, both tiers |
| `env true &` in a loop (no wait) | 353–369 B a turn at a pids limit of 65,536; wrong at 4,096 (never reaped) | **≤ 100 B a turn**, answering right at a pids limit of 4,096 |
| a loop of 6,000 `env true &`, pids limit 4,096 (`probe/jobs/keep.sh`) | 1,910 "cannot be run" | **0** (as dash); `jobs` still lists 6,000 |
| `probe/setm/rss.sh` without `set -m`, `true &` / `env true &` | 221 / 306 B a job | **≤ 60 B a job** (dash 24 / 16) |
| the same after `set -m` (pelt#41's loop) | 715 / 812 B a job | lower by the table's share, still over (the job's text and its notice are job control's; reported with the number, §3.3) |

### 3.3 pelt#41: decided — match dash, and the number

dash keeps a `set -m` script's loop's jobs until the loop ends and tells
them then (§2.2); so does pelt. **pelt keeps dash's order of notices**
and fixes the one difference measured, m02: a job pelt runs itself
(`true &`) is told one complete command late because its slot is marked
`late` whenever job control is on, which only an interactive shell's
prompt needs; in a script it is told with the others. The slot it keeps
meanwhile is reported with its number (§3.2's last row, against dash's
14–16 B). Rows (corpus cases recorded from dash, `exec 2>&1` first so
the notices are standard output and compared byte for byte, each job
waited for with `wait $!` so no row depends on timing):
`jobsctl/c_monitor_loop_notices` (m07's shape, programs: told after the
loop, newest first), `jobsctl/c_monitor_loop_builtin` (m02's shape with
`wait $!`: **red at trunk**, green at the head),
`jobsctl/c_monitor_list_notices` (m03 and m08: after each complete
command, not inside a group or a function).

### 3.4 pelt#27: the census ends the tree it started

A module the harnesses share, `tools/lib_reap.py`: on linux the harness
process becomes a **child subreaper** (`prctl(PR_SET_CHILD_SUBREAPER)`)
so every process a case starts stays its descendant however its parents
end; on a timeout it reads the case's whole tree from `/proc` (every
descendant of the case's process, and every process re-parented to the
harness since the case began), **ends each by its recorded pid**
(`SIGKILL`), reaps them, and walks again until nothing is left;
elsewhere (macOS) the tree is read from `ps` before the first kill.
`tools/lib_cases.py`'s `run` (so `tools/difftest`, `tools/oracle-record`)
and `tools/lib_session.py`'s session (in place of its `killpg`) use it;
each says how many processes it ended (`timed out, ended N processes`),
and `tools/syscall-census` adds them up and says so (`N cases timed out
under strace; M processes ended, 0 left`). No timeout's length changes.

**The proving case, and its witness.** `tests/reap/` is a corpus of one
case that times out on purpose, `hang/c_tree.sh`: the shell writes its
own pid and those of a child and a grandchild (`sleep 300 &`, and a
shell that starts another `sleep 300 &` and waits), then blocks opening
a FIFO nobody writes. `tools/reap-witness BIN_DIR` runs it through
`tools/difftest` and, on linux where `strace` is, through
`tools/syscall-census`, and then asks for each recorded pid whether it
is still alive (and ends it if so): **ok only when the case timed out,
the harness said it ended them, and none is left.** Predicted: at
trunk's harness the witness is red on both rows (the census leaves the
shell and both sleeps, difftest the two sleeps: §2.3's shape); at the
head green on both tiers, on linux and (difftest's row) macOS in CI. CI
installs `strace` on the linux legs for it.

### 3.5 The numbers

| | at trunk | predicted at the head |
|---|---|---|
| corpus | 962/0/38 (sh21) | **(962 + 3)/0/38**: the three #41 rows, one of them red at trunk |
| sessions | 273/0/3 | **273/0/3** (no session moves: notices at the prompt are untouched) |
| statements | 505 of 547 | 505 of 547 (the rows are dash's behaviour, not new statements) |
| `shape-rss` | 33 rows, all ok | **+7 rows** (`builtin-read-redir`, `builtin-eval`, `builtin-cd`, `builtin-command`, `builtin-umask`, `background-nowait`, `background-program-nowait`), **each red at trunk, ok at the head**, both tiers |
| `tools/reap-witness` | — (new) | red at trunk's harness, ok at the head |
| every other gate | 0 | 0 |

**Plants (RULES §7, the PR's own `tier pr` run):** plant A, the head
with `src/` and the harnesses' reaping put back to trunk: red on exactly
the seven new `shape-rss` rows (both tiers), `jobsctl/c_monitor_loop_builtin`,
and both rows of `tools/reap-witness`. Plant B, the head with the job
slot's fold keeping no status (item 3.2.2 broken): red on the corpus
rows that read a folded job's status (`wait/c_unwaited_many_status`, a
new case: 300 jobs nobody waits for, then `wait $first` and `jobs |
wc -l`, recorded from dash), and nothing else.
