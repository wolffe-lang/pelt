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

(filled in as measured)

## 4. Evidence index

(filled in)

## 5. Done-when

- PR open, five sections, commits as bullets, a test checklist; `tier pr`
  green at the final head; the `full-matrix` label added at that head.
- `wolf/tools/lane-audit.sh pelt sh23 <PR>` from the org directory: clean
  but for `tier full`'s green (the hand-back's run).
- Issues listed in §7, none filed or closed; pelt#49 closes on the merge.

## 6. The documents the contract names

(filled in)

## 7. Findings, issues to file (none filed by the lane)

(filled in)
