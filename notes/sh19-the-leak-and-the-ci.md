# sh19 — the leak, the skipped sessions, and what re-exec would take (pelt#33, #35, #34)

Contract: `sprints/pelt/19-the-leak-and-the-ci/sh19-the-leak-and-the-ci.md`
in the planning repo, authored at `b860faa` and corrected at `1f16faa`
(the orchestrator, 2026-10-19: ruling #69 R1 was made on 2026-10-11,
option B, so #34 is the implementation note for B, not a fork-or-not
recommendation). This file is the lane's record: §1 to §3 are committed
before the first change under `src/`, `tools/`, `tests/` or
`.github/`; the rest is filled in as the work lands.

## 1. Forbidden

As the contract, which takes s243's rules word for word with this
lane's toolchains. No shell's source is read or searched for (dash,
bash, busybox, mksh, zsh or any other), nor a libc's or a kernel's
other than PAX's own tree. Behaviour comes from POSIX.1-2024 (XCU
2.9.3.1 "Asynchronous Lists", 2.12 "Shell Execution Environment", the
`wait` and `jobs` pages), the shells' manuals as documentation, wolf's
spec at `v0.2.32`, and black-box runs of dash 0.5.13.4 and bash 5.3.20
**only inside throwaway `--network none` containers**
(`notes/sh19-evidence/refrun.sh`, kasumi's `/usr` read-only). No
assertion deleted or weakened; no timeout or retry as a fix. Signals
only to processes a test started. The toolchain from the release
archives by digest, each read twice. No build on nomad-1: kasumi under
`~/lanes/sh19/`, detached jobs by `setsid` with the pid recorded
(`notes/sh19-evidence/launch.sh`) and stopped by that pid only. No
merge, no tag, no issue filed or closed, no package installed, no other
lane's CI run cancelled, nothing under `~/.claude`, no attribution
trailers. Strict evidence (#571). #34 is a note: nothing of ruling #69
R1 B is implemented. If the harness refuses an action, the lane stops
and reports.

## 2. Inputs, verified (2026-10-19, before any change)

| input | contract says | measured | drift |
|---|---|---|---|
| pelt trunk | `cc2fdc9` | `origin/trunk` = `cc2fdc9e0f39…` (sh18's notes); branch `sh19` cut from it in its own worktree; kasumi clone at the same commit | none |
| wolf 0.2.32 | `v0.2.32` at `72de141f` | tag object `d21c4b28…` → `72de141f6246…`, read twice (`logs/tags.txt`); release 416327027; `wolf 0.2.32 (wolfgang, pin 72de141)` | none |
| lupin 0.1.54 | `v0.1.54` at `0e536e8` | tag object `9c98d445…` → `0e536e8fb451…`, read twice; release 415937354 | none |
| the digests | by digest, read twice | release API read twice (`logs/digests.txt`), equal to `wolf-toolchain.toml` for all six archives; `tools/fetch-toolchain` on kasumi hashed the linux x86-64 pair OK (`logs/base-fetch.log`) | none |
| wolf-std | `d37c911` | `d37c911f12206c4bf5c8d3281a649bf31da3beef` (API), the archive's `STD-REV` the same | none |
| pelt#33 | `cmd & wait` keeps ~1,809 B a turn | open; measured at trunk below: `env true & wait` **1,782 B a turn native, 1,844 release** | none |
| pelt#35 | sessions skipped after a red corpus | open; `.github/workflows/ci.yml` at trunk: the two session steps and the two self-tests read `if: matrix.builds`, every other post-build step `if: ${{ matrix.builds && !cancelled() }}` | none |
| pelt#34 | in-process stages are not jobs | open | — |
| ruling #69 R1 | "R1 fork open" (inputs line) | `wave-53.md` 2026-10-11 and `sprints/pelt/index.md`: **R1 B**, pelt re-executes itself for a subshell; a wolf fork only if it can be sound with the runtime's threads | **the contract's inputs line is stale**; its body was corrected at `1f16faa` |
| px17 | `clone3 CLONE_VM\|CLONE_VFORK` is spawn, not fork | pax `notes/px17-the-pipes.md` §3, P1: px17's own prediction of a vfork-like spawn was **falsified**: wolf's spawn **forks** (`clone(…, SIGCHLD)` without `CLONE_VM`, then a socketpair handshake), so PAX gained `fork` (an address-space copy, `paging.copy_user`) at px17; sh18's syscall census shows the same split at 0.2.32 (`clone` 1,252 = spawns, `clone3` 1,261 = threads) | the contract's reading of px17 is reversed; #34's note measures it again |
| the contract's #34 | a fork-or-not note (`b860faa`) | re-worded at `1f16faa` (R1 B made: a re-exec implementation note) and at `a85d0e8` (ruling #90: wolf gets `os_fork`, s247, 0.2.34; a fork-adoption note for sh20) | **two re-scopes mid-lane**, §3.5 |
| kasumi | `/home` ~27 GB | 24 GB free at the start; load 0.00 | — |

### 2.1 What is kept, measured (trunk `cc2fdc9`, kasumi)

**By `shape-rss`'s own method** (`probe/bgshapes.py` imports
`tools/shape-rss`'s `run_file`/`run_typed`: peak RSS at 10,000 and
20,000 turns, the answer checked), pelt's two tiers against dash
(`logs/base-bgshapes.log`, `logs/dash-bgshapes.log`), bytes a turn:

| shape | native | release | dash |
|---|---|---|---|
| `wait` (no job: the control) | **661** | **609** | 3 |
| `env true` (a program, the control) | 38 | 52 | −9 |
| `true & wait` | 1,199 | 1,226 | 9 |
| **`env true & wait`** (pelt#33) | **1,782** | **1,844** | 5 |
| `env true & wait $!` | 2,168 | 2,267 | 16 |
| `( true ) & wait` | 640 | 631 | −2 |
| `{ true; } & wait` | 660 | 638 | −15 |
| `true &` (no wait) | 747 | 751 | 13 |
| `env true &` (no wait) | 1,497 | 1,509 | 3 |
| script of N lines `env true & wait` | 1,844 | 1,810 | −3 |
| script of N lines `true & wait` | 1,185 | 1,184 | 1 |
| typed `env true & wait` | 2,301 | 2,301 | 0 |
| typed `true & wait` | 1,682 | 1,682 | 0 |

So `wait` alone keeps ~640 B a turn, `( … ) &` and `{ …; } &` keep
nothing of their own beyond it, and a simple command after `&` keeps
~550 B (a built-in) or ~1,150 B (a program) more.

**pelt exposes no allocator counts** (no builtin reads a region's
ledger in `src/`). The allocator's own count is the root arena's chunk
grabs: the process root is a bump arena over 64 KiB chunks, never
freed (sh08 §3.1), so after warm-up every `malloc` of 64 KiB or more is
the root growing. `probe/heapprof.py` (sh08's, unchanged) breaks on
those under gdb and records the pelt frames (`probe/profbg.sh`, 3,000
turns, native; `logs/prof-base/`):

| shape | chunk grabs after 20 | where (innermost four frames) |
|---|---|---|
| `wait` | 9 | 100% `[list_new] < args_of < builtin < run_fields` (via `run_slow`) |
| `true &` | 12 | 50% `[list_new] < run_fields < run_slow < run_simple`, 25% `[list_push] < enc_fields < run_slow`, 17% `args_of < builtin`, 8% `[list_push] < jb_new < run_async` |
| `env true &` | 64 | 42% `[strbuf_finish] < find_in < find_in_path < hash_find`, 39% `[list_new] < start_child < run_external < run_fields`, 16% `[fs_stat_record] < stat_of < find_in`, 2% `jb_new`, 2% `jb_add_proc` |
| `true & wait` | 36 | `run_fields`' lists 42%, `enc_fields` 19%, `redirs_of` 19%, `[str_repeat] < run_simple` 19% |
| `env true & wait $!` | 98 | `run_fields` 20%, `find_in` (stat 19%, path strings 16%), `enc_fields` 16%, `args_of` 9%, `start_child` 8%, **`jb_new` 3%, `jb_add_proc` 2%** |
| `( true ) & wait` | 10 | `run_fields` 40%, `args_of` 30%, `enc_fields` 30% |

**What one list costs in the root** (`witness/listcost/main.lu`, wolf
0.2.32, `logs/listcost.txt`): an empty `List[str]()` **46 B**, a list
with one `push` **176 B**, the same on both tiers.

**The other built-ins keep the same** (`logs/base-builtins.log`,
release, bytes a turn; dash 0–22 for every row, `logs/dash-builtins.log`):
`export X` 648, `jobs` 647, `unset y` 653, `set -- a` 667, `kill -0
$$` 748, `umask 022` 800, `command true` 888, `cd .` 1,252, `eval :`
1,320, `read x </dev/null` 1,675.

**What the references keep of a job** (`probe/scripts/w01`–`w09`, dash
and bash in the container, trunk pelt on the host; `refs/`): all three
keep every job nobody waited for (5,000 `true &` then `jobs`: 5,000
`Done` lines each, w09), and a pid whose `$!` was expanded (w02, w06).
After `wait $p`, **dash forgets the job once another job starts**
(`wait $p` again: 3 with no job in between, w01; 127 after one, w08);
bash forgets it at once (127 both times); **pelt never forgets it** (3
both times, w08), so `cmd & wait $!` grows the table a slot a turn.
`wait` with no operand forgets the ended jobs in all three (w03, pelt
and bash 127 after it, dash 4: dash keeps a job `wait` reaped until the
next job starts here too). After `env true & wait`, `hash` lists
nothing in any of them (w04: the search was the subshell's).

## 3. Prediction (committed before the first change)

### 3.1 #33: the cause

What `cmd & wait` keeps is **not a job record, a group entry or a
notice: it is the ordinary path's scratch, in the root arena, twice a
turn**:

1. **`wait`, like every built-in but the pure, flow, `local` and
   `shift` ones, runs the ordinary path** (`run_fast` bails on it), and
   `run_fields` builds about nine lists per command in the root, most of
   them empty: `enc_fields`' fields (176 B), `names`, `values`, `had`,
   `old` (4 × 46), `redirs_of`'s (46), the regular built-in's own `old`
   and `had` (2 × 46), `builtin`'s `args_of` (46 or more), plus
   `pre_expand`'s copied-out text: ≈ 600 B, which is `wait`'s 609–661.
2. **The command after `&` never takes the fast path**: `run_simple`
   admits `nowait` only for a pipeline stage or a job's last stage, so a
   simple command `run_async` starts goes the ordinary way too; a
   program also builds `start_child`'s descriptor map and **searches
   `PATH` again every turn** (the in-process subshell's frame takes the
   hash entry back, as it must: w04), keeping each candidate path and
   its stat record in the root.
3. **`wait $!` never frees the job** with job control off, so the table
   grows a slot (8 + 5 list pushes) a turn, where dash forgets it when
   the next job starts (w08).

### 3.2 #33: the fix (each its own commit)

- **A lean ordinary path for a built-in.** A built-in with no
  assignment and no redirection (`exec` aside), with `-x` off, runs from
  `pre_expand`'s text with no list built but its arguments, and those
  in a list taken from a pool in the state and given back (cleared, its
  capacity kept), so a turn builds nothing; the redirection frame is
  opened and closed as before. `builtin` gains `builtin_args(name,
  args)`; every other caller is unchanged.
- **`cmd &` on the fast path.** `run_async` marks its simple command,
  and `run_simple` lets the fast path start it not waited for, as it
  starts a pipeline stage (`R_STAGE`, joined to the job by `jb_join`);
  the fast path writes no `H` (hash) op for it, since the subshell's
  frame would take the entry back at once.
- **A waited job is forgotten when the next one starts** (job control
  off, dash, w01/w08): `wait pid` marks the ended job, `jb_new` frees
  the marked ones first. Two corpus cases recorded from dash in the
  container (w01's and w08's shapes).

### 3.3 #33: the numbers

| shape | trunk (release) | predicted at the head (both tiers) |
|---|---|---|
| `env true & wait` | 1,844 B a turn | **under shape-rss's bound** (2,000 KB over 10,000 turns, ≈ 200 B a turn): ≤ 100 B a turn |
| `true & wait` | 1,226 | ≤ 100 |
| `env true & wait $!` | 2,267 | ≤ 100 |
| `wait` | 609 | ≤ 50 |
| the same as a script of N lines | 1,810 / 1,184 | ≤ 100 |
| typed `env true & wait`, `true & wait` (job control on) | 2,301 / 1,682 | **still over the bound** at the first step: each job's text (`node_text`, `jb_fill_text`'s stage list) and its notice line (`job_line`) are built in the root, ≈ 300 B a job. A second step builds the text in `copy region` (only the final string kept) and the notice line in a region; predicted then ≤ 150 B a turn, under the bound |
| `export X`, `jobs`, `unset y`, `kill -0 $$`, `umask 022` | 648–800 | ≤ 100 (nothing kept but their bytes) |
| `set -- a`, `cd .`, `eval :`, `command true`, `read x </dev/null` | 667–1,675 | **still over** (each keeps what it builds: a new `$@`, the `PWD` strings, `eval`'s parse, `command`'s own field list; `read` has a redirection, so it is not on the lean path); reported, not gated |
| corpus, sessions | 956/0/38, 264/0/3 | (958 + 0)/0/38 (two new cases pass), 264/0/3, both tiers |
| every other gate | 0 | 0 (`shape-rss`'s 24 rows unchanged within noise) |

New `shape-rss` rows, by name: `background-wait` (`env true & wait`,
the issue's shape), `background-builtin-wait` (`true & wait`),
`background-wait-pid` (`env true & wait $!`), `script-background-wait`,
`builtin-wait` (`wait`), and the typed pair once the second step lands.
**Red before green:** the new rows on trunk's binaries fail at the
numbers above; in CI, a plant (`sh19-plant`) of the head with the three
`src/` fixes reverted is red on exactly the new rows (and the corpus's
two new cases) on linux x86-64 and macOS arm64.

### 3.4 #35

The two session steps and the two harness self-tests take `if: ${{
matrix.builds && !cancelled() }}`, as every other step after the build
already does; a red corpus still fails the job (its own step is red),
and the sessions now report on their own. **Plant:** a branch
`sh19-plant-double` whose one `src/` change breaks something both
corpora see (`jobs`' state word), dispatched once on the CI change:
predicted the corpus steps red **and** the session steps run and red in
the same run, on linux x86-64 and macOS; on trunk's workflow the same
plant would skip the sessions (sh18's run 39160267977 is that control,
already recorded).

### 3.5 #34 (a note; nothing implemented)

**Re-scoped twice on 2026-10-19 by the orchestrator, both after §1–§3
were first committed (`9556d3c`):** at `1f16faa` to an implementation
note for ruling #69 R1 B (re-execute), then at `a85d0e8` by **ruling
#90** (the maintainer: wolf gets a real `os_fork`, lane s247, in
0.2.34) to **pelt's fork-adoption note for sh20**. The re-exec
prediction this section held is withdrawn unmeasured; nothing of it was
measured or written. This is the prediction for the note as it now
stands, committed before any #34 measurement:

- **Each in-process shape today**, linux on kasumi and macOS arm64 by
  one dispatched diagnostic run on a branch never to merge: `( … )`
  runs in pelt's process (a program started inside it has `$$` as its
  parent, where dash's has the subshell's pid); `( … ) &` and `{ …; } &`
  run to their end before the next command (`( sleep 0.3; echo a ) &
  echo b` prints `a` before `b`, dash the reverse) and their `$!` is a
  number no process has; `$( … )` is in-process with its output
  captured; a pipeline stage pelt runs itself (a built-in, a compound
  command, a function) runs to its end before the next stage starts,
  so an endless in-process producer (`while :; do echo y; done | head
  -n 1`) never ends; the same on both hosts.
- **What the forked child must do first**, from XCU 2.11 and 2.12 and
  the `trap` page, per shape; and **what pelt state must be sane in
  it**, measured on a running pelt: its threads (`/proc/PID/task`:
  predicted 2 from `main`, the signal hub's drain thread being the
  second, s243), its descriptors (`/proc/PID/fd`: predicted 0–2, the
  hub's pipe pair and, interactive, the terminal and the history file),
  its signal dispositions (`SigCgt`/`SigIgn`/`SigBlk`).
- **dash's cost per shape** on sh06's census loops (`tools/bench`) and
  one loop per shape, on kasumi under `taskset -c 0-3`, beside pelt
  today: predicted dash 100–400 µs a forked shape (`( : )`, `x=$( : )`,
  `( : ) &` + `wait`, a stage it runs itself), pelt's in-process shapes
  3–30 µs, so the in-process pelt is faster than dash on every
  subshell-heavy loop and sh20's fork must not be slower than dash's.
- **What fork clears**: the nine `pending=fork` corpus rows
  (`tests/diff/PENDING.md`'s fork rows), `session:c_jc_mixed_pipeline`
  and statements 2.11/18 and wait/7 (`tests/census/clauses.tsv`'s
  `pending (fork)` rows), plus the recorded differences of §2.1 that are
  the subshell's (`c_wait_interrupted_term`'s order).

### 3.6 A static pelt for PAX

pax trunk's `tools/mkpelt` in a throwaway Ubuntu 24.04 container on
kasumi with `ld.lld`, as sh18; its sha256 in the report; trunk
`cc2fdc9` rebuilt the same way must give sh18's `76f3fc40…`; the
system-call set unchanged (the fixes call nothing new).
