# sh17 — the POSIX gaps (pelt#10–#15)

Contract: `sprints/pelt/17-the-posix-gaps/sh17-the-posix-gaps.md` in
the planning repo (`ed700dc`). This file is the lane's record: §1 to §3
are committed before the first change under `src/`, `tools/` or
`tests/`; the evidence index (§4) is filled in as the work lands.

## 1. Forbidden

As the contract. No shell's source is read or searched for (dash, bash,
mksh, busybox or any other), nor a libc's or a kernel's (rulings
#42–#45). Behaviour comes from POSIX.1-2024 (XCU 2.2.4, 2.3.1, 2.9.1.4,
2.9.2 and the `alias`, `unalias`, `type`, `hash`, `command`, `read`,
`getopts`, `set` and `sh` pages), the shells' manuals as documentation,
and black-box runs of the reference binaries **only inside throwaway
`--network none` containers**: `refrun.sh` on kasumi starts
`archlinux:base-devel` with kasumi's own `/usr` mounted read-only, so
the binaries are the oracles of record (dash 0.5.13.4-1.1, sha256
`c6221703b6197ce2…` as `tests/diff/ORACLE` names it; bash 5.3.20-2 as
`bash --posix`), and nothing else of the host is visible; every
`tools/oracle-record` and `tools/session-record` run, and the
gauntlet's `oracle-record --check`, goes through it. A signal's
meaning is named, never a literal bit. The toolchain from the release
archives by digest, each read twice. No merge, no tag, no issue filed
or closed (listed in the report), no package installed on a host, no
other lane's CI run cancelled, nothing under `~/.claude`, no
attribution trailers. No build on nomad-1: kasumi, under
`~/lanes/sh17/` (one worktree per tree measured, pruned), detached jobs
by `setsid` with the pid recorded and stopped by that pid only.
Scratch under `~/lanes/sh17/`, never `/tmp`. Strict evidence (#571):
`wolf build` exit 2 is a compile error; process and terminal tests
also under `taskset -c 0-3`; SigBlk/SigIgn read before any signal row
is called red. Job control (P12, pelt#18) is out. If the harness
refuses an action, the lane stops and reports.

## 2. Inputs, verified (2026-10-17, re-derived before any change)

| input | contract says | measured | drift |
|---|---|---|---|
| pelt trunk | `06223a8` or later | `origin/trunk` = `06223a89613a…` (sh16's notes); branch `sh17` cut from it; no open PR | none |
| wolf 0.2.30 | `v0.2.30` at `1b37f368` | tag object `ffb7c5b3…` → `1b37f368228d…`, read twice; `wolf 0.2.30 (wolfgang, pin 1b37f36)` | none |
| lupin 0.1.53 | `v0.1.53` at `7896edd` | tag object `83631915…` → `7896eddc17fd…`, read twice | none |
| the digests | by digest, each read twice | the release API read twice for every archive, equal to `wolf-toolchain.toml`; the linux x86-64 pair downloaded twice on kasumi and hashed: wolf `4e55b39e…`, lupin `5db55332…` (`notes/sh17-evidence/logs/fetch.log`) | none; no pin change in this lane |
| the bundled std | wolf-std `fd6bcdc` | the pin `fd6bcdcb1dfe…`, staged by `tools/fetch-toolchain` | none |
| the issues | pelt#10–#15 as filed | all open; bodies as the contract cites; no comments | none |
| sh14's divergence list | pelt#28: say if touched | `trap -x`, unreported write errors, the census coin: **none touched** | — |
| the pending cases | — | 37 corpus cases and 1 session case wait on P02–P08 (`tests/diff/PENDING.md`: sh-option-parsing 2, alias 16, type 2, hash 1, command-p 1, dollar-single-quote 7, pipefail 2, read-trailing-delimiter 1, readonly-read-getopts 2, read-d 1, read-no-var 1; session `c_alias_interactive`); 37 statements pending on them in `tests/census/clauses.tsv` | — |
| the baseline | — | trunk `06223a8` on kasumi in its own worktree, every gate (`logs/base.status`): corpus 880/0/80 both tiers and under `taskset -c 0-3`; sessions 241/0/14; statements 451 of 545 | none |
| kasumi | `/home` ~30G | 32G free at the start; no mksh on the host | — |

### 2.1 What the references do

Rows in `notes/sh17-evidence/probe/*.rows`, driven by `probe.py` in
the container; answers in `logs/p0*-refs.txt` (dash, bash, and trunk
pelt beside them). Where POSIX.1-2024 speaks it decides; where it is
silent dash decides; bash only where dash lacks the feature.

**P02, the command line** (`p02-refs.txt`). dash and bash agree:
`-ec`, `-ce`, `-xc`, `-nc`, `-uc` take the letters and the string;
`-c -- string name arg` and `-ec -- …` too; `-eo pipefail` sets both;
a lone `-` ends the options and is dropped (`sh -s - x` gives `$1=x`;
`sh - file y` runs `file`). trunk pelt reads `-ec` and its kin as a file
name (127) and keeps `-` as `$1`. **A missing command file: POSIX `sh`
EXIT STATUS says 127 (bash); dash answers 2.** That is `sh -- -c` too:
`-c` after `--` is a file name. sh06 recorded the `--` row from dash
(`dashdash=2`) inside `sh/c_combined_options`; `sh/c_command_file_missing`
already takes bash for the same rule (`sh/6`). Unspecified, dash
followed: `-cs` runs the string and then standard input. Not
reachable: `$0` of `sh -c` with no name is argv[0] in both (`../sh`);
wolf hands a program no argv[0] (`env_args`), so pelt says `pelt`.

**P03, aliases** (`p03-refs.txt`, `p03b-refs.txt`), dash and bash
agreeing except where marked: an alias is expanded in command position
(after `;`, `&&`, `|`, `(`, `{`, `!`, `then`, `do`, after assignments
and redirections), never a reserved word in its grammatical place
(`alias if=…` leaves `if … fi` alone), and its value is read as input:
operators, reserved words (`for i in 1 2; do`), a newline, a `#`
comment that swallows **the rest of the line** (`alias c='echo a #'`
then `c b` prints `a`), a function definition's name (`alias f=g; f()
{ …; }` defines `g`). Recursion stops at a name already being expanded
(`a=b b=c c=a` → `a` not found). A value ending in a blank makes the
**next token** a candidate: a redirection operator or a quoted word in
that place ends the chain. **Parse time:** a function body, a `{ … }`
and the same line keep the aliases they were parsed under; `$(…)` and
`` `…` `` are parsed with their line in dash (an alias defined earlier
on the line is not seen; bash sees it in backquotes); `eval` and `.`
parse when they run. A subshell's and a substitution's alias changes
end with it. `alias` prints `'name=value'` quoted whole (dash; bash
`name='value'`), `alias -p` is a name (dash, POSIX names no option),
`alias --` drops the `--` (POSIX XCU 1.4; dash says it is not found),
`unalias` with no operand 0 (dash; bash 2), `unalias -z` 2,
`unalias a nope b` removes both and fails. Names: dash refuses blank,
`} & ; | < > ( ) \ " ' $` and backquote (2), takes every other
printable byte including `/` and a leading `-`. `command -v` of an
alias is `alias 'q=echo x'`.

**P04, the command search** (`p04-refs.txt`). dash remembers every
utility found by a search: a run, `hash name`, `command -v`, `type`,
and a pipeline stage (the parent searches); not a subshell's or a
substitution's, not one a command's own `PATH=` assignment found, not
`command -p`'s. Assigning `PATH` (even to its own value) or `hash -r`
forgets them all. A remembered path is used without a search: a
program put earlier on `PATH` later is not found (`b` twice), one whose
execute bit went answers 126; one that is gone is searched for again
(`a`, then `b`). `hash` lists full paths, one a line; `hash builtin`,
`hash function`, `hash /path` answer 0 and remember nothing; a missing
name fails (1) and the rest are still remembered; `hash -v`, `hash -z`
2. `type`: one line per name on standard output, **including "not
found" (127)**; a name with a slash is itself when it is an executable
file. `command -p`: dash's default path begins `/usr/sbin`; bash's
`/bin`. `command -v ./plain` of a file with no execute bit fails (127);
trunk pelt prints it. sh06's `command/c_p` piped `command -p -v ls`
into `sed` under `PATH=/nonexistent`, so its recorded line was `sed`
not being found, not `command -p`'s answer.

**P05, `$'…'`** (`p05-refs.txt`). **dash 0.5.13.4 has `$'…'`** (the
clause table's note says it has none; every `c_ds_*` meta already says
`dash=agree`). Both: `\" \' \\ \a \b \e \f \n \r \t \v`, `\cX` (`\c\\`
is FS, `\c?` DEL), `\x` one or two hex digits, `\ddd` one to three
octal digits (the value modulo 256), a NUL from either ends the string
(the rest up to the quote is dropped), an unknown escape keeps its
backslash (`\q`, and dash's `\E` and `\?`); inside double quotes and
in a here-document body `$'` is ordinary; unquoted inside `${x-…}` and
`${x#…}` it is a quote; `<<$'E'` is a quoted delimiter `E`. dash only:
`\u` and `\U` (UTF-8 of the code point), and `\x` with no digit is a
NUL. Where they part, POSIX decides `\xe9` (the byte: bash); pelt
cannot send a byte that is not UTF-8 (W06, pelt#20), so a lone `\xe9`
becomes `?` where `\xc3\xa9` is `é` as in bash.

**P06, `pipefail`** (`p06-refs.txt`): both have it. The status is the
rightmost non-zero stage's, 0 when all succeed; `!` inverts that; `set
-e` sees it; a stage killed by SIGPIPE counts (`yes | head -1` 141); a
subshell's and a function's `set -o pipefail` is the subshell's and the
caller's as for any option; `set +o` and `set -o` list it.

**P08, `read`** (`p08-refs.txt`, `misc-refs.txt`). Both: the last
variable takes the rest of the line **less one trailing delimiter when
the rest is a single field** (`a:b:c:` → `c`; `c::` stays `c::`; `a:`
alone → `a`; `a\:b:` → `a:b`); a readonly or invalid name fails (dash 2)
after the variables before it are assigned, and those after it are
not; `getopts` into one fails 2. `read` with no variable: dash 2, bash
`REPLY` (unspecified; dash followed). dash has no `-d`; bash, the
reference for it: `-d c` reads to `c` (the first byte of a longer
operand), `-d ''` to a NUL, newlines are data, a backslash escapes the
delimiter and backslash-newline still continues, `-rd ''` combines,
end of input assigns and answers 1.

## 3. Prediction (committed before the first change)

### 3.1 The design, per issue

- **#10 (P02).** `sh.main` reads option letters as one cluster: `c`,
  `i`, `s` are the command line's; `o` takes the next argument as an
  option name (`-eo pipefail`); the rest go to `set`. A lone `-` ends
  the options and is dropped; `--` ends them. `-cs` runs the string,
  then standard input (dash). A missing command file stays 127
  (POSIX); the `--` row of `sh/c_combined_options` moves to a new case
  `sh/c_dashdash_operand` with `oracle=bash`, as `sh/6` already does.
  `set` takes `-o name` inside a cluster too (`set -eo pipefail`).
- **#11 (P03).** The alias table lives in the tree (`Ast.aliases`), so
  every parser sees it; `alias` and `unalias` write it through the
  journal (`J_ALIAS`), so a subshell's changes end with it. The parser
  substitutes in command position before reserved words are looked at
  (`parse_command`), and on the token after a value ending in a blank:
  the word is replaced in the text by the value followed by the rest
  of its line (a new buffer; the outer text waits on a stack and the
  lexer returns to it at the line's end), so the value is read as
  input — a comment takes the rest of the line as in dash. An alias is
  not expanded inside its own text (each expansion's extent is
  tracked). `$(…)` is checked at parse time without aliases (its text
  is parsed again when it runs, with the aliases then in force). An
  interactive line skips the one-command fast path while any alias is
  defined, and `needs_more` sees the table. `command -v`/`-V` show
  aliases.
- **#12 (P04).** A table `name → path` in the state, valid for one
  value of `PATH` (it is emptied when `PATH` is assigned, or found to
  differ); a hit runs without a `stat`, a miss searches and
  remembers — in the fast path too, by a write the real state makes
  after the command (`commit_fast`). A command's own `PATH=` search,
  `command -p` and a name with a slash are not remembered. A
  remembered path that is gone is searched for again and replaced. Not
  journaled: a subshell's finds stay (a pipeline stage is how dash
  finds them too); `PATH` coming back from a subshell empties the
  table. `hash` (list, names, `-r`), `type` (pelt's own words, every
  line on standard output, 127 for a name not found), `command -V`
  answering as `type`, `command -v` requiring the execute bit, and
  `command -p` searching `/usr/bin:/bin:/usr/sbin:/sbin` (pelt's
  choice: the standard utilities on linux and macOS). `command/c_p` is
  rewritten to call `sed` by its path and recorded again from dash.
- **#13 (P05).** The lexer reads `$'…'` as one quoted part (a
  backslash escapes the next byte) outside double quotes; expansion
  decodes it to quoted bytes (POSIX's escapes and dash's `\u`/`\U`);
  `brace_end` and `paren_skip` step over it; a here-document
  delimiter decodes it.
- **#14 (P06).** `set -o pipefail` is an option (`opt_pipefail`, kept
  by frames, listed by `set ±o`); a pipeline keeps each stage's status
  on the state's stack beside its child and answers the rightmost
  non-zero one when the option is on.
- **#15 (P08).** `read`: the single-field rule for the last variable,
  names checked as they are assigned (a readonly or invalid one: a
  message, status 2, the rest unassigned), no operand refused (2),
  `-d delim` (the first byte; `''` a NUL) through a byte reader that
  stops at it; `getopts` into a readonly variable: 2.

### 3.2 Tests

- **Every pending case of the six issues leaves pending** (37 corpus
  cases, `c_alias_interactive`), `read/c_no_var` included; and
  `sh/c_dashdash_operand`, `command/c_p` (re-recorded).
- **New cases** from the probe rows, recorded by `oracle-record` in
  the container (about 40: aliases after assignments and redirections,
  reserved words, function names, comments, chains, parse time,
  subshells, `alias`/`unalias` forms; `hash`'s table; `type`'s kinds;
  `$'…'` escapes; `pipefail` rows; `read` delimiters and targets);
  `oracle=bash` only for `read -d`; a new session case for an alias at
  the prompt in a pipeline. Table checks in `sh.selftest` for the
  `$'…'` decoder and the read splitter.
- **Census**: the 37 statements leave pending, and the new cases are
  named under them.

### 3.3 The numbers

| | trunk | predicted at the head |
|---|---|---|
| corpus | 880/0/80 | **(917 + new)/0/43** on both tiers and under `taskset`: the 37 leave pending; falsified if any case fails or pending is not 43 |
| sessions | 241/0/14 | **(242 + new)/0/13** |
| statements | 451 of 545 (83.5%) | **488 of 545 (89.5%)** |
| `edit-witness` | 11 rows, idle 0 context switches | 11 rows green; idle 0 |
| real scripts | 76/3/1 aided | **verdict for verdict as trunk** (the known coins aside) |
| `statx` on `configure-shaped.sh` (1,200 checks), release, kasumi, `strace -f -c` | ~8,400 (sh06) | **under 1,000** at the head: one search per distinct name until `PATH` changes |
| memory: `loop-rss`, `shape-rss` | green | green: the table holds one entry per name |

### 3.4 The machines

native and release, as every lane. lupin and the checked machine:
predicted unchanged (lupin refuses at resolve naming
`os_signal_default`; the checked machine `unsupported`).

### 3.5 Plant

On branch `sh17-plant` (never to merge), CI narrowed to the ubuntu job
and dispatched once: the head with alias substitution turned off and
the pipefail status ignored. Predicted red: every alias case (16
leaving pending, the new ones) and both pipefail cases plus the new
ones, on both tiers; the session `c_alias_interactive` and the new
alias session; nothing else.

### 3.6 A static pelt for PAX

`pax/tools/mkpelt` at pax trunk inside Ubuntu 24.04 on kasumi (with
`ld.lld` present, as sh16), against this branch's head: an `ET_EXEC`
with no `PT_INTERP`; its sha256 in the report for PAX's next pin.
