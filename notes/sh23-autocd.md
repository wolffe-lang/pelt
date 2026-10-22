# sh23 — `set -o autocd` (pelt#49; ruling #113)

Contract: `sprints/pelt/24-autocd/sh23-autocd.md` in the planning repo
(ruling #113, A). This file is the lane's record: §1 to §3 are committed
before the first change under `src/`, `tools/` or `tests/`, and before any
reference shell is run with the option; the rest is filled in as the work
lands.

## 1. Forbidden

As the contract and `sprints/RULES.md` say. No shell's source is read or
searched for (dash, bash, zsh, fish, busybox or any other), nor a libc's or
a kernel's. Behaviour comes from POSIX.1-2024 (XCU 2.9.1 "Simple Commands"
and its command search, 2.9.1.4; the `cd` and `set` pages), the shells'
manuals as documentation (bash's `shopt` list, the `autocd` paragraph:
"If set, a command name that is the name of a directory is executed as if
it were the argument to the cd command. This option is only used by
interactive shells."; zsh's `zshoptions`, `AUTO_CD`: "If a command is
issued that can't be executed as a normal command, and the command is the
name of a directory, perform the cd command to that directory. This option
is only applicable if the option SHIN_STDIN is set"), and black-box runs of
dash 0.5.13.4 (the control for the default, which has no such option), bash
5.3.20 and zsh 5.9 **only inside throwaway `--network none` containers**
whose `/usr` is kasumi's, read only (`notes/sh23-evidence/ctr.sh`). lope's
tree at `5ac37df` is the maintainer's and is read and run (its
`shell/pelt/*.sh`, `tools/hook-sessions`). No change to pelt#42's hook
beyond the precedence the contract states; no change to the pin (sh20 moves
it); the code change keeps to `builtin.lu`'s option table and one check in
`run_external` before `start_child` (sh20 is on `exec.lu`), plus the
option's field in the state. No build on nomad-1: kasumi under
`~/lanes/sh23/`, detached jobs by `setsid -f` with the pid recorded
(`launch.sh`), tests and measurements inside the container under
`taskset -c 0-3` with `ulimit -c 0`. No merge, no tag, no issue filed or
closed, no package installed, no other lane's run cancelled, nothing under
`~/.claude`, no attribution trailers. If the harness refuses an action, the
lane stops and reports.

## 2. Inputs, verified (2026-10-21, before any change)

