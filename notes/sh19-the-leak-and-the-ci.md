# sh19 — the leak, the skipped sessions, and what a fork must do (pelt#33, #35, #34)

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

### 3.7 pelt#37 (added by the orchestrator, 2026-10-19; prediction before the change)

The maintainer found on PAX that from a cwd of `/`, `cd bin; pwd`
prints `//bin`. Measured black-box (`probe/scripts/w12-cd-root.sh`,
dash and `bash --posix` in the container, this branch's pelt on the
host; `refs/w12-*`):

| from | operand | dash | bash | pelt now |
|---|---|---|---|---|
| `/` | `bin`, `./bin`, `bin/` | `/bin` | `/bin` | **`//bin`** |
| `/` | `//` | `//` | `//` | `//` |
| `/` | `//bin` | `//bin` | `//bin` | `//bin` |
| `//` | `bin` | `//bin` | `//bin` | **`/bin`** |
| `/`, `CDPATH=/` | `bin` | `//bin` | `/bin` | `//bin` (dash's) |
| `/usr/` | `bin` | `/usr/bin` | `/usr/bin` | `/usr/bin` |

The cause is `bi_cd`'s relative join `canon("{base}/{cur}")`: a base
ending in `/` gets a second one, so `/` + `bin` is `//bin`, which
`canon` keeps (a leading `//` is implementation-defined and kept, as
dash keeps it), and `//` + `bin` is `///bin`, which it folds to
`/bin`. **The fix:** the join adds the `/` only when the base does not
end in one; `canon` is unchanged, and so is the `CDPATH` join (pelt
already answers dash's `//bin` there). **Predicted:** three new corpus
cases recorded from dash: `cd/c_root_relative` (the first row) red at
this branch's head before the fix and green after; `cd/c_double_slash`
(`cd //`) green before and after; `cd/c_double_slash_path` (`cd //bin`,
and `bin` from `//`) red before (its last line) and green after. Corpus
958/0/38 → 961/0/38 on both tiers; nothing else moves; the static pelt's
digest moves (a `src/` change). Seen red: the cases pushed before the
fix, so the PR's own run at that head is red on exactly them.

### 3.8 The result against the prediction

Measured on kasumi by `notes/sh19-evidence/gauntlet.sh` (sh18's, its
paths moved; every gate's exit status in `logs/<tag>.status`): the
**#33/#35 head** `a7d3455` (`head`: all 37 gates 0) and the **#37 head**
`cd05c3b` (`head2`); trunk's own gauntlet is sh18's `head4` (`2676879`,
the same `src/`, `tools/` and `tests/` as trunk `cc2fdc9`: all gates
0); and in CI (§4).

| prediction | predicted | measured | held? |
|---|---|---|---|
| #33's cause | the ordinary path's scratch in the root, twice a turn; `wait $!`'s slot | as predicted, and confirmed by the fix: each of the three commits removes its share (`logs/bg-a-bgshapes.log`) | held |
| `env true & wait` | ≤ 100 B a turn, both tiers | 59, 88, 104 native; 76, 95, 105 release (three passes: `bg-a`, `bg-b`, the gauntlet, the trimmed rows) | under the gate's bound always (≈ 200 B at 10,000 turns); **≤ 100 not held in two of six** |
| `true & wait` | ≤ 100 | 43–91 | held |
| `env true & wait $!` | ≤ 100 | 51–103 | held but once (103) |
| `wait` | ≤ 50 | 42–91 (the bare loop `:` alone keeps 46) | **not held** |
| script of N lines | ≤ 100 | `env true & wait` 88–109, `true & wait` 20–74 | held but once (109) |
| typed, after step 1 | still over, ≈ 300 B a job | 560–588 B a turn | held in kind (over), larger than predicted |
| typed, after step 2 | ≤ 150 | `true & wait` 160, `env true & wait` 188 | **not held** (under the gate's bound) |
| `export`, `unset`, `kill -0`, `jobs`, `umask` | ≤ 100 | 42–73, 47, 37–65, 109, 151 | held for three; **`jobs` 109 and `umask` 151 over** |
| `set -- a`, `cd .`, `eval :`, `command true`, `read x </dev/null` | still over | 60, 575, 716, 189, 1,667 | held but **`set -- a` fell to 60** |
| corpus | (958 + 0)/0/38 | **958/0/38** both tiers and both under `taskset -c 0-3` (`head`) | held |
| sessions | 264/0/3 | **264/0/3** both tiers and under `taskset` | held |
| every other gate | 0 | 0, all 37 (`logs/head.status`) | held |
| the plant | red on exactly the new rows and the corpus's new case; sessions run and red after a red corpus | CI **39308407198** (`sh19-plant` `e6dafed`: the four `src/` fixes reverted, a running job's word `Going`): `shape-rss` red on exactly the nine sh19 rows, both tiers, linux and macOS; corpus red on exactly `wait/c_pid_forgotten`, both tiers, both hosts; **the session steps ran after the red corpus** and were red on exactly six `c_jc_*` sessions (native both hosts, release linux; macOS's release session step was cut by the job's 45-minute limit); **not predicted: `wolf test` red too** (its job-line table check reads `Running`) | held, with one more red than predicted |
| #37 | three cases, two red then green, 961/0/38 | red on exactly `cd/c_root_relative` and `cd/c_double_slash_path` at `50d9354`, on kasumi and in the PR's run **39318541896** (linux job: 959/2/38 both tiers, and the sessions ran after it, 264/0/3: #35 again; `ci/red37-39318541896.txt`); at `cd05c3b` **961/0/38** both tiers and under `taskset` (`head2`) | held |
| #34 | shapes as listed, the same on both hosts | as listed, row for row, linux and macOS, both tiers (§6.1) | held |
| | threads 2; descriptors 0–2, the hub's pair, the terminal and the history file | threads 2 everywhere; the hub's **two pipes, both ends each** (3–6), the terminal (7); **no history file held open** (it is opened per write) | held but for the history file |
| | dash 100–400 µs a forked shape; pelt 3–30 µs | dash 100–156 µs; pelt release 4.5–12.5, native 21–45 | dash held; pelt held on release, **native over 30 µs for five shapes** |
| | nine corpus rows, the session, 2.11/18 and wait/7 | the nine, the session and **nine** statements (2.9.2/8, 2.9.2/9, 2.11/18, 2.13/6, 2.13/7, 2.13/11, 2.13/12, wait/7, dot/8) | held, more statements than predicted |
| static pelt | trunk gives sh18's `76f3fc40…`; the system-call set unchanged | trunk rebuilt to **`76f3fc40…`**; at `cd05c3b` **`7be05ec0478f624dc296d7b5c2a27f2b5b9348563f1ea47ed15b745eb402d0ca`** (15,200,336 bytes, ET_EXEC, no PT_INTERP, hashed twice); `tools/syscall-census` at `cd05c3b`: **the same 50 calls by name as sh18's head** (`sysc/head2/census.txt`, `logs/sysc-head2.log`; the timing-sensitive cases part under strace, reported, not judged, as at sh18) | held |

**Not predicted.**

- **The first plant's word reached nothing.** `Done` → `Ended` turned
  no corpus case and no session red on kasumi (notices go to standard
  error, which both harnesses compare by presence only; no corpus
  `.out` holds `Done`), so the plant used the `Running` word, which
  six sessions read on standard output (`logs/plant/`).
- **The new rows cost the macOS job its time.** Five program rows
  (30,000 spawns each) took nine minutes a tier on the macOS runner
  and the plant's job ran into its 45-minute limit; the rows were cut
  to one program row and seven built-in rows (`11b8c5a`), each built-in
  row seen red at trunk and green at the head on kasumi
  (`logs/shape-rows-v2-trunk-head.log`). No limit was raised.
- **A `set -m` script keeps a slot a job until its loop ends**: its
  notices come after the complete command, so a loop's finished jobs
  wait in the table (`logs/prof-b-setm.txt`: `jb_add_proc` growing);
  not measured against dash, not gated, named in §8.

## 4. Evidence index

- **The prediction:** `9556d3c`, before the first change (`f57f901`);
  #34's re-scoped prediction `da85a86`, before any #34 measurement;
  #37's `2e51375`, before its cases (`f00797b`) and its fix (`cd05c3b`).
- **The cause, measured at trunk:** `logs/base-bgshapes.log`,
  `logs/dash-bgshapes.log`, `logs/base-builtins.log`,
  `logs/dash-builtins.log` (`probe/bgshapes.py`); the heap profile
  `logs/prof-base/` (`probe/heapprof.py`, `probe/profbg.sh`); one
  list's cost `logs/listcost.txt` (`witness/listcost/main.lu`); the
  references' job memory `refs/w01`–`w10` (`probe/scripts/`).
- **Each fix's share:** `logs/bg-a-bgshapes.log`, `logs/bi-a-bgshapes.log`
  (the three `src/` fixes), `logs/bg-b-bgshapes.log` and
  `logs/prof-a-setm.txt`, `logs/prof-b-setm.txt` (the notice and text).
- **Seen red:** trunk's binaries on the sh19 rows, every row FAIL on
  both tiers (`logs/red-shape-*.log` for the first nine,
  `logs/shape-rows-v2-trunk-head.log` for the eight that stand); the
  plant in CI, run **39308407198** (`ci/plant-39308407198.txt`) and its
  local twin (`logs/plant/`); #37's two cases at `50d9354` on kasumi
  and in the PR's run **39318541896** at that head.
- **The gauntlets:** `gauntlet.sh`; `logs/head.status` (`a7d3455`, all
  37 gates 0) and `logs/head2.status` (`cd05c3b`, all 37 gates 0:
  corpus **961/0/38** both tiers and both under `taskset -c 0-3`,
  sessions 264/0/3, statements 505 of 547), every step's log in
  `logs/gauntlet/`.
- **CI green:** run **39316879930** at `4d01c75` (#33, #35 and #34's
  head: every job and step success on linux x86-64 and macOS arm64,
  aarch64's refusals asserted; the macOS job took 40 min 53 s of its
  45); run **39321161832** at `cd05c3b` (the last `src/` commit, with
  #37: every job and step success, macOS 37 min 51 s); the run at the
  PR's final head is in the PR body.
- **#34:** `probe/shapes/` (the shapes, `state.py`), `refs/shapes/`,
  `logs/state-*.txt`, the diagnostic runs **39305606803** and
  **39307007029** (`ci/diag-*.txt`, branch `sh19-macdiag`, never to
  merge); `probe/bench/` and `logs/bench-pin0-3.txt`,
  `logs/bench-pin10-13.txt`, `logs/bench-pin0-3-contended.txt`.
- **PAX:** `mkpelt-job.sh`, `mkpelt-run.sh`; `logs/mkpelt-trunk.log`
  (trunk `cc2fdc9` → `76f3fc40…`, sh18's digest), `logs/mkpelt-head.log`
  (`914885b`, the #33 head → `2bc1c0c5…`), `logs/mkpelt-fix.log`
  (`cd05c3b`, the last `src/` commit → **`7be05ec0…`**).

## 5. Done-when

- Branch `sh19`, PR #36 open and unmerged; the PR's run at the final
  head (RULES.md §6: the lane hands back with its id); lane-audit from
  the org directory, its exit status read directly.
- pelt#33, #35, #37 close-ready; #34 answered by §6 (it stays open for
  sh20). None filed or closed by the lane.

## 6. #34: pelt's fork-adoption note, for sh20

Ruling #90 (2026-10-19): wolf gets a user-visible `os_fork` whose child
keeps running wolf code (s247, wolf 0.2.34), and pelt's sh20 makes its
subshells processes after that pin. This section is what sh20 starts
from. It designs nothing of `os_fork` itself (s247's) and discusses no
alternative. Every row below was run; the commands are in
`notes/sh19-evidence/probe/shapes/` and `probe/bench/`.

### 6.1 What each in-process shape does today

`probe/shapes/shapes.sh` under pelt at this branch (both tiers) on
kasumi and on both CI hosts (dispatched runs **39305606803** and
**39307007029** on `sh19-macdiag`, never to merge;
`ci/diag-*.txt`), and under dash 0.5.13.4 and `bash --posix` 5.3.20 in
the container (`refs/shapes/`). pelt answers **the same on linux and
macOS, on both tiers**, row for row.

| shape | pelt today (linux = macOS) | dash, bash (linux) |
|---|---|---|
| `( list )` | in pelt's process, its changes undone by a frame (`sh.state`'s `frame_open`/`frame_close`): a program started inside it, not as its last command, has **pelt** as its parent | a child process: such a program's parent is the subshell |
| `( cmd )`, `$( cmd )`, one simple command | the program is pelt's child | **the same**: both shells run the last command of a subshell in the subshell's own process, so its parent is the shell (`w11`, and `shapes.sh` before its `; :` was added) |
| `( list ) &`, `{ list; } &` | runs to its end **before** the next command (`( sleep 0.3; echo a ) & echo b` prints `a b`); `$!` is a number no process has (`kill -0 $!` fails); a finished job is recorded afterwards | concurrent (`b a`); `$!` a live process |
| `$( list )` | in-process, its output caught in pelt's own buffer (`caps`/`cap_data`): a program inside it, not last, has **pelt** as its parent | a child process writing a pipe |
| a pipeline stage pelt runs itself (a built-in, a compound command) | runs to its end before the next stage starts (`{ echo one; sleep 0.3; echo done >&2; } \| { read v; … }`: `producer-done` before `reader-got-one`), its output caught and fed on; a program stage after it is **pelt's** child; **an endless producer never ends**: `while :; do echo y; done \| head -n 1` prints nothing and is killed at 3 s on linux (exit 124) and macOS (exit 142), where dash and bash print `y`, 0 | concurrent; each stage a child |
| a function in a pipeline | as a stage pelt runs itself (`f-done` before `reader-got-one`) | concurrent |
| an assignment in any stage, the last included | not kept (`: \| z=1` leaves `z` 0) | not kept: dash and bash run the last stage in a subshell too (`w11`) |
| `exec cmd` in a subshell | the shell goes on (pelt starts `cmd` as its child and waits) | the shell goes on (`cmd` replaces the subshell) |
| job control | a pipeline with such a stage is **no job**: its programs keep `SUSPEND` ignored and Ctrl-Z does nothing (sh18 `9b06c8e`, `session:c_jc_mixed_pipeline` pending) | Ctrl-Z stops the whole pipeline |

### 6.2 What the forked child must do first

From POSIX.1-2024 XCU (numbered as in the 2024 text: 2.9.3.1
Asynchronous AND-OR Lists, 2.11 Job Control, 2.12 Signals and Error
Handling, 2.13 Shell Execution Environment) and the `trap` and `wait`
pages; "dash" means a black-box run already recorded in `refs/`:

1. **Traps**: every trap that is caught is set back to the default
   action, every ignored one stays ignored (2.13, `trap`). The one
   exception POSIX allows: a command substitution whose only command is
   `trap` may list the parent's traps (`trap`); dash does
   (`signal/c_trap_cmdsub_shows_parent`, pending `trap-in-cmdsub`), so
   sh20 decides it by lexical look at the substitution, as the page
   permits, before the reset. A trap set inside the child is the
   child's; the parent's `EXIT` trap never runs in the child.
2. **Not interactive** (2.13: the subshell of an interactive shell
   behaves as a non-interactive one, `$-` may still show `i`): no
   prompt, no line editor and so no `os_signal_wait_fd`, no history
   written, no notices. The signals an interactive pelt catches for
   itself go back to the default in the child unless a trap set them:
   measured at pelt's prompt `SigCgt` = INT, QUIT, TERM, CHLD and
   `SigIgn` = TSTP, TTOU (`logs/state-pelt.txt`); dash at its prompt
   ignores QUIT, TERM, TSTP, TTOU (`SigIgn 0x284004`) and its subshells
   take the defaults.
3. **No job table**: the child's table starts empty and job control is
   off in it (its children are not the parent's: `wait` in a subshell
   cannot wait for the parent's children, `wait/7`; dash's `$(jobs)` is
   empty, `w09`'s first form). The parent keeps every job and records
   the child: for `&`, **`$!` is the child's pid, set in the parent**
   (2.9.3.1); `$$` and `PPID` stay the shell's in the child (2.5.2,
   `sub-dollar-dollar` above).
4. **After `&` with job control off**: standard input `/dev/null`
   unless redirected (2.9.3.1) and SIGINT and SIGQUIT ignored (2.12), in
   the child before the list runs (pelt does both today around its
   in-process run, `run_async`).
5. **With job control on in the parent**: the child joins the job's
   process group (the first stage leads it), set by both parent and
   child as `os_spawn_job` does for programs; the parent hands a
   foreground job the terminal and takes it back; the child changes no
   group, takes no terminal and puts TSTP, TTIN and TTOU back to the
   default, so Ctrl-Z stops it with the rest of the job (2.11; this is
   what clears 2.11/18).
6. **Leave by the child's own door**: the child's end is `os_exit` with
   the list's status after the child's own `EXIT` trap, never pelt's
   exit path (which gives the terminal and group back and restores the
   terminal's mode: `tools/edit-witness` fails a session that leaves it
   changed, and a child doing it would undo the parent's editor mode).
7. **Before the fork, in the parent**: flush `sh.out` (pelt's own
   buffered built-in output), or the child writes it a second time.

### 6.3 What pelt state must be sane in the child

Measured on a running pelt (`probe/shapes/state.py`; linux `/proc`,
macOS `ps -M` and `lsof` in the diagnostic runs), both tiers, both
hosts:

| what a fork copies | pelt (linux = macOS) | dash | what the child does |
|---|---|---|---|
| threads | **2** in every situation (a script waiting on a program, with a trap, in `$( )`, in a pipeline; at the prompt; with a job running): `main` and the signal hub's drain thread (s243) | 1 | none of its own: a fork copies only the calling thread, so the hub must be made again in the child before its first listen, poll or wait. That is s247's (`os_fork`'s child re-initialisation), and sh20 must not call a signal or wait builtin before `os_fork` returns in the child |
| descriptors | 0–2; **3–6**, two pipes with both ends each (the hub's); **7** a pipe end while a `$( )` or a pipeline runs (the capture's or the pipeline's own); **7** `/dev/tty` with job control | 0–2; `10` the tty; `3` a pipe end in `$( )` | the hub's four are s247's; pelt's own: the tty handle (`jc_tty`) closed, every pipe end that belongs to another stage or to the parent's capture closed (or a reader never sees its end of input: `pipe/c_shell_producer_ends`, 2.9.2/9), the history file never opened |
| signal dispositions | script: `SigCgt` one runtime signal (33) only; with `trap … USR1 INT`: + INT, USR1; prompt: + INT, QUIT, TERM, CHLD, `SigIgn` TSTP, TTOU | caught only what is trapped | 6.2's items 1, 2, 5, from the reset trap table through `sig_apply` |
| the state (`sh.state`'s `Sh`) | variables, exports, read-only marks, functions, aliases, options, `$@`, `$0`, the command hash, `umask`, the cwd: as they are | | kept: the fork's copy is the subshell environment (2.13) |
| | the job table (`jb_*`, `pr_*`, `stash_*`, `def_*`), `jc_on`, `jc_tty`, `jc_pgid` | | emptied, off, closed (6.2 item 3) |
| | the captures (`caps`, `cap_data`, `pend_cap`), the pipeline's `stage_*` | | not the child's: its standard output is the pipe it was given, and the parent alone reads the capture |
| | `interactive`, `at_prompt`, the editor's state, `ed` | | off (6.2 item 2) |
| | the frame stacks (`istk`, `sstk`, `ji`, `fr_top`) | | a fresh base: nothing is put back at the child's end, it exits |

### 6.4 The cost: dash's per shape, the target

`probe/bench/run` (sh06's `tools/bench/run` with a loop per shape
beside the four census loops: 2,000 turns each, 9 runs, median wall
time, every shell's output byte-identical or the row is refused), run
in the container on kasumi **under `taskset -c 0-3`** at load 7.7
(`logs/bench-pin0-3.txt`; also cpus 10–13 at load 9.2,
`logs/bench-pin10-13.txt`, within 10% of it; an earlier pass on cpus
0–3 while another lane's four busy loops held them is kept as
`logs/bench-pin0-3-contended.txt` and not read). Per turn, loop counter
included:

| shape | dash | pelt today, release | pelt today, native |
|---|---|---|---|
| `( : )` | **100 µs** | 4.5 µs | 21 µs |
| `x=$( : )` | **104 µs** | 5.5 µs | 27 µs |
| `x=$(echo y)` | **104 µs** | 6.0 µs | 28 µs |
| `( : ) & wait` | **103 µs** | 7.5 µs | 35 µs |
| `{ :; } & wait` | **105 µs** | 7.5 µs | 32 µs |
| `: \| :` (both stages the shell's) | **146 µs** | 9.0 µs | 36 µs |
| `f \| :` (a function stage) | **146 µs** | 11 µs | 42 µs |
| `echo x \| { read y; }` | **156 µs** | 12.5 µs | 45 µs |
| `/bin/true` (control: a program) | 200 µs | **312 µs** | 339 µs |

The census loops (seconds, 2,000 programs or 1,000 pipelines or
200,000 expansions or 1,200 checks): fork dash 0.450, pelt 0.929;
pipeline 0.645, 0.953; param 0.425, 2.092; configure-shaped 0.413,
0.460. **Reading:** pelt's in-process subshells are 13–22× faster
than dash's forks today, and its spawn (which forks pelt's address
space and execs: px17) costs 1.56× dash's fork-and-exec. A fork of
pelt is the first half of that spawn, so **sh20's target is dash's
column**: each forked shape no slower per turn than dash's under
`taskset -c 0-3`, measured by this bench with the census loops, and
the shapes 6.5 keeps in-process no slower than they are today.

### 6.5 What fork clears, and the shape to take

**Cleared** (the subshell is a process): the nine `pending=fork` corpus
rows (`builtin/c_s_dot_special_file`, `env/c_subshell_concurrent`,
`pending/subshell_signal`, `pipe/c_concurrent_stages`,
`pipe/c_shell_producer_ends`, `redir/c_s_cmdsub_fd_pipeline`,
`signal/c_subshell_trap_reset`, `signal/c_trap_ignore_pipe`,
`wait/c_subshell`), the session `c_jc_mixed_pipeline`, and nine
statements pending on fork: **2.9.2/8, 2.9.2/9, 2.11/18, 2.13/6,
2.13/7, 2.13/11, 2.13/12, wait/7, dot/8** (`docs/CENSUS.md`'s
`pending (fork)` rows); the two named without a case
(`tests/diff/PENDING.md`: the endless producer, `exec` in a subshell);
and two recorded differences, `signal/c_wait_interrupted_term`'s order
(its sender becomes concurrent) and `$(jobs -p)` at an interactive
prompt (sh18 §8: empty, as dash's, once the child's table is empty).
**Not cleared by fork alone:** `signal/c_trap_cmdsub_shows_parent`
(the lone-`trap` exception, 6.2 item 1, is sh20's choice).

**Recommended shape for sh20.**
- **Fork every shape POSIX names a subshell** (`( list )`, `$( list )`,
  every list after `&`, every pipeline stage pelt runs itself, the last
  included), through one place in `sh.exec` that flushes `sh.out`,
  forks, and in the child runs 6.2's steps in order (traps, then the
  dispositions, the job table, the descriptors, interactivity) before
  the body, ending by 6.2 item 6. The parent's side is the one that
  exists for programs today: a job in a group, the terminal handed
  over, `os_wait_poll`.
- **Keep in-process** a `( cmd )` or `$( cmd )` whose body is one
  simple command the fast path finishes (`run_fast`: a program, a pure
  built-in), with `-x` off and no trap on the conditions it could
  raise: dash and bash run that command in the subshell's own process,
  so what can be observed of it (its parent, its pid, the signals sent
  to it) is what pelt's in-process run gives already (6.1, second
  row), at today's 5–6 µs. Everything else forks.
- **Gate**: the bench of 6.4 under `taskset -c 0-3` (each forked shape
  at or below dash's per-turn time), the nine corpus rows, the session
  and the nine statements met, `shape-rss` flat (a forked child's memory
  is not the parent's, so a loop of forks must keep the parent flat),
  and `tools/syscall-census`'s new calls listed for PAX (a fork is
  `clone` without `CLONE_VM` on linux; PAX serves it since px17 as an
  eager copy of every present user page, `paging.copy_user` at pax
  `d6fbcdc`, so on PAX a fork's cost grows with pelt's resident size,
  15 MB of static image and its heap: a px lane measures it).

## 7. Findings

- **Every built-in the fast path does not serve kept ~650 B a command**
  in the root before this lane (`logs/base-builtins.log`); now the ones
  with no assignment and no redirection keep only what they build. Still
  over the bound at the head: `cd .` 575 B a turn (the `PWD` strings),
  `eval :` 716 (its parse), `command true` 189, `umask 022` 151, `read
  x </dev/null` 1,667 (a redirection sends it down the full ordinary
  path, nine lists again). An issue to file (below).
- **`cmd &` with no `wait` keeps a job a turn** in pelt, dash and bash
  alike (5,000 `Done` lines, `w09`): POSIX keeps them known; pelt's slot
  costs 231–347 B a turn against dash's few bytes. Recorded, not gated.
- **The macOS job took 38 to 41 of its 45 minutes** (runs
  39321161832, 39316879930): the
  session corpus and `shape-rss` are the long steps; the next rows or a
  slow runner will cut it. A ruling is owed on the limit or a split of
  the job (this lane raised nothing).
- **px17's spawn, re-read:** wolf's spawn forks (`clone` without
  `CLONE_VM`), so PAX has served `fork` since px17, as an eager copy of
  every present page (§6.5).

## 8. Pending, not verified, named out

- **Pending, unchanged:** the nine fork rows, `c_jc_mixed_pipeline`,
  and the rest of `tests/diff/PENDING.md` (38 pending, as at trunk).
- **Recorded differences left:** `wait` then `wait $p` (dash answers
  4, pelt 127: pelt forgets at `wait`, dash at the next job, `w03`);
  `jobs` marks for unwaited jobs (`w05`); `CDPATH=/` gives `//bin` as
  dash does where bash gives `/bin` (`w12`).
- **A `set -m` script's loop** keeps a slot per job until the loop's
  complete command ends (the notices come after it): not measured
  against dash.
- **Not verified:** macOS by CI only (no build on nomad-1); linux
  aarch64 still builds no tier at 0.2.32 (asserted in CI); the bench
  ran on kasumi only, in the container, at load 7.7 (0–3) and 9.2
  (10–13).
- **Disclosed:** the harness refused my removing
  `kasumi:/tmp/.sh_history` (30 bytes, written by `state.py` with
  `HOME=/tmp` before it took `TMPDIR`); it is left for the orchestrator.
  Two of my own static-build containers overlapped for about twenty
  seconds after a launch with a short sha (both failed; the build was
  run again once, `logs/mkpelt-fix.log`). Two sh18 processes have sat
  idle on kasumi for 22 hours (`~/lanes/sh18/{pin,head}/target/static/pelt
  ../s.sh`, pids 1370174 and 1540529): not mine, not touched. Branches
  on origin never to merge: `sh19-plant`, `sh19-macdiag`.
