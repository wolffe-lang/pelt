# sh21 — `command_not_found_handle` (pelt#42: lope's no-prefix jump, on Linux and on PAX)

Contract: `sprints/pelt/21-the-hook/sh21-the-hook.md` in the planning repo,
at trunk `90a8914` (ruling #91 R4: lope preinstalled on PAX with `lope init
pelt`). This file is the lane's record: §1 to §3 are committed before the
first change under `src/`, `tools/`, `tests/` or `.github/`; the rest is
filled in as the work lands.

## 1. Forbidden

As the contract and `sprints/RULES.md` say. No shell's source is read or
searched for (dash, bash, fish, zsh, busybox, mksh or any other), nor a
libc's or a kernel's. Behaviour comes from POSIX.1-2024 (XCU 2.9.1 "Simple
Commands" and its command search, 2.9.5 "Function Definition Command", 2.12
"Shell Execution Environment", the `command` page), the shells' manuals as
documentation (bash's "Command Search and Execution", fish's
`fish_command_not_found`), wolf's spec at the pin, and black-box runs of
dash 0.5.13.4, bash 5.3.20 and fish 4.9.3 **only inside throwaway
`--network none` containers** whose `/usr` is kasumi's, read only
(`notes/sh21-evidence/refrun.sh`). lope's tree at `5ac37df` is the
maintainer's and is read and run (its hook text, `tools/hook-sessions`,
`tests/hooks/expected.tsv`, the lp00 note). No change to the order of
command search; no hook in a non-interactive shell. No assertion deleted or
weakened; no timeout or retry as a fix. The toolchain from the release
archives by digest, each read twice. No build on nomad-1: kasumi under
`~/lanes/sh21/`, detached jobs by `setsid` with the pid recorded
(`notes/sh21-evidence/launch.sh`) and stopped by that pid only; PTY sessions
on shells the lane starts, each with a scratch `HOME` and `XDG_*`. No merge,
no tag, no issue filed or closed, no package installed on a host, no other
lane's CI run cancelled, nothing under `~/.claude`, no attribution
trailers. If the harness refuses an action, the lane stops and reports.

## 2. Inputs, verified (2026-10-20, before any change)

| input | contract says | measured | drift |
|---|---|---|---|
| pelt trunk | `be1a75d` | `origin/trunk` = `be1a75da0255…` (tl28's pelt#38 merge); branch `sh21` cut from it in its own worktree; kasumi clone at the same commit | none |
| pelt's pin | stays where it is (0.2.33 folds into sh20) | `wolf-toolchain.toml`: wolf 0.2.32 `v0.2.32` → tag object `d21c4b28…` → `72de141f6246…`; lupin 0.1.54 `v0.1.54` → `9c98d445…` → `0e536e8fb451…`; std `d37c911`; each tag read twice through the API; the release API's digests (releases 416327027, 415937354) read twice, equal to the file for all six archives; `tools/fetch-toolchain` on kasumi hashed the linux x86-64 pair OK (`logs/base-build.launch.log`) | none |
| the crawl's toolchain | wolf 0.2.33 `v0.2.33` at `85dab5d7`, lupin 0.1.54, std `cceda63` | `v0.2.33` → tag object `56110e4f…` → `85dab5d7e597…`, read twice; release 417610226's digests read twice; it is lope `5ac37df`'s pin, and lope is built with it (below); pelt is not | none (pelt keeps 0.2.32, as the contract says) |
| pelt#42 | the hook's exact shape | read: the name, interactive only, command search found nothing, never re-entered, the current environment, the expanded words with `$1` the name, the redirections around the call, its status the command's, 127 said as pelt's own not-found | none |
| lope | `5ac37df` | lope `origin/trunk` = `5ac37df22866…`; cloned to kasumi from a bundle of that commit (lope is private); built with its own `tools/build --release` at its pin: `target/release/lope` sha256 `b90c2170…` (`logs/base-build.launch.log`) | none |
| lope's pelt text | `src/cmd/init.lu` | `lope init pelt` = `shell/pelt/hook.sh` + `pwd.sh` (a `cd` function) + `cmd.sh` (`g`, `gi`) + `shell/posix/menu.sh` + `jump.sh`, which defines `command_not_found_handle`: `[ -d "$1" ]` then `command lope query --cwd`, then `command lope query`, then `command cd -- DIR && __lope_hook; return 0`, else `return 127`; its result in `__lope_result` from a command substitution, inside the handler | none |
| the oracle | `tools/hook-sessions --shells pelt`, 0 rows differ | at trunk: **0 of 10 pelt rows differ** from `tests/hooks/expected.tsv` (`hooks/base-pelt.tsv`) — because that file's pelt rows are pelt `cc2fdc9`'s, where the jump stays put: word `/home`, two `/home`, here `/t`, frag `/t` (its header: "its no-prefix rows stay where they were (sh21)") | **yes**: with the hook those four rows MUST differ from 5ac37df's file. The oracle is read against `hooks/expected-sh21.tsv`: lope's file with pelt's rows set to what bash, zsh, fish and fortsh answer there (all four agree on every step). Both comparisons are reported; lope's file wants its four pelt rows moved when lope pins a pelt with the hook (a lope issue to file) |
| `tools/mkpelt` | the static pelt, digest given | pax trunk's `tools/mkpelt`: pelt at `user/pelt.pin`'s commit, built `--release` with a `cc` that adds `-static`, in Ubuntu (never kasumi's CachyOS glibc); sh19's way (`notes/sh19-evidence/mkpelt-job.sh`): a throwaway `ubuntu:24.04` container with `ld.lld`, the pin's `PELT_REV` set to the head | none |

The counts at trunk `be1a75d` (kasumi): corpus **961/0/38** native
(`logs/base-diff-native.log`); sessions and the release tier in §4.

### 2.1 The references, measured (black box)

`notes/sh21-evidence/probe/`: fourteen POSIX-shell probes (`sh/p01`–`p14`)
and six fish ones (`fish/f01`–`f06`), run by `probe/run.sh` inside the
container under dash (a script, and `-i` on standard input), bash (`--posix`
and plain, a script, and `-i`), fish (a script, and `-i`) and pelt trunk
(a script, and `-i`), each with a scratch `HOME`, `XDG_*` and `TMPDIR`;
every answer is in `refs/base/<shell>-<mode>/<probe>.{out,err,exit}`.

| probe | dash | bash 5.3.20 `command_not_found_handle` | fish 4.9.3 `fish_command_not_found` | pelt `be1a75d` |
|---|---|---|---|---|
| p01/f01 a handler that `cd`s | no hook: `not found`, 127 | called with `$1` the name, `$2…` the words; **in a subshell**: the shell stays (`after: p01`) | called with `$argv` the words; **in the shell**: it moves (`after: there`) | as dash |
| p02/f02 return 0, 3, 127 | — | the status is the handler's (0, 3, 127; fall-off 0; last `false` 1); at 127 **nothing is said** | **127 whatever it returns**; the shell's own message is said | as dash |
| p03/f03 the handler runs the name again | — | **re-entered**, each call a subshell deeper (depth 1–4 to the probe's bound; the parent's count stays 0) | re-entered (1–4) | as dash |
| p04/f04 redirections | — | applied around the call (`>out 2>err` get the handler's lines) | **not applied**: the files are never made, and the handler's standard output goes to the shell's standard error | as dash |
| p05 the words | — | `[8][nosuch][two words][two][words][p][q][*][dflt]`, `"no such" a` → `[2][no such][a]` | — | as dash |
| p06 `FOO=bar nosuch` | — | `FOO` set and exported inside, unset after | — | as dash |
| p07/f06 `command nosuch`, `./nosuch`, `type`, `exec` | — | `command nosuch`: **called** (5); `./nosuch`: not called (127); `type`: not called; `(exec nosuch)`: not called | `command nosuch`: called; **`./nosuch`: called** | as dash |
| p08/f06 a pipeline, `$( )`, a function, `( )` | — | called in each | called in each | as dash |
| p09/f05 an assignment in it; `exit 7` in it | — | not kept; `exit` ends the subshell only (status 7) | kept; `exit` ends the shell | as dash |
| p10 `set -e`, the handler returns 3 | — | the shell exits 3 | — | as dash |
| p11 `unset -f` the handler | — | the plain not-found | — | as dash |
| p13 `nosuch &` | — | called in the background; `wait` 6 | — | as dash |
| scripts (`-script` columns) | — | **called in a non-interactive shell too**, `--posix` or not | called in `fish FILE` too | as dash |

## 3. Prediction (committed before the first change)

### 3.1 The shape to build

One place: the simple command's own command search (`sh.exec`'s
`run_external`, reached from `run_fields` after the command's redirections
are applied and its assignments expanded). When the name has no `/`,
neither the remembered path nor the search of `PATH` (the command's own
`PATH=` or the shell's) finds a file, **the shell is interactive**, a
function named `command_not_found_handle` is defined, and the shell is not
already inside it: the function is called as a function is — in the
current shell environment, `$@` the command's expanded words (so `$1` is
the name), the command's assignments made for the call and undone after
(as for a function, XCU 2.9.1), the redirections already in place around
it. Its status is the command's. When that status is 127 (and nothing is
leaving: no `exit`, no interrupt), pelt then says `NAME: not found` as it
always does, through the same redirections. Inside the call a name not
found is the plain not-found: a flag on the state, saved and put back
around the call, so the handler is never re-entered, from a substitution
or a function inside it either. The fast path is untouched (a miss there
already goes the ordinary way). Not changed: `command NAME` (the `command`
built-in asks for the utility and suppresses functions, XCU `command`: no
handler, pelt's choice where bash calls it), `exec NAME`, `type`, `hash`,
`command -v`, a name with a `/`, a found file the kernel will not run
(126) or whose interpreter is missing; the order of command search; a
non-interactive shell. In a pipeline, a substitution, `( )` or after `&`
the call is the subshell's, as any function's there is (pelt runs those in
process, in a frame that puts the directory back; sh20 forks them), so a
`cd` there stays there.

### 3.2 The rows (new cases)

| case | oracle | at trunk (no hook) | at the head |
|---|---|---|---|
| `simple/cnf_not_interactive` (a script, `-c`, standard input define the handler) | dash; bash differs | ok | ok |
| `session:cnf_skipped` (`command nosuch`, `./nosuch`, after `unset -f`) | dash; bash differs | ok | ok |
| `session:cnf_cd` (the handler `cd`s: the shell moves, `OLDPWD`, `cd -` back, an assignment kept; in `( )` it stays) | by hand | **FAIL** | ok |
| `session:cnf_127` (127 said through the redirections; 0 silent) | by hand | **FAIL** | ok |
| `session:cnf_rerun` (the name run again inside: not re-entered, count 1) | by hand | **FAIL** | ok |
| `session:cnf_status` (0, 3, fall-off 0, last `false` 1) | bash; dash differs | **FAIL** | ok |
| `session:cnf_redirect` (`>o 2>e`, a pipeline stage with `2>&1`) | bash | **FAIL** | ok |
| `session:cnf_words` (the expanded words, a name with a space) | bash | **FAIL** | ok |
| `session:cnf_assign` (`FOO=bar nosuch`: set inside, gone after) | bash | **FAIL** | ok |
| `session:cnf_contexts` (a pipeline, `$( )`, a function, `( )`) | bash | **FAIL** | ok |

The hand-written transcripts (`tr_by=hand`, each `why=` says where pelt
parts from bash and fish) are written before the first change under `src/`
and are what the head must answer byte for byte.

### 3.3 The counts

- Corpus: **961/0/38 → 962/0/38** on both tiers (one case).
- Sessions: trunk's count (expected **264/0/3**, sh19's) → **+9**, every
  one passing; nothing else moves.
- Statements: **505 of 547** unchanged (the hook is not POSIX; the cases are
  named `cnf_*`, not census cases).
- Every other gate as at trunk: `wolf test`, fmt, the census, the width
  table, `glob-rss`, `loop-rss`, `shape-rss` (the hook is one function
  lookup on the miss path only; the found path is unchanged), the exec,
  edit, history and signal witnesses, both harness self-tests,
  `oracle-record --check`.

### 3.4 The PTY oracle

`tools/hook-sessions --tool lope=… --shells pelt --pelt <head>` from the
lope tree at `5ac37df`, on kasumi, with fzf: against
`hooks/expected-sh21.tsv` **0 rows differ** (word `/t/beta/gamma`, two
`/t/projects/myapp`, here `/t/alpha`, frag `/t/beta`, the six others as at
trunk: `cd` 3 of 3, real ran, miss 127 said, `g` back, menu, fzf); against
lope's own `tests/hooks/expected.tsv` exactly those **four rows differ**,
in that direction.

### 3.5 The plants (RULES.md §7: a `tier pr` dispatch on a plant branch)

- **A, pelt without the hook**: the head's tests and `src/` at trunk. Red on
  exactly the eight `FAIL` sessions of §3.2, on both tiers; the corpus and
  `cnf_skipped` green.
- **B, the hook without its guards**: called in any shell, for `command`'s
  operand too, and re-entered. Red on exactly `simple/cnf_not_interactive`,
  `session:cnf_skipped` and `session:cnf_rerun`, both tiers; the other seven
  sessions green.

Between them every new row is seen red in CI.

### 3.6 The static pelt for PAX

pax trunk's `tools/mkpelt` at the last `src/` commit in a throwaway Ubuntu
24.04 with `ld.lld` (sh19's method): ET_EXEC, no PT_INTERP, a digest that
differs from sh19's `7be05ec0…` (the source moved), hashed twice; trunk
`be1a75d` rebuilt the same way gives trunk's own digest first (tl28 changed
no `src/`, so expected `7be05ec0…`). `tools/syscall-census`: the same set of
calls (the hook calls nothing new).