| input | contract says | measured | drift |
|---|---|---|---|
| pelt trunk | `3b0bab9` | `origin/trunk` = `3b0bab9881f5…` (tl30's last note); branch `sh23` cut from it in its own worktree (`~/lanes/sh23` on nomad-1); kasumi's clone at the same commit | none |
| the pin | the seventh, wolf 0.2.32 / lupin 0.1.54, as it stands | `wolf-toolchain.toml` untouched; the release API's digests for the linux x86-64 pair read twice (releases 416327027, 415937354): `4c37f9c5…`, `175df238…`, equal to the file; `tools/fetch-toolchain` on kasumi hashed both OK (`logs/base-build.launch.log`) | none |
| `run_external` | the one place: search, then `unfound`/`run_cnf` | `src/sh/exec.lu:2346`: a name with no `/` is searched (`find_in` / `hash_find`); found nowhere, `unfound` (which may call `command_not_found_handle` when `hook`, interactive, defined, not inside it) and return; else `start_child`. A name with a `/` is not searched and goes straight to `start_child`, which says `NAME: cannot be run` and 126 for a directory. `hook` is false for `command NAME` (`builtin.lu:772`) and `exec`'s fallback (`exec.lu:2580`) | none |
| the fast path | — | `run_fast` (`exec.lu:994`) runs a found program itself, and goes the ordinary way (`slow()`) for a name not found and for a spawn that fails, so a directory reaches `run_external` either way | — |
| the option table | `builtin.lu` ~269–335 | `option_name` (`builtin.lu:265`), `print_options` (`:316`, eleven names in alphabetical order with their `$-` letter or `-`); the options a frame keeps are `state.lu`'s `opts_bits`/`set_opts_bits` (thirteen bits); `pelt -o NAME` reaches `bi_set` (`main.lu:63`) | the option needs one field in `Sh` and one bit in `opts_bits`, beside the table |
| lope | trunk `5ac37df`, `shell/pelt/jump.sh` | lope `origin/trunk` = `5ac37df22866…`; cloned to kasumi from a bundle (lope is private), built with its own `tools/build --release` at its pin (wolf 0.2.33): `target/release/lope` sha256 `b90c2170…`, sh21's digest. `jump.sh`'s `command_not_found_handle`: `[ -d "$1" ]` → `command cd -- "$1" && __lope_hook`, else `lope query --cwd`, then `lope query`, then `command cd -- RESULT && __lope_hook`, else 127. `pwd.sh` defines `cd` as a function (`command cd "$@" && __lope_hook`) so a visit is recorded | none |
| pelt#49 | the issue | read: `home/pax` and `/home/pax/` answer "cannot execute" on PAX with lope's hook loaded; A is the option | none |
| CHANGELOG, "the docs' options list" | named by the contract | **no `CHANGELOG` exists at trunk** (nor on any branch), and the docs carry no options list: the README's status paragraph names `set -o pipefail` in prose, and `docs/CENSUS.md` has the `set` rows | **yes**: §6 |

## 3. Prediction (committed before the first change, and before bash or zsh is run with the option)

### 3.1 The references (scored in §3.6 against black-box runs)

- **The extra words.** bash 5 hands them to `cd` as further operands, as
  if `cd -- DIR word…` had been typed; bash 5's `cd` refuses a second
  operand ("too many arguments"), so `DIR a b` answers 1 with a diagnostic
  and the shell stays where it was. zsh: AUTO_CD takes a lone word only;
  `DIR a b` is not a cd but the plain failed execution.
- **A directory named like a function.** The function runs (bash, zsh):
  the directory is tried only when command search found nothing, and a
  function is found first. The same for a built-in and for a program on
  `PATH` of that name.
- **A function named `cd`.** bash: the implied `cd` is the command `cd`,
  so a function of that name runs (lope's recorder would see the jump).
  zsh: the built-in (zsh records by `chpwd` instead).
- **What is said.** bash writes `cd -- DIR` to standard error before it
  changes directory (about 70% sure); zsh nothing.
- **Not interactive.** bash ignores the option (`DIR` in a script with
  `shopt -s autocd` is "Is a directory", 126); zsh applies AUTO_CD when it
  reads commands from standard input even without `-i`, and not for a
  script file or `-c`.
- **`command DIR`**: no cd in bash (126). **The hook**: with both,
  bash goes to the directory before `command_not_found_handle`.

### 3.2 The shape to build

`set -o autocd` / `set +o autocd`, a field `opt_autocd` (off), one bit in
`opts_bits` (a subshell's setting ends with it), listed by `set -o` and
`set +o` between `allexport` and `emacs` (the table's order is
alphabetical; no `$-` letter). `pelt -o autocd` reaches it through `bi_set`
as every `-o` does. One check in `run_external`, after the search and before
both `unfound` and `start_child`: when `hook` (the simple command's own
name, not `command`'s operand or `exec`'s), the option is on, the shell is
interactive, the name was not found (no `/`) or has a `/` (never searched),
and `fs_is_dir(NAME)`: the command is `cd -- NAME` with the words bash 5
gives it (§3.1, as measured), run as the command `cd` is (so a function
named `cd`, lope's, runs when bash's measurement says it does; else the
built-in), with the command's assignments and redirections as for any
command. Otherwise nothing changes: a file is still 126 and `cannot be
run`, no such path 127 and `not found`, the hook still called for a
slash-less name that is not a directory. A function, built-in or program of
that name never reaches `run_external`'s miss (functions and built-ins are
found in `run_fields`; a program is found by the search).

### 3.3 The rows (new cases)

| case | oracle | at trunk | at the head |
|---|---|---|---|
| `simple/autocd_off` (a script, the default: `d/e`, `$PWD/d/`, `..`, `d`, `"my dir"`, a file, no such path; status and where the shell is after each) | dash | ok | ok |
| `simple/autocd_script` (the same rows after `command set -o autocd 2>/dev/null`, and `-c`: a non-interactive shell does nothing with it) | dash | **FAIL** (`set -o autocd` refused; pelt's `command set` error still ends the shell, P09) | ok |
| `session:autocd_off` (interactive, the default: a slashed directory 126 said, a slash-less one 127 said, the hook still called for it) | dash; bash agrees | ok | ok |
| `session:autocd_list` (`set -o`/`set +o` show it off then on, in its place; `set +o autocd`; `eval "$(set +o)"` round trip) | by hand | **FAIL** | ok |
| `session:autocd_slash` (`home/pax`, `$PWD/home/pax/`, `..`, `~`; status 0, `PWD`, `OLDPWD`, `cd -` back) | by hand, after bash | **FAIL** | ok |
| `session:autocd_bare` (a child, `"my dir"`, `$d`) | by hand, after bash | **FAIL** | ok |
| `session:autocd_not_dir` (a file 126 said, no such path 127 said, both with a slash and without) | by hand, after bash | ok (the same answers) | ok |
| `session:autocd_wins` (a directory named like a program on `PATH`, a built-in and a function: each runs) | by hand, after bash | ok | ok |
| `session:autocd_words` (the extra words, as bash 5) | by hand, after bash | **FAIL** | ok |
| `session:autocd_hook` (a handler beside the option: a directory goes to `cd`, the handler not called; a fuzzy word goes to the handler) | by hand, after bash | **FAIL** | ok |
| `session:autocd_status` (a directory `cd` cannot enter: `cd`'s status and diagnostic; `command ./dir` still 126; in `( )` the shell stays) | by hand, after bash | **FAIL** | ok |
| `session:autocd_invoked` (`pelt -i -o autocd`: on from the command line; `"$0" -o autocd -c 'DIR'` is 126) | by hand | **FAIL** | ok |

Every hand-written transcript is written before the first change under
`src/`, from the reference answers of §3.6, and its `why=` names where pelt
parts from bash and zsh.

### 3.4 The counts

- Corpus: trunk's count (expected sh22's) **+2 cases**, both passing on
  both tiers; nothing else moves. With the option off **no existing row
  moves**: the rows that list the options filter or count the lines
  (`option/c_plus_o`'s `grep -c .`, the others `grep`), and `eval "$(set
  +o)"` takes the new line.
- Sessions: trunk's count **+10**, every one passing; nothing else moves.
- Statements: unchanged (the option is not POSIX); the CENSUS's "beyond
  POSIX" section gains one row, kind X, naming the sessions.
- Every other gate as at trunk (fmt, both builds, `wolf test`, the census,
  the width table, `glob-rss`, `loop-rss`, `shape-rss`, the witnesses, both
  harness self-tests, `oracle-record --check`).

### 3.5 The cost

With the option off (the default) the check is one boolean read on the
miss path only: no system call, nothing measurable. With it on, an
interactive shell pays one `stat` (`fs_is_dir`) for each command found
nowhere and each slashed command that reaches `run_external` (a found
program runs from the fast path and never gets there): one call beside the
miss's own search of every `PATH` entry, under 2 µs, inside the noise of a
10,000-miss loop. Measured by `strace -c -f` and wall time on a loop of
10,000 misses at `pelt -i`, the option off and on, on both tiers.

### 3.6 The result against the prediction

**The references** (black box, inside `ctr.sh`; the probes
`probe/sh/p01`–`p20`, the answers `refs/base/` and `refs/base2/`, one
shell a directory; the PTY rows `refs/pty-autocd.txt`):

| §3.1 predicted | measured | score |
|---|---|---|
| bash hands the extra words to `cd`, which refuses: status 1, stays | `cd -- child a b`, "too many arguments", status **2**, stays; the same for `child a`, `child other`, `./child x`, `child -P` (`p05-words`; the PTY's `sub a b` `st=2`) | right, but the status is 2 |
| zsh takes AUTO_CD for a lone word only | `child a b` 127, `./child x` 126 (`p05-words`; PTY `st=127`) | right |
| a directory named like a function, a built-in or a PATH program: it runs | runs in bash and zsh (`p04-wins`) | right |
| a function named `cd`: bash calls it, zsh the built-in | bash `fn cd [2] -- sub`, `-- ./sub`; zsh the built-in (`p06-cdfn`) | right |
| bash writes `cd -- DIR` on standard error (about 70% sure), zsh nothing | bash writes `cd -- NAME`, quoted for reinput, outside the command's redirections; zsh nothing (`p09-trace`, `p05-words`'s `.err`) | right |
| not interactive: bash ignores it; zsh applies it on standard input without `-i`, not in a script or `-c` | as predicted (`bash-script-autocd`, `bash-c-autocd`, `bash-stdin-autocd`, `zsh-stdin-autocd`, `zsh-script-autocd`, `zsh-c-autocd`) | right |
| `command DIR`: no `cd` in bash (126) | bash and zsh both `cd`: `command ./sub` and `command sub` status 0 in `/sub` (`refs/base2/*/p08-status`) | **wrong** |
| the hook: bash goes to the directory before `command_not_found_handle` | so (`p07-hook`) | right |

Not predicted: bash's `( )` and `$( )` do not autocd (a subshell is not
interactive) while a pipeline stage, `eval` and a function body do; `exec
DIR` is 126 in bash (`p12-exec`); with `CDPATH` bash checks the word from
here, then `cd` takes `CDPATH` (`p10-cdpath`; zsh tries `CDPATH` for the
word itself); a directory `cd` cannot enter (mode 000) is bash's `cd`'s
failure, status 1 and "Permission denied" said through the command's
redirections, where zsh does not take AUTO_CD (126 slashed, 127 bare,
`p08-status`).

**Inside a subshell** (measured at the resume, `probe/subsh.sh` and
`probe/subsh2.sh`, each row printing the directory from inside its
context, and `probe/subsh3.sh`, the status of `x=$(DIR)`;
`refs/subsh.txt`, `refs/subsh2.txt`, `refs/subsh3.txt`): bash 5.3 does not autocd
inside `( )`, `$( )`, a `{ }` group in a pipe or the last stage of one,
and does inside `eval` and a function body; zsh 5.9 only inside `eval`;
dash and trunk pelt have no option. **pelt at the head autocds in all of
them**: its subshells run in-process and keep `interactive`, as they do
for pelt#42's hook (`unfound` tests `sh.interactive` alone). The parent
never moves in any shell, so no session row sees it (`autocd_status`'s
`(sub)` row checks the parent); `x=$(DIR)` is where it shows: status 0
in pelt, where bash and zsh answer 127 (`sub`) and 126 (`./sub`). Put
to the maintainer as R-sh23-4 (§7), as built.

**What pelt does** (the shape of §3.2, built at `580246a`, `7776899`,
`564612b`): as bash in every row above but three, each a choice made and
put to the maintainer (§7): nothing is said but what `cd` says (zsh's
way); the extra words are `cd`'s operands as in bash, and pelt's `cd`
takes the first as dash's does, so `DIR a b` goes to `DIR` with 0 where
bash refuses with 2; `command DIR` is not a `cd` (126 slashed, 127 bare,
as pelt#42's hook is not called for `command`) where bash and zsh change
directory.

**The counts** (§3.4; gauntlet `g1` at `497d104`, `logs/g1.status`, every
gate 0; `g2` at `93561ad` the same, §4):

| | trunk `3b0bab9` (`logs/base-*`) | head `497d104` (`logs/gauntlet/g1-*`) | predicted |
|---|---|---|---|
| corpus, pass/fail/pending (pending passing) | 966/0/38 (2), both tiers | **968/0/38 (2)**, both tiers, with and without `taskset -c 0-3` | +2, nothing else moves: **right** |
| sessions | 273/0/3, both tiers | **283/0/3**, both tiers, with and without `taskset` | +10: **right** |
| POSIX statements (clause census) | 505 of 547 (93.2%), 41 not counted (kind X) | 505 of 547, **42** not counted | unchanged, one X row: **right** |
| fmt, both builds, `wolf test` (1 passed, no SKIP), width table, `glob-rss`, `loop-rss`, `shape-rss`, the exec, edit, history, signal and reap witnesses (both tiers, the edit and signal ones under `taskset` too), both harness self-tests, `oracle-record --check` (0 drifted) | 0 | 0 | as trunk: **right** |

The new cases at trunk (`logs/trunk-new-*`, trunk's binaries with the
head's tests): `simple/autocd_script` FAIL and `simple/autocd_off` ok; 9 of
the 10 sessions FAIL and `autocd_off` ok, on both tiers. That is the
table of §3.3 except two rows predicted to pass at trunk,
`autocd_not_dir` and `autocd_wins`: each types `set -o autocd` first,
which trunk refuses (said on standard error, so the transcript differs
there), and `autocd_wins` ends with `./fn`, the slashed name of the
directory, which the option enters (trunk: 126).

**The cost** (§3.5; `cost.sh` in the container under `taskset -c 0-3`, a
quiet kasumi, load 0.14; `cost/head/`, `cost/trunk/`): an interactive
pelt (`pelt -i`, the lines on standard input) runs a loop of 10,000
commands found nowhere, and of 2,000 `basename` found on `PATH`, the
median of seven runs interleaved:

| | 10,000 misses, off | on | 2,000 found, off | on | system calls, 1,000 misses, off → on |
|---|---|---|---|---|---|
| head, native | 0.348 s | 0.346 s | 0.752 s | 0.752 s | 29,247 → 30,276; `statx` 12,004 → **13,006** |
| head, release | 0.145 s | 0.145 s | 0.700 s | 0.701 s | the same |
| trunk, native | 0.348 s | (refused) | 0.758 s | (refused) | 29,252, `statx` 12,004 |
| trunk, release | 0.144 s | (refused) | 0.697 s | (refused) | 29,253, `statx` 12,004 |

With the option on a miss costs exactly one `statx` more (1,002 for 1,000
misses; the other 27 calls are the one extra input line, `set -o autocd`:
16 reads, 6 `rt_sigprocmask`, 2 writes, an `openat`, a `close`, an
`ioctl`), and no wall time a 10,000-miss loop can see; with it off the
head is trunk. A found program never reaches the check (it runs from
`run_fast`). **Right.**

**lope's session** (`autocd-jump.py`: lope `5ac37df`'s `init pelt` from
the ENV file, its `cd` function and `command_not_found_handle`, on a PTY
in the container; `logs/jump/{head,trunk}/rows-{on,off}.txt` and the
transcripts beside them). The same rows on both tiers:

| typed | head, `set -o autocd` | head, off (the default) | trunk (`set -o autocd` refused) |
|---|---|---|---|
| `t/alpha` | `/t/alpha` 0 (the option) | 126, cannot be run | 126, cannot be run |
| `ROOT/t/projects/` | `/t/projects` 0 (the option) | 126 | 126 |
| `..` | `/t` 0, from `/t/projects` (the option) | 0, from ROOT, the hook's `cd ..` | the same as off |
| `beta` | `/t/beta` 0, from `/t` (the option) | `/t/beta` 0 (the hook, by lope's query) | the same as off |
| `proj` (from HOME) | `/t/projects` 0 (the hook, fuzzy) | the same | the same |
| `t/projects/myapp` | `/t/projects/myapp` 0 (the option) | 126 | 126 |
| `myapp` (from HOME) | `/t/projects/myapp` 0 (the hook: lope's `cd` function recorded the option's jump) | 127, not found (never visited) | 127 |
| `zzqqxx` | 127, not found (the hook's) | 127 | 127 |

Trunk's rows are pelt#49's report (a slashed path "cannot be run" with
the hook loaded); the head with the option on answers it, the fuzzy word
still jumps by the hook, and the off rows are trunk's.

## 4. Evidence index

Everything ran on kasumi under `~/lanes/sh23/` (builds on the host, every
case and witness inside `ctr.sh`'s container, under `taskset -c 0-3` where
the gate says) and is copied here under `notes/sh23-evidence/`.

- **Prediction**: `08145f8` (§1 to §3.5), before the first change under
  `src/`, `tools/` or `tests/`, and before bash or zsh ran with the option.
- **References** (black box): `probe/sh/p01`–`p20` with `probe/run.sh`,
  the answers in `refs/base/`, `refs/base2/`, `refs/pty-autocd.txt`
  (`edfef82`); inside a subshell, `probe/subsh.sh`, `subsh2.sh`,
  `subsh3.sh` and `refs/subsh*.txt` (`eb1e5a0`); the ordinary path's
  shapes, `probe/wins2.sh` and `refs/wins2.txt` (`bfd3212`).
- **Hand transcripts**: `handtr.py` runs trunk pelt on
  `handtr/<case>.explicit` (the case's keys with each autocd line typed
  as its `cd -- WORD...`) and writes `handtr/<case>.tr`: the nine
  sessions at `ac2f8a8`, before the first `src/` change; `autocd_wins`'s
  four new rows at `be68723` (both trunk tiers identical).
- **Trunk**: `logs/base-*` (counts at `3b0bab9`); `logs/trunk-new-*`, the
  new cases with trunk's binaries: `simple/autocd_script` FAIL, 9 of the
  10 sessions FAIL, `autocd_off` ok, both tiers.
- **Gauntlet `g1`** at `497d104` (the code as built): `logs/g1.status`
  (every gate 0, `ctr=0`, `done`; the binaries' sha256 beside the build),
  `logs/gauntlet/g1-*.log`.
- **Gauntlet `g2`** at `93561ad` (`autocd_wins`'s new rows; the code as at
  `497d104`): `logs/g2.status`, every gate 0 (`ctr=0`, `done`), the two
  binaries byte for byte `g1`'s (sha256 `6b2ff495…` native, `b9b12f5d…`
  release); the counts as `g1`'s (968/0/38, 283/0/3, both tiers, with and
  without `taskset`); `logs/gauntlet/g2-*.log`. kasumi was shared with two
  other lanes' builds and tests while it ran (load 8 to 20 on 16 cores);
  the signal, edit and rss gates held.
- After `93561ad` the branch changes `notes/` only.
- **The cost**: `cost.sh`, `cost/head/`, `cost/trunk/` (§3.6).
- **lope's session**: `autocd-jump.py`, `logs/jump/` (§3.6).
- **Driver scripts**: `finish.sh` (the cost, lope's session, the plants
  at `497d104`), `finish2.sh` (B5 and B6 at `93561ad`, then `g2`), with
  their progress in `logs/finish.status`, `logs/finish2.status`.

**The plants** (ruling #104 R2: a `module` lane's breaks run locally and
are cited; no CI run was dispatched). Each is a patch on the head in
`plants/`, applied by `plant.sh` in a scratch worktree on kasumi, built on
both tiers, then run: `full` is the whole corpus and every session on both
tiers, `quick` is `simple/` and the 19 `autocd_*` and `cnf_*` sessions on
native. Every plant built (`build=0`; a compile error would have been
recorded and nothing run). Each `logs/plants/<name>/status` names the head,
the patch's sha256 and the binaries'.

| plant | the break | run | red (the FAIL lines, `logs/plants/<name>/*.log`, kasumi) |
|---|---|---|---|
| **A** | `src/` at trunk (`a-trunk-src.patch`; the release binary is trunk's byte for byte, sha256 `8d773735…`) | full, `497d104` | corpus 967/1/38 on both tiers: `simple/autocd_script`; sessions 274/9/3 on both tiers: `autocd_bare`, `autocd_hook`, `autocd_invoked`, `autocd_list`, `autocd_not_dir`, `autocd_slash`, `autocd_status`, `autocd_wins`, `autocd_words`. `simple/autocd_off` and `autocd_off` stay green, as every other row (`logs/plants/a/`) |
| **B** | the check unguarded (`fs_exists`) and first in `run_fields`, `autocd_dir`'s guards and `hook &&` dropped (`b.patch`) | full, `497d104` | corpus 965/3/38 on both tiers: `simple/autocd_off`, `simple/autocd_script`, `simple/c_126_127` (trunk's row: a slashed file is now `cd`'s); sessions 278/5/3 on both tiers: `autocd_invoked`, `autocd_not_dir`, `autocd_off`, `autocd_status`, `cnf_cd` (`logs/plants/b/`). The pause expected `autocd_wins` too: it stayed green (B6 below says why) |
| B1 | the option's guard dropped | quick, `497d104` | `autocd_invoked`, `autocd_off`, `cnf_cd` (`logs/plants/b1-option/`) |
| B2 | the interactive guard dropped | quick, `497d104` | `simple/autocd_script` (`logs/plants/b2-interactive/`) |
| B3 | `fs_is_dir` → `fs_exists` | quick, `497d104` | `autocd_not_dir` (`logs/plants/b3-isdir/`) |
| B4 | `hook &&` dropped | quick, `497d104` | `autocd_status`, `command ./sub` (`logs/plants/b4-hook/`) |
| B5 | the found program's guard dropped (`path.len > 0` with no `/`) | quick, `497d104` | **none** (`logs/plants/b5-found/`): no row held it |
| | | quick, `93561ad` | `autocd_wins` step 10, `path-traced st=0 /basename` (`logs/plants/b5-found-rows/sess-native.log`) |
| B6 | the check first in `run_fields`, before the function and built-in lookup, its guards kept | quick, `497d104` | **none** (`logs/plants/b6-first/`): no row held it |
| | | quick, `93561ad` | `autocd_wins` steps 7–10: `function-assign st=0 /fn`, `function-redir st=0 /fn`, `builtin-assign st=0 /echo`, `path-traced st=0 /basename` (`logs/plants/b6-first-rows/sess-native.log`) |

B5 and B6 were green at `497d104` because `autocd_wins`'s rows never took
the ordinary path: `run_fast` runs a program it finds itself, and
`run_slow` calls a function, or a built-in, typed without an assignment
(a function also without a redirection) before `run_fields` is reached.
So the order the contract asks for (a function, built-in or program wins)
was held only by where the check sits, not by a row. `93561ad` adds the
four shapes that reach `run_fields` and `run_external` (a function or a
built-in with an assignment, a function with a redirection, a program
under `set -x`, where `fast_ok` is false), each answered alike by bash,
zsh and dash (`refs/wins2.txt`) and written from trunk's answers
(`handtr.py`); the code is unchanged, so the rows pass at the head
(`g2`) and are red under B5 and B6.

## 5. Done-when

Ruling #104 (made after this contract was written) puts this lane in
`Footprint: module`: pelt's own program, one option, no CI, pin, spec,
runtime, codegen or loader. So:

- PR open, five sections by name, commits as bullets, a test checklist
  and the line `Footprint: module`; the final head pushed.
- The local gauntlet green at the code's head and cited (`g1`, §4); the
  planted breaks run locally and cited (R2, §4), no CI run dispatched for
  them; no `full-matrix` label.
- `wolf/tools/lane-audit.sh pelt sh23 <PR>` from the org directory:
  passing but for `tier pr`'s green, which the orchestrator merges on.
- Issues listed in §7, none filed or closed; pelt#49 closes on the merge.

## 6. The documents the contract names

- **CHANGELOG**: none existed at trunk or on any branch (§2's drift).
  This lane starts one, `docs/CHANGELOG.md` (`e0afbd2`, moved by
  `497d104`), with one entry under "Unreleased", and says where pelt
  parts from bash (`e185be4`). It sits under `docs/` because the CI
  planner's rules name prose narrowly (`ci/tiers.py`: `notes/**`,
  `docs/**`, `README.md` are PROSE); a new top-level file matches no rule
  and would make every later pull request that touches it run full.
- **"The docs' options list"**: there is none. pelt documents its options
  in prose: the README's status paragraph (it named `set -o pipefail`; now
  `set -o autocd` beside it, `6db6566`) and `docs/PLAN.md`'s list of the
  extensions after POSIX (`4d5639e`). `set -o`/`set +o` themselves list it
  (`autocd_list`).
- **CENSUS**: the "beyond POSIX" table gains `ed/26`, kind X, naming the
  ten sessions (`b18de6e`; `tests/census/clauses.tsv`); statements are
  unchanged (505 of 547) and the not-counted rows go 41 → 42 (§3.6).

## 7. Findings, issues to file (none filed by the lane)

**Issues**: none to file. pelt#49 closes on the merge (the PR says so);
nothing filed or closed by the lane.

**Rulings asked** (each implemented as recommended; any other answer is
one line in `run_autocd` or `run_external` and the rows that say it):

- **R-sh23-1, what is said.** bash writes `cd -- NAME` (quoted for
  reinput) on standard error before it changes directory; zsh says
  nothing. **Recommended and built: nothing but what `cd` says** (zsh's
  way): the jump shows in the prompt, and a user who types a path wants
  the directory, not an echo of the command they did not type. bash's way
  is one `emit` before the call in `run_autocd`.
- **R-sh23-2, the extra words.** bash hands them to `cd` as operands
  (`cd -- DIR a b`) and its `cd` refuses a second operand (status 2,
  stays); zsh takes a lone word only (`DIR a b` is 127). **Recommended
  and built: bash's shape, the words are `cd`'s operands, and pelt's `cd`
  does with them what it always does**: it takes the first and leaves the
  rest, as dash's `cd` does, so `DIR a b` goes to `DIR`, 0
  (`autocd_words`). The option adds no rule of its own; if pelt's `cd`
  ever refuses extra operands, the option follows.
- **R-sh23-3, `command DIR`.** bash and zsh both change directory for
  `command ./sub` and `command sub` (`refs/base2/*/p08-status`), which
  §3.1 predicted wrong. **Recommended and built: 126 (slashed) and 127
  (bare), unchanged**: `command` asks for a command and suppresses
  function lookup, and pelt#42's hook is not called for `command NAME`
  either (`hook` false); the option keeps to the same line, so `command`
  stays a way to say "run this, do not interpret it". bash's way is to
  drop `hook &&` from the one check in `run_external` and let the plant
  B4 rows (`autocd_status`'s `command ./dir`) move.
- **R-sh23-4, inside a subshell** (found at the resume, §3.6). As built,
  pelt's in-process `( )`, `$( )` and pipeline stages of an interactive
  shell take the option, as they take pelt#42's hook; bash takes it only
  in `eval` and a function body, zsh only in `eval`. The lane's brief
  says that when sh20's fork lands, `autocd_dir` tests
  `sh.interactive || sh.sub_of_i`, as sh20's `unfound` does: the fork
  then changes nothing here, and the as-built line is kept.
  **Recommended: bash's line, not built.** A command substitution is
  where a word that names a directory would otherwise succeed silently
  (`x=$(build)`: 0 in pelt, 127 in bash and zsh; `x=$(./build)`: 0,
  126), and both references agree. Built, it is one more condition in `autocd_dir`,
  `|| sh.sub > 0` (the depth `run_subshell` and `run_cmdsub` raise),
  which also holds after the fork, and one session row from
  `refs/subsh2.txt`'s bash answers, seen red at this head. Left as built
  because the brief's sh20 line decides the subshell's answer the other
  way; the maintainer's ruling picks one.

**Follow-ups, other lanes'**:

- **lp02** (lope's `init pelt` emitting the option): an older pelt
  refuses `set -o autocd` with a diagnostic and, in a shell that is not
  interactive, `command set -o autocd` still ends the shell (P09, pelt's
  open census item); `init pelt` is sourced by an interactive shell, where
  the refusal only prints, so a guard of `set -o autocd 2>/dev/null` is
  enough there (trunk's session above: refused, then the hook's rows as
  before). lope's `cd` function already records the option's jumps
  (`myapp`, §3.6), so nothing else in lope changes.
- **sh20** (the fork, pelt#50, beside this lane on `exec.lu`): when it
  lands, `autocd_dir`'s `sh.interactive` becomes
  `sh.interactive || sh.sub_of_i`, as sh20's `unfound` tests, so a forked
  subshell of an interactive shell keeps the option as it keeps the hook.
  Not done here: sh20 had not landed at this lane's final head (§4).
