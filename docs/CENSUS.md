# The census: what pelt lacks, measured

pelt at `b32bebc` (wolf 0.2.27 / lupin 0.1.50), measured on 2026-10-11
against dash 0.5.13.4 (the oracle of record, `tests/diff/ORACLE`) and
`bash --posix` 5.3.20, on linux x86-64 (kasumi) with CI on linux x86-64
and macOS arm64. Four measurements, each kept in the tree so it can be
taken again: the POSIX clauses, real scripts, the prompt, and speed.
The plan that follows from them is [`PLAN.md`](PLAN.md).

**The three numbers.**

| measure | result |
|---|---|
| POSIX.1-2024 XCU chapter 2 and the built-in utilities' pages, testable statements met | **400 of 527, 75.9%** (`tools/clause-census`) |
| real `sh` scripts that run as under dash (output, status, files) | **50 of 80, 62.5%**; 72 of 80 once four gaps are routed around (`tools/script-census`) |
| the largest single gap | **`test -r`, `-w`, `-x`, `-L`, `-h`, `-ef` answer wrongly**: 14 of the 80 scripts fail on it, the most of any construct, and it is pelt's own work |

## 1. The clause census

**Method.** Every normative paragraph of POSIX.1-2024 XCU chapter 2
(read from the Open Group's online edition, `pubs.opengroup.org/
onlinepubs/9799919799`, 2026-10-11) and of the utility pages for the
special built-ins and for `sh`, `alias`, `unalias`, `command`, `type`,
`hash`, `cd`, `pwd`, `echo`, `true`, `false`, `test`, `printf`, `read`,
`getopts`, `wait`, `kill`, `umask`, `ulimit`, `fc`, `jobs`, `fg` and
`bg` was cut into testable statements, written in this project's words
with an id (the clause, then a serial), and each statement given the
cases that show it: the corpus's existing cases where they do, and a
new case (`c_*`) where nothing did. Every new case was recorded from
dash by `tools/oracle-record`; where dash and POSIX part, the case says
so and takes `bash --posix` as its oracle (24 cases: `$'…'`, `;&`,
`getopts`' `OPTARG`, the declaration utilities, `read -d`, `trap -p`,
`cd -e`, `set -h`, `set -u` in arithmetic, `LINENO` in a function,
`sh`'s 127 for a missing command file). A case pelt fails is marked
`pending=` with what it waits on (`tests/diff/PENDING.md`,
`tests/session/PENDING.md`), so CI stays at 0 failures and each gap
stays visible. Statements that POSIX leaves unspecified or optional but
scripts lean on (dash's `echo`, `read` with no name, `$((++x))`) are
recorded and not counted (kind X).

`tests/census/clauses.tsv` is the table; `tools/clause-census` counts
it and checks it against the tree on every CI host. A statement is
**met** when every case that shows it passes; that is a sample of the
statement, not a proof.

**How the corpus was built.** sh01–sh05 built the corpus by area, as
the language arrived: the grammar, expansions, redirections and the
special built-ins by design; the utility pages only where a lane needed
one. 283 of the 532 statements had a passing case before this census.
Nothing covered aliases, `$'…'`, `umask`, `ulimit`, `type`, `hash`,
`fc`, `jobs`, `fg`, `bg`, the job-control clauses, or `test`'s file
primaries beyond `-e`, `-f`, `-d`, `-s`.

**Counts.** 471 new differential cases (110 pending) and 42 new
session cases (35 pending). The corpus is 804 pass, 0 fail, 117
pending on both tiers; the sessions 92 pass, 0 fail, 35 pending.
dash and `bash --posix` give different output on 96 of the new cases,
mostly in how they format messages and listings.

| part | statements | met | pending | gap | untestable | met, of the testable | had a case before the census |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2.1 Introduction | 2 | 1 | 0 | 0 | 1 | 100% | 1 |
| 2.2 Quoting | 19 | 10 | 9 | 0 | 0 | 53% | 9 |
| 2.3 Token recognition and aliases | 18 | 8 | 10 | 0 | 0 | 44% | 5 |
| 2.4 Reserved words | 3 | 3 | 0 | 0 | 0 | 100% | 1 |
| 2.5 Parameters and variables | 34 | 25 | 8 | 0 | 1 | 76% | 19 |
| 2.6 Word expansions | 67 | 66 | 1 | 0 | 0 | 99% | 44 |
| 2.7 Redirection | 27 | 27 | 0 | 0 | 0 | 100% | 19 |
| 2.8 Exit status and errors | 17 | 15 | 1 | 0 | 1 | 94% | 11 |
| 2.9 Shell commands | 68 | 61 | 7 | 0 | 0 | 90% | 46 |
| 2.10 Grammar | 15 | 15 | 0 | 0 | 0 | 100% | 7 |
| 2.11 Job control | 15 | 3 | 10 | 2 | 0 | 20% | 1 |
| 2.12 Signals | 5 | 3 | 2 | 0 | 0 | 60% | 3 |
| 2.13 Execution environment | 12 | 8 | 4 | 0 | 0 | 67% | 7 |
| 2.14 Pattern matching | 17 | 15 | 2 | 0 | 0 | 88% | 13 |
| 2.15 Special built-ins | 88 | 75 | 13 | 0 | 0 | 85% | 54 |
| `sh` (utility page) | 26 | 16 | 8 | 0 | 2 | 67% | 6 |
| `alias` (utility page) | 6 | 0 | 6 | 0 | 0 | 0% | 0 |
| `command` (utility page) | 7 | 4 | 3 | 0 | 0 | 57% | 3 |
| `type` (utility page) | 2 | 0 | 2 | 0 | 0 | 0% | 0 |
| `hash` (utility page) | 2 | 1 | 1 | 0 | 0 | 50% | 0 |
| `cd` (utility page) | 8 | 7 | 1 | 0 | 0 | 88% | 6 |
| `pwd` (utility page) | 2 | 1 | 1 | 0 | 0 | 50% | 1 |
| `echo` (utility page) | 1 | 1 | 0 | 0 | 0 | 100% | 1 |
| `true` (utility page) | 1 | 1 | 0 | 0 | 0 | 100% | 1 |
| `test` (utility page) | 15 | 9 | 6 | 0 | 0 | 60% | 8 |
| `printf` (utility page) | 9 | 6 | 3 | 0 | 0 | 67% | 6 |
| `read` (utility page) | 8 | 5 | 3 | 0 | 0 | 62% | 3 |
| `getopts` (utility page) | 7 | 7 | 0 | 0 | 0 | 100% | 2 |
| `wait` (utility page) | 7 | 5 | 2 | 0 | 0 | 71% | 5 |
| `kill` (utility page) | 6 | 2 | 4 | 0 | 0 | 33% | 1 |
| `umask` (utility page) | 4 | 0 | 4 | 0 | 0 | 0% | 0 |
| `ulimit` (utility page) | 4 | 0 | 4 | 0 | 0 | 0% | 0 |
| `fc` (utility page) | 4 | 0 | 4 | 0 | 0 | 0% | 0 |
| `jobs` (utility page) | 3 | 0 | 3 | 0 | 0 | 0% | 0 |
| `fg` (utility page) | 2 | 0 | 2 | 0 | 0 | 0% | 0 |
| `bg` (utility page) | 1 | 0 | 1 | 0 | 0 | 0% | 0 |
| **total** | **532** | **400** | **125** | **2** | **5** | **75.9%** | **283** |

Not counted: 18 statements recorded for what dash does where POSIX leaves the behaviour unspecified or optional (kind X).

**What the unmet statements wait on**, counted by statement (a
statement may wait on more than one thing):

| waits on | statements | whose work |
|---|---:|---|
| aliases (`alias`, `unalias`, XCU 2.3.1) | 17 | pelt |
| job control (`set -m`, `jobs`, `fg`, `bg`, Ctrl-Z, XCU 2.11) | 14 | wolf-lang, then pelt; PAX for PAX |
| `$'…'` (XCU 2.2.4, new in 2024) | 7 | pelt |
| a process per subshell and pipeline stage (no fork) | 7 | wolf-lang (or a ruling) |
| command history and `fc` | 6 | pelt |
| `test`'s file primaries | 5 | pelt (and wolf-lang for exact access) |
| `kill` built in | 4 | wolf-lang#141 |
| `umask` | 4 | wolf-lang s230 (merged, not released) |
| `ulimit` | 4 | wolf-lang |
| `$$`, `PPID` off linux | 4 | wolf-lang#141 |
| about forty others, one to two statements each | 53 | mostly pelt |


## 2. The script census

**Method** (`tools/script-census`). 80 real scripts, each pinned by
the sha256 of the script file (`tools/script-census.pins`), run under
dash and under a static pelt in throwaway `--network none` containers
with nothing of the host mounted but one scratch directory. Compared:
standard output byte for byte, the exit status, standard error by
presence, and a listing of the files each run made or changed. No
third-party script is in this repository; the tool fetches each by
digest. The dash in each image is that distribution's (Arch 0.5.13.4,
Debian 13 0.5.12, Alpine 3.22 0.5.12); every construct below was
checked again against the oracle's 0.5.13.4.

| group | scripts | same | differs |
|---|---:|---:|---:|
| autoconf `configure` (GNU hello 2.12.2, sed 4.9, gzip 1.14) and zlib 1.3.1's | 4 | 1 | 3 |
| automake 1.18.1 and libtool 2.5.4 helpers | 13 | 6 | 7 |
| git 2.56.0's test library (a 4-test file, and `t0000-basic`) | 2 | 0 | 2 |
| Debian 13 maintainer scripts | 17 | 10 | 7 |
| Debian init scripts and helpers | 7 | 2 | 5 |
| Alpine 3.22 package scripts and alpine-conf tools | 16 | 16 | 0 |
| small `#!/bin/sh` utilities (10 of them `shellcheck -s sh` clean: all 10 same) | 21 | 15 | 6 |
| **total** | **80** | **50** | **30** |

No script hung and none crashed pelt. A second pass (`--aided`)
rewrote each script so that the four most common gaps went around pelt
(`test` run from `/usr/bin`, `umask` skipped, `trap … 13` spelled
`PIPE`, autoconf's bracket-with-slash `case` arms rewritten): **72 of
80** then run as under dash, and the 8 left are constructs 5 to 8.

**The smallest constructs, ranked by scripts broken.** Each is a case
of this project's own writing (`c_s_*`), pending, recorded from dash.

| # | construct | scripts | case | whose work |
|---|---|---:|---|---|
| 1 | `test -x` is false for an executable file; `-r`/`-w` ignore the permission bits; `-L`/`-h` never true; `-ef` never true | 14 | `test/c_s_test_access` | pelt |
| 2 | `umask` is "not supported yet" (status 2) | 9 | `umask/c_s_umask_set` | wolf-lang (s230's `os_umask`, not yet released), then pelt |
| 3 | `trap ACTION 13` is refused (a number with no wolf meaning), though `trap … PIPE` is taken | 7 | `signal/c_s_trap_by_number` | pelt to record it; wolf-lang#679 to catch it |
| 4 | a bracket expression holding `/` never matches in `case` or `${x#…}` | 4 | `glob/c_s_bracket_slash_case` | pelt |
| 5 | in `$( exec 4>&1; { … >&4; } \| cmd >&3 )` a pipeline stage's write to descriptor 4 is lost | 3 | `redir/c_s_cmdsub_fd_pipeline` | pelt, tied to the in-process pipeline |
| 6 | unquoted `$*` on the right of an assignment, or as a `case` word, joins with nothing instead of IFS's first character — a **silent wrong answer**: configure computes `host_os=linuxgnu` | 3 | `param/c_s_star_assign_ifs` | pelt |
| 7 | every byte above 0x7f becomes `?` when it leaves pelt (an argument, a file name, `read`, a here-document), even valid UTF-8 — a **silent wrong answer** | 1 | `quote/c_s_high_bytes` | pelt; and bytes that are not UTF-8 cannot be a wolf `str` at all (wolf-lang) |
| 8 | `.` of `/dev/null` or a FIFO is "not found" and ends the shell | 1 | `builtin/c_s_dot_special_file` | pelt |

The per-script table (package, version, digest, licence, both exit
statuses, verdict) is `notes/sh06-evidence/scripts/scripts.tsv`; the
three shells' answers for every construct are in
`notes/sh06-evidence/scripts/constructs.md`.

## 3. The interactive census

Typed through a pseudo-terminal (`tools/session`, with keys, Ctrl-Z
and a `bash --posix -i` oracle added for what dash has no editor for)
and measured by `tools/interactive-census`.

| what a person meets | today | case | waits on |
|---|---|---|---|
| `PS1`, `PS2`, `ENV`, `exit`, Ctrl-D, Ctrl-C at the prompt and over a child, the terminal's own erase, kill and word-erase, two lines pasted at once | works | 92 sessions | — |
| arrows, Home/End, Ctrl-A/E/K/D, Alt-B/F, a line longer than the terminal's 4,095 bytes | none: typed into the command as bytes | `c_ed_*`, `c_long_line` | pelt (raw mode exists in wolf) |
| Up/Down history, Ctrl-R, `fc`, `!` in `PS1` | none | `c_ed_up_*`, `c_ed_search`, `c_hist_*`, `c_ps1_bang` | pelt |
| Tab completion of files and commands | none | `c_ed_complete_*` | pelt; a ruling |
| UTF-8 and wide characters at the prompt | erased a byte at a time | `c_ed_utf8_*` | pelt (and a width table) |
| a resized window | not heard | `witness/winch` | wolf-lang (window size, `SIGWINCH`) |
| `set -o vi` | accepted, does nothing | `c_vi_*` | pelt, after the editor |
| job control: `set -m`, `jobs`, `fg`, `bg`, Ctrl-Z, job numbers, completion notices | none | `c_jc_*` (11) | wolf-lang (stop reporting, `SIGCONT`, a group signal, an interruptible wait), then pelt; PAX for PAX |
| aliases at the prompt | none | `c_alias_interactive` | pelt |
| `set -o ignoreeof`, `MAIL` | accepted, do nothing | `c_ignoreeof`, `c_mail` | pelt |
| startup (`-c :`, and to the first prompt) | 1.35 ms and 2.70 ms median against dash's 2.32 and 2.32 (loaded host); 0.34 and 0.40 ms against 0.36 and 0.37 on the native tier, quiet | — | — |
| memory after 10,000 typed `i=$((i+1)); echo $i` | **33 MB and growing** (3.4 MB at 100, 18 MB at 5,000) against dash's flat 2.8 MB | `tools/interactive-census` | pelt (below) |
| a session typed a byte at a time, 20 ms a byte (about 500 baud, PAX's serial console) | the same output as typed at once | `PELT_SESSION_SLOW` | — |

**Memory.** The CI gate (`tools/loop-rss`, `tools/session-rss`) holds
a loop of simple commands flat, and it is: 0.3 KB a typed line. But a
line or loop body that is more than one simple command keeps
kilobytes each time it runs:

| each run of | kept, a script loop | kept, a typed line |
|---|---:|---:|
| `:` or `x=1` | flat | 0.3 KB |
| `true && true`, `{ true; }` | flat | 3.5 KB |
| `case a in a) :;; esac` | 0.3 KB | — |
| a function call | 1.3 KB | — |
| `x=$(true)` | 6.2 KB | — |
| `true \| true` | 9.9 KB | 10.6 KB |
| a script's top-level line, any | 1.7 KB | — |

A script of 20,000 `true | true` lines peaks at 258 MB; dash at 2.7 MB.
A `configure` run makes thousands of command substitutions and
pipelines (`notes/sh06-evidence/loopmem.sh`, `leak.py`, logs).

**What wolf gives a line editor today**, measured by the witnesses in
`notes/sh06-evidence/witness/` (built with the pinned 0.2.27, driven by
`drive.py` through a pseudo-terminal):

- **Enough to start.** `os_term_set_mode` turns canonical mode and echo
  off and back on exactly (`term_keys`: "mode restored: true"); a read
  of one byte returns each key (an arrow arrives as `27 91 68`); a read
  with `VMIN` 0 and `VTIME` 2 comes back empty after 0.2 s; the window's
  size can be learned by moving the cursor to the far corner and asking
  where it is (`24;80`).
- **No window size or resize.** No call answers `TIOCGWINSZ`, and no
  meaning in `[os.signal.set]` is `SIGWINCH`: resized twice while
  listening for all nine meanings, the program heard nothing
  (`winch`). `os_signal_listen(512)`, a bit no meaning has, answers ok
  (wolf-lang#679's second half).
- **A read is not cut short by a signal.** Listening for `INTERRUPT`
  and blocked in a read, the program was sent `SIGINT` and was still in
  its read two seconds later; the poll saw it only after a key came
  (`read_vs_signal`). An editor waiting for a key cannot wake for a
  child that ended, a resize, or a trap. A timed read (`VTIME`) is the
  workaround, at a tenth of a second's latency.
- **A stopped child is not reported.** A child stopped by `SIGSTOP`
  sat in state `T` while the parent stayed in `os_wait_status`, which
  returns only when the child ends; and there is no call to send
  `SIGCONT` (`stop_report`). Job control cannot start.
- **Arguments are UTF-8.** `os_spawn_fds` passes "é中" intact
  (`c3 a9 e4 b8 ad`), so pelt's `?` is pelt's; but the bytes
  `a \xff b`, a legal POSIX argument, cannot be made into a `str` at
  all (`argv_bytes`).
- **Not given:** a character-width table (`wcwidth`), and a way to put
  the terminal's mode back if the shell is killed.

## 4. Speed

`tools/bench/run`, nine runs each, median, on kasumi; output checked
identical across shells.

| loop | dash | pelt release | ratio | pelt native | ratio |
|---|---:|---:|---:|---:|---:|
| 2,000 × `/bin/true` | 0.329 s | 0.505 s | 1.54 | 0.521 s | 1.58 |
| 1,000 × `echo x \| cat \| cat >/dev/null` | 0.336 s | 0.568 s | 1.69 | 0.569 s | 1.70 |
| 200,000 turns of `${x#*/}`, `${#y}`, `$((…))`, `case` | 0.369 s | 1.446 s | **3.92** | 3.772 s | **10.24** |
| 1,200 configure-shaped checks | 0.337 s | 0.506 s | 1.50 | 0.561 s | 1.66 |

Under `taskset -c 0-3` the release ratios are 1.49, 1.56, 3.89, 1.44.

**Where the time goes.** In the expansion loop pelt runs 20.2 G
instructions to dash's 5.2 G (about 101,000 against 26,000 a turn) at
much the same IPC, with no system calls of note: it is pelt's own work
per command. About 29% of cycles are the wolf runtime making, growing
and checking lists, maps and strings; the rest is pelt's interpreter,
which parses arithmetic from text on every turn. The native tier is
2.6 times slower than release on this loop. A program started costs
pelt 57 system calls against dash's 34 (a full `clone`, a
`socketpair`, six `fcntl`, eleven `close`, three `rt_sigprocmask`, a
`recvfrom`; dash uses `vfork`), and pelt searches `PATH` for every
command: 8,432 `statx` in the configure-shaped run, 7,025 failing.

## 5. The clause table, statement by statement

Generated by `tools/clause-census --markdown` from `tests/census/clauses.tsv`.
### 2.1 Introduction

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| 2.1/1 | Operands become positional parameters 1..n and the command name special parameter 0 | met | `exec/argv0`, `func/args` |  |
| 2.1/2 | A first line starting with #! gives unspecified results | untestable |  | unspecified by the standard; pelt treats it as a comment (exec/script_no_shebang covers the kernel-refused case) |

### 2.2 Quoting

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| 2.2.1/1 | An unquoted backslash preserves the literal value of the next character | met | `quote/backslash`, `quote/c_backslash_each` |  |
| 2.2.1/2 | Backslash-newline is a line continuation, removed before tokens are split, and is not a token separator | met | `quote/continuation`, `quote/c_continuation_joins` |  |
| 2.2.2/1 | Single quotes preserve the literal value of every character within them | met | `quote/single`, `quote/c_single_all` |  |
| 2.2.3/1 | Within double quotes $ keeps its meaning for parameter, command and arithmetic expansion | met | `quote/double`, `quote/c_dq_dollar` |  |
| 2.2.3/2 | Within double quotes $' does not introduce dollar-single-quotes | met | `quote/c_dq_no_dollar_single` |  |
| 2.2.3/3 | Characters between "$(" and its matching ")" inside double quotes are not affected by the double quotes | met | `quote/c_dq_cmdsub_inner_quotes` |  |
| 2.2.3/4 | Inside double quotes, in ${x#pattern} forms the outer double quotes do not quote the pattern's special characters | met | `param/trim_quoted`, `quote/c_dq_trim_pattern` |  |
| 2.2.3/5 | Inside double quotes, in ${x:-word} forms the word keeps literal value except for " ` $ and backslash; backslash also escapes } | met | `quote/dq_in_param`, `quote/c_dq_default_word` |  |
| 2.2.3/6 | Inside double quotes a backquote introduces command substitution, ended by the next unescaped backquote | met | `quote/c_dq_backquote` |  |
| 2.2.3/7 | Inside double quotes backslash is an escape only before $ ` " backslash and newline | met | `quote/special_chars`, `quote/c_dq_backslash` |  |
| 2.2.3/8 | The literal value of the result of an expansion in double quotes is preserved (no splitting, no globbing) | met | `split/quoted`, `quote/c_dq_result_literal` |  |
| 2.2.4/1 | $'...' preserves characters literally up to the terminating unescaped single quote | met | `quote/dollar_single`, `quote/c_ds_plain` | POSIX.1-2024 requires them; recorded with bash --posix as the oracle, and dash 0.5.13.4 agrees on every case (sh17 measured that it has them) |
| 2.2.4/2 | $'...' escapes \" \' \\ \a \b \e \f \n \r \t \v yield their characters | met | `quote/c_ds_escapes`, `quote/ds_more_escapes` |  |
| 2.2.4/3 | $'\cX' yields the control character for X | met | `quote/c_ds_control` |  |
| 2.2.4/4 | $'\xXX' yields the byte with that hexadecimal value, ended by the first non-hex character | met | `quote/c_ds_hex` |  |
| 2.2.4/5 | $'\ddd' yields the byte with that octal value, one to three digits | met | `quote/c_ds_octal` |  |
| 2.2.4/6 | An escaped single quote does not end a $'...' sequence, and the sequence joins with adjacent word parts | met | `quote/c_ds_embedded` |  |
| 2.2.4/7 | $'...' escapes are processed before word expansion: the result is quoted (not split, not globbed) | met | `quote/c_ds_quoted`, `quote/ds_contexts` |  |

### 2.3 Token recognition and aliases

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| 2.3/1 | Operators are formed greedily from unquoted characters (&& \|\| ;; ;& << >> <& >& <> <<- >\|) | met | `parse/redirs_ok`, `parse/compound_ok`, `parse/c_operators_adjacent` |  |
| 2.3/2 | A quote does not delimit a token: adjacent quoted and unquoted parts form one word | met | `quote/mixed`, `parse/c_quotes_join` |  |
| 2.3/3 | An unquoted blank delimits a token and is discarded | met | `parse/c_blanks` |  |
| 2.3/4 | A # at the start of a word begins a comment up to but excluding the newline; inside a word it is literal | met | `parse/comments_ok`, `parse/c_comment_word` |  |
| 2.3/5 | Expansions nested in a word are found recursively and included unmodified in the token | met | `parse/cmdsub_nested_ok`, `cmdsub/nested`, `parse/c_nested_units` |  |
| 2.3/6 | A here-document body starts after the next newline token; tokens after the operator on the same line are kept | met | `parse/heredoc_ok`, `redir/heredoc`, `parse/c_heredoc_rest_of_line` |  |
| 2.3/7 | Each complete command is executed before the next is tokenized and parsed | met | `parse/c_exec_before_parse`, `parse/c_exec_before_parse_cd` |  |
| 2.3/8 | The token at end of input is delimited (a last line with no newline runs) | met | `parse/c_no_final_newline` |  |
| 2.3.1/1 | An unquoted command-name token that names an alias is replaced by the alias value | met | `alias/c_basic`, `alias/command_position` | dash and bash --posix agree; alias takes effect for the next complete command |
| 2.3.1/2 | A token with any quoting character is not subject to alias substitution | met | `alias/c_quoted_not` |  |
| 2.3.1/3 | Only a token in command-name position is substituted, not an argument | met | `alias/c_position` |  |
| 2.3.1/4 | An alias is not expanded again inside its own expansion (no recursion on the same name) | met | `alias/c_no_self_recursion`, `alias/recursion_more` |  |
| 2.3.1/5 | An alias value ending in a blank makes the next token subject to alias substitution | met | `alias/c_trailing_blank`, `alias/trailing_more` |  |
| 2.3.1/6 | The alias value is tokenized as input: it may hold several tokens, operators and reserved words | met | `alias/c_value_tokens`, `alias/value_text`, `alias/reserved_words` |  |
| 2.3.1/7 | A change to an alias takes effect no later than the end of the complete command that made it | met | `alias/c_takes_effect_next` |  |
| 2.3.1/8 | Aliases are not inherited by a separately invoked shell | met | `alias/c_not_inherited` |  |
| 2.3.1/10 | At the prompt an alias defined on one line is in effect on the next | met | `session:c_alias_interactive` |  |
| 2.3.1/9 | Aliases are part of the environment a subshell duplicates | met | `alias/c_subshell`, `alias/scope` |  |

### 2.4 Reserved words

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| 2.4/1 | Reserved words are recognized only unquoted and in command position | met | `parse/compound_ok`, `parse/c_reserved_quoted` |  |
| 2.4/2 | Reserved words are recognized after another reserved word (if/then/else/do/{/!) | met | `parse/c_reserved_after_reserved` |  |
| 2.4/3 | In is the only reserved word recognized as the third word of case and for | met | `parse/c_in_third_word` |  |
| 2.4/4 | A word ending in a colon in command position is a plain command name when it is not otherwise special | not counted | `parse/c_colon_word` | results are unspecified by POSIX; recorded because dash and bash agree |

### 2.5 Parameters and variables

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| 2.5/1 | A set parameter may be null, and a variable once set stays set until unset | met | `param/unset_var`, `param/c_set_null` |  |
| 2.5.1/1 | Positional parameter digits are read as decimal even with a leading zero; more than one digit needs braces | met | `param/ten`, `param/positional`, `param/c_positional_digits` |  |
| 2.5.2/1 | "$@" produces one field per positional parameter, joined to the surrounding word at each end | met | `param/at_in_word`, `param/at_star`, `param/c_at_fields` |  |
| 2.5.2/2 | "$@" with no positional parameters produces zero fields | met | `param/at_empty`, `param/c_at_zero` |  |
| 2.5.2/3 | Unquoted $@ and $* produce the parameters, each then split into fields | met | `param/c_at_unquoted` |  |
| 2.5.2/4 | "$*" joins the parameters with the first character of IFS, a space if IFS is unset, nothing if IFS is null | met | `param/ifs_star`, `param/c_star_join` |  |
| 2.5.2/5 | $* in an assignment or other non-splitting context joins as "$*" does | met | `param/c_star_assign` |  |
| 2.5.2/6 | "$@" inside ${x:-"$@"} keeps separate fields | met | `param/c_at_in_default` |  |
| 2.5.2/7 | $# is the decimal count of positional parameters, not counting $0 | met | `param/positional`, `param/c_hash` |  |
| 2.5.2/8 | $? is the exit status of the most recent pipeline, and is 0 at start | met | `param/status`, `param/c_status` |  |
| 2.5.2/9 | A subshell starts with the invoking shell's $? | met | `param/c_status_into_subshell` |  |
| 2.5.2/10 | x=$(cmd) leaves the command substitution's status in $? | met | `simple/assign_status`, `param/c_status_assign_cmdsub` |  |
| 2.5.2/11 | $- holds the current single-letter option flags | met | `option/dollar_dash`, `param/c_dash_flags` |  |
| 2.5.2/12 | $$ is the process ID of the invoked shell, the same value in a subshell | met | `param/pid`, `param/c_pid_subshell`, `param/pid_everywhere` |  |
| 2.5.2/13 | $$ is the shell's real process ID (what its child sees as its parent) | met | `param/c_pid_is_real` |  |
| 2.5.2/14 | $! is the process ID of the most recent asynchronous list | met | `jobs/bang`, `signal/bang_is_a_process`, `param/c_bang` |  |
| 2.5.2/15 | $0 is the script's name as given; in a function it is unchanged | met | `exec/argv0`, `param/c_zero` |  |
| 2.5.3/1 | Variables are initialized from the environment and marked for export at once | met | `env/reexport`, `env/c_init_exported`, `param/c_ps_from_env` |  |
| 2.5.3/2 | Environment entries whose names are not valid names do not become shell variables | met | `env/c_invalid_names` |  |
| 2.5.3/3 | ENV is parameter-expanded and the file it names is run before an interactive shell reads commands | met | `session:env_file`, `session:env_missing` |  |
| 2.5.3/4 | ENV is not read by a non-interactive shell | met | `env/c_env_not_read` |  |
| 2.5.3/5 | IFS is set to space, tab, newline when the shell is invoked, whatever the environment held | met | `env/c_ifs_reset` |  |
| 2.5.3/6 | With IFS unset, splitting and read behave as if it were space, tab, newline | met | `split/unset_ifs`, `split/c_unset_ifs_read` |  |
| 2.5.3/7 | LINENO is the current line number within the script or function | met | `param/lineno`, `param/c_lineno` | dash 0.5.13.4 counts from the function's first line inside a function; bash --posix and pelt count lines of the script. The standard's words allow either; the script's line is what a diagnostic needs, so bash is the oracle |
| 2.5.3/8 | PPID is the parent's process ID, the same in a subshell | met | `env/c_ppid`, `env/ppid_variable` |  |
| 2.5.3/9 | PS1 is parameter-expanded and written to standard error before each command is read; default "$ " | met | `session:echo_hi`, `session:ps1_param` |  |
| 2.5.3/10 | In PS1 each ! is replaced by the history number of the next command, and !! by one ! | met | `session:c_ps1_bang`, `session:c_ps1_bang_number` |  |
| 2.5.3/11 | PS2 is expanded and written to standard error when a command continues onto another line; default "> " | met | `session:ps2_if` |  |
| 2.5.3/12 | PS4 is parameter-expanded and written before each line of a set -x trace; default "+ " | pending (ps4-expansion) | `option/xtrace`, `option/c_ps4` |  |
| 2.5.3/13 | PWD is set from the environment when that is an absolute pathname of the current directory with no dot components | pending (pwd-from-env) | `cd/c_pwd_from_env` |  |
| 2.5.3/14 | HOME is used by tilde expansion | met | `tilde/home` |  |
| 2.5.3/15 | LANG, LC_ALL, LC_COLLATE, LC_CTYPE, LC_MESSAGES select the locale for patterns, characters and messages | untestable |  | needs a non-C locale present on every CI host; measured by hand on kasumi (docs/CENSUS.md, locale rows) |
| 2.5.3/16 | The shell processes values as characters where the standard speaks of characters (${#x} counts characters) | met | `param/c_length_bytes_in_c` | the corpus runs in the C locale, where a character is a byte; the UTF-8 answer is measured by hand (docs/CENSUS.md, locale rows) |

### 2.6 Word expansions

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| 2.6/1 | Tilde, parameter, command and arithmetic expansion happen first, beginning to end; then field splitting, pathname expansion, quote removal | met | `param/c_expansion_order` |  |
| 2.6/2 | Expansions within one word give one field unless split, globbed or "$@" | met | `split/c_one_field` |  |
| 2.6/3 | A $ followed by a blank, newline or end of word is literal | met | `param/dollar_alone`, `param/c_dollar_literal` |  |
| 2.6/4 | Results of expansion are not rescanned for further expansion | met | `param/c_no_rescan` |  |
| 2.6.1/1 | A leading unquoted ~ up to the first slash is a tilde-prefix; alone it is replaced by HOME | met | `tilde/home`, `tilde/middle`, `tilde/c_basic` |  |
| 2.6.1/2 | In an assignment a tilde-prefix is recognized after = and after each unquoted colon | met | `tilde/assign`, `tilde/c_assign_colon` |  |
| 2.6.1/3 | Tilde in a word that is not an assignment is expanded only at the start of the word | met | `tilde/c_not_assign` |  |
| 2.6.1/4 | The tilde replacement is not split or globbed, and a null HOME gives one empty field | met | `tilde/c_quoted_result` |  |
| 2.6.1/5 | ~login is replaced by that user's home directory from the user database | pending (user database) | `tilde/user`, `tilde/c_user_root` |  |
| 2.6.1/6 | Tilde expansion applies to the word after a redirection operator and to case words and patterns | met | `tilde/c_redirect_case` |  |
| 2.6.1/7 | A quoted character in the tilde-prefix prevents tilde expansion | met | `tilde/c_quoted_prefix` |  |
| 2.6.2/1 | ${parameter} substitutes the value; braces delimit the name | met | `param/simple`, `param/concat`, `param/c_braces` |  |
| 2.6.2/2 | An unbraced name uses the longest valid name | met | `param/underscore_names`, `param/c_longest_name` |  |
| 2.6.2/3 | The matching } skips quoted strings, escaped braces and embedded expansions | met | `param/nested`, `param/c_matching_brace` |  |
| 2.6.2/4 | ${x:-word} substitutes word when x is unset or null; ${x-word} only when unset | met | `param/default`, `param/c_use_default` |  |
| 2.6.2/5 | ${x:=word} assigns word when x is unset or null and substitutes the final value; ${x=word} only when unset | met | `param/assign`, `param/c_assign_default` |  |
| 2.6.2/6 | ${N:=word} on a positional or special parameter is an error | met | `param/assign_positional_error` |  |
| 2.6.2/7 | ${x:?word} writes word to standard error and a non-interactive shell exits non-zero when x is unset or null | met | `param/error_unset`, `param/error_null`, `param/c_error_exit` |  |
| 2.6.2/8 | ${x:+word} substitutes word when x is set and not null; ${x+word} when set | met | `param/alternative`, `param/c_alternative` |  |
| 2.6.2/9 | The word is expanded only when it is needed | met | `param/c_word_lazy` |  |
| 2.6.2/10 | The word undergoes tilde, parameter, command and arithmetic expansion | met | `param/c_word_expanded` |  |
| 2.6.2/11 | An unquoted ${x:-word} result is split into fields, with quoted parts of word kept together | met | `param/default_split`, `param/c_default_fields` |  |
| 2.6.2/12 | ${#x} is the length of the value in characters | met | `param/length`, `param/c_length` |  |
| 2.6.2/13 | ${#x} of an unset parameter fails under set -u | met | `param/c_length_nounset` |  |
| 2.6.2/14 | ${x%pattern} removes the smallest matching suffix and ${x%%pattern} the largest | met | `param/trim_suffix`, `param/c_trim_suffix` |  |
| 2.6.2/15 | ${x#pattern} removes the smallest matching prefix and ${x##pattern} the largest | met | `param/trim_prefix`, `param/c_trim_prefix` |  |
| 2.6.2/16 | Quoting characters within the braces makes pattern characters literal | met | `param/trim_quoted`, `param/c_trim_literal` |  |
| 2.6.2/17 | The pattern word is itself expanded (variables, command substitution) before matching | met | `param/trim_var_pattern`, `param/c_trim_expanded_pattern` |  |
| 2.6.2/18 | Trim forms of an unset parameter fail under set -u | met | `param/c_trim_nounset` |  |
| 2.6.2/19 | A bad substitution operator is an expansion error: a non-interactive shell exits | met | `param/bad_substitution` |  |
| 2.6.2/20 | Parameter expansion applies to special parameters ($?, $#, $-, $!, $0, $$) in the modifier forms | met | `param/c_special_modifiers` |  |
| 2.6.3/1 | $(commands) runs in a subshell and is replaced by its standard output | met | `cmdsub/basic`, `cmdsub/isolation`, `cmdsub/external`, `cmdsub/c_subshell_env` |  |
| 2.6.3/2 | Trailing newlines of the output are removed, all of them; others are kept | met | `cmdsub/trailing_newlines`, `cmdsub/program_newlines`, `cmdsub/c_newlines` |  |
| 2.6.3/3 | Unquoted command substitution output is split and globbed; quoted is not | met | `cmdsub/in_dquotes`, `cmdsub/c_split_glob` |  |
| 2.6.3/4 | In `...` a backslash is literal except before $ ` and backslash | met | `cmdsub/backquote`, `cmdsub/program_backquote`, `cmdsub/c_backquote_backslash` |  |
| 2.6.3/5 | Backquotes nest by escaping the inner ones | met | `cmdsub/c_backquote_nested` |  |
| 2.6.3/6 | $(...) may hold any program: quotes, comments, case with unbalanced ), here-documents | met | `cmdsub/case_inside`, `cmdsub/c_any_program` |  |
| 2.6.3/7 | The result of a command substitution is not expanded again | met | `cmdsub/c_not_rescanned` |  |
| 2.6.3/8 | $(( is arithmetic when it parses as such; $( ( starts a subshell in a command substitution | met | `cmdsub/c_arith_ambiguity` |  |
| 2.6.3/9 | The exit status of the last command substitution is the status of a command with no name | met | `cmdsub/status`, `cmdsub/program_status` |  |
| 2.6.3/10 | An exit in a command substitution ends only the substitution | met | `cmdsub/exit_inside` |  |
| 2.6.3/11 | A command substitution's commands see standard input and standard error of the shell | met | `cmdsub/program_stderr`, `cmdsub/c_stdin_inherited` |  |
| 2.6.4/1 | $((expression)) is replaced by the value of the expression | met | `arith/basic` |  |
| 2.6.4/2 | The expression is treated as if double-quoted: parameter expansion and command substitution apply, and a double quote is not special | met | `arith/variables`, `arith/nested`, `arith/c_expand_first` |  |
| 2.6.4/3 | Decimal, octal (leading 0) and hexadecimal (0x) constants are recognized | met | `arith/hex_octal`, `arith/c_constants` |  |
| 2.6.4/4 | The C operators apply with C precedence: unary + - ~ !, * / %, + -, << >>, relational, equality, & ^ \|, && \|\|, ?:, assignment | met | `arith/precedence`, `arith/unary`, `arith/shifts_bits`, `arith/logical`, `arith/compare`, `arith/ternary`, `arith/short_circuit`, `arith/c_operators` |  |
| 2.6.4/5 | Assignment operators change the variable, and the change is in effect after the expansion | met | `arith/assign_ops`, `arith/assign_var`, `arith/c_assign` |  |
| 2.6.4/6 | A variable name in an expression is read as its value: $((x)) equals $(($x)) for an integer value, signs included | met | `arith/c_variable_value` |  |
| 2.6.4/7 | Arithmetic is signed long, at least; wrap-around does not stop the shell | met | `arith/overflow`, `arith/c_long` |  |
| 2.6.4/8 | An invalid expression fails with a diagnostic; a non-interactive shell exits | met | `arith/syntax_error`, `arith/illegal_value`, `arith/divzero`, `arith/c_invalid` |  |
| 2.6.4/9 | White space and newlines are allowed in an expression | met | `arith/spaces_newlines` |  |
| 2.6.4/10 | An arithmetic expansion's result is subject to field splitting when unquoted | met | `split/ifs_digits`, `arith/c_result_split` |  |
| 2.6.4/11 | A variable whose value is itself an expression or name is evaluated (extension recorded: dash refuses, bash recurses) | not counted | `arith/c_value_not_constant` | not required by POSIX (only integer-constant values are); recorded from dash |
| 2.6.4/12 | Comma is not required; ++ and -- are not required (recorded from dash) | not counted | `arith/c_incr_optional` | optional operators; dash refuses ++x as written (reads +(+x)), bash implements them |
| 2.6.5/1 | Fields from expansions not in double quotes are split at IFS characters | met | `split/default`, `split/literal_not_split`, `split/c_basic` |  |
| 2.6.5/2 | With IFS null no splitting occurs, and an expansion that is wholly empty is removed | met | `split/empty_ifs`, `split/empty_unquoted`, `split/c_null_ifs` |  |
| 2.6.5/3 | IFS white space at the start and end of an expansion is ignored, and runs of it delimit once | met | `split/c_whitespace_runs` |  |
| 2.6.5/4 | Each non-white-space IFS character delimits a field; adjacent ones give empty fields | met | `split/colon`, `split/leading_colon`, `split/c_nonwhite` |  |
| 2.6.5/5 | A non-white-space IFS character with adjacent IFS white space is one delimiter | met | `split/mixed_ifs`, `split/c_mixed` |  |
| 2.6.5/6 | A trailing non-white-space IFS delimiter does not produce a trailing empty field | met | `split/c_trailing_delim` |  |
| 2.6.5/7 | An expansion that is empty or all IFS white space produces zero fields | met | `split/c_zero_fields` |  |
| 2.6.5/8 | Only the parts of a word that came from an expansion are split; literal parts join their neighbours | met | `split/joined_word`, `split/c_literal_parts` |  |
| 2.6.5/9 | Splitting applies to command substitution and arithmetic results as to parameters | met | `split/cmdsub` |  |
| 2.6.5/10 | IFS is used at the time of the split, including an assignment earlier in the same list | met | `split/c_ifs_changes` |  |
| 2.6.5/11 | Assignment values and case words are not split | met | `split/c_not_in_assign` |  |
| 2.6.6/1 | After splitting, each field with unquoted pattern characters is matched against file names unless set -f | met | `glob/star`, `glob/noglob`, `option/noglob` |  |
| 2.6.6/2 | A pattern produced by an expansion is used for pathname expansion | met | `glob/edge_var`, `glob/c_from_expansion` |  |
| 2.6.7/1 | Quote characters present in the original word are removed unless themselves quoted | met | `quote/mixed`, `quote/empty_args`, `quote/c_removal` |  |
| 2.6.7/2 | Quote characters that result from an expansion are not removed | met | `quote/c_removal_not_expanded` |  |

### 2.7 Redirection

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| 2.7/1 | [n]redir-op word: the number must immediately precede the operator; a quoted number or operator is not a redirection | met | `redir/redirect_out`, `redir/redirect_err`, `redir/c_number_forms` |  |
| 2.7/2 | The redirection is removed from the arguments wherever it appears in the command | met | `redir/c_anywhere` |  |
| 2.7/3 | File descriptors 0 through 9 can be used | met | `redir/exec_fd`, `exec/redirect_fd3`, `redir/c_fd_range` |  |
| 2.7/4 | The target word undergoes tilde, parameter, command and arithmetic expansion and quote removal | met | `redir/target_expansion`, `redir/c_target_expansions` |  |
| 2.7/5 | A non-interactive shell does not apply pathname expansion to the target word | met | `redir/c_target_no_glob` |  |
| 2.7/6 | A target word that splits into several fields is not split (recorded from dash) | met | `redir/c_target_not_split` | POSIX names no field splitting for the redirection word; dash and pelt take it as one word, bash --posix refuses it as ambiguous |
| 2.7/7 | Several redirections on one command are evaluated in order from beginning to end | met | `redir/order_matters`, `redir/dup_err_to_out`, `redir/c_order` |  |
| 2.7/8 | A failure to open or create the file makes the redirection fail and the command is not run | met | `redir/fail_status`, `redir/c_open_fails` |  |
| 2.7.1/1 | [n]<word opens the file for reading on descriptor n, default 0 | met | `redir/in_file`, `redir/read_fd`, `redir/c_in_fd` |  |
| 2.7.2/1 | [n]>word creates or truncates the file for writing on descriptor n, default 1 | met | `redir/out_trunc`, `redir/redirect_out`, `redir/c_out_trunc` |  |
| 2.7.2/2 | With set -C, > fails on an existing regular file and >\| overrides it | met | `redir/noclobber`, `redir/c_noclobber` |  |
| 2.7.3/1 | [n]>>word opens for append, creating the file if needed | met | `redir/append`, `redir/c_append` |  |
| 2.7.4/1 | A here-document runs to a line holding only the delimiter | met | `redir/heredoc`, `redir/c_heredoc_delimiter` |  |
| 2.7.4/2 | With an unquoted delimiter the body undergoes parameter, command and arithmetic expansion | met | `redir/heredoc_expand`, `redir/c_heredoc_expansions` |  |
| 2.7.4/3 | With any part of the delimiter quoted, the body is not expanded and the delimiter is the word after quote removal | met | `redir/heredoc_quoted`, `redir/c_heredoc_quoted_forms` |  |
| 2.7.4/4 | In an expanding here-document backslash acts as inside double quotes, and a double quote is literal | met | `redir/c_heredoc_backslash` |  |
| 2.7.4/5 | <<- strips leading tabs from body lines and the delimiter line | met | `redir/heredoc_strip`, `redir/c_heredoc_tabs` |  |
| 2.7.4/6 | Several here-documents on one line are read in order | met | `redir/heredoc_two`, `parse/two_heredocs_ok`, `redir/c_heredoc_order` |  |
| 2.7.4/7 | A here-document for a command that is not executed is read without being expanded | met | `redir/c_heredoc_skipped` |  |
| 2.7.4/8 | A here-document can feed any descriptor ([n]<<) and any command, compound commands and functions included | met | `redir/heredoc_function`, `redir/heredoc_read`, `redir/heredoc_large`, `redir/c_heredoc_fd` |  |
| 2.7.4/9 | The end of a -c command string ends an unterminated here-document's search as a newline would | met | `redir/c_heredoc_end_of_string` |  |
| 2.7.4/10 | A here-document inside a command substitution, and a command substitution inside a here-document | met | `redir/c_heredoc_in_cmdsub` |  |
| 2.7.5/1 | [n]<&m makes n a copy of m; [n]<&- closes n; closing a closed descriptor is not an error | met | `redir/read_fd`, `redir/c_dup_in` |  |
| 2.7.5/2 | Duplicating from a descriptor that is not open is a redirection error | met | `redir/bad_fd`, `redir/c_dup_bad` |  |
| 2.7.6/1 | [n]>&m makes n a copy of m; [n]>&- closes n | met | `redir/dup_err_to_out`, `redir/close_out`, `redir/c_dup_out` |  |
| 2.7.6/2 | The word after <& or >& is expanded: digits or - from a variable work | met | `redir/c_dup_expanded` |  |
| 2.7.7/1 | [n]<>word opens for reading and writing on n (default 0), creating the file, not truncating it | met | `redir/readwrite`, `redir/c_readwrite` |  |

### 2.8 Exit status and errors

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| 2.8.1/1 | A syntax error makes a non-interactive shell exit with a diagnostic and a non-zero status | met | `parse/fi_unexpected`, `option/bad_option`, `stdin/syntax_error_ends`, `parse/c_syntax_error_exits` |  |
| 2.8.1/2 | A syntax error found later in a script does not stop commands already executed | met | `parse/c_syntax_error_late` |  |
| 2.8.1/3 | An error in a special built-in run directly makes a non-interactive shell exit | met | `builtin/shift_error`, `redir/special_fail_exits`, `builtin/c_special_error_exits` |  |
| 2.8.1/4 | A special built-in error under the command utility does not make the shell exit | pending (command-special) | `builtin/command_bypass`, `builtin/c_special_error_command` |  |
| 2.8.1/5 | An error in another utility does not make the shell exit | met | `builtin/c_regular_error_continues` |  |
| 2.8.1/6 | A redirection error with a special built-in makes a non-interactive shell exit | met | `redir/special_fail_exits`, `redir/c_special_redirect_error` |  |
| 2.8.1/7 | A redirection error with a compound command, a function or another utility does not make the shell exit | met | `redir/fail_status`, `exec/redirect_fails`, `redir/c_other_redirect_error` |  |
| 2.8.1/8 | A variable assignment error (assigning a readonly variable) makes a non-interactive shell exit | met | `builtin/readonly_error`, `simple/readonly_assign`, `simple/c_assign_error_exits` |  |
| 2.8.1/9 | An expansion error makes a non-interactive shell exit | met | `param/bad_substitution`, `param/error_unset`, `param/c_expansion_error_exits` |  |
| 2.8.1/10 | Command not found gives a diagnostic and status 127, and the shell goes on | met | `simple/not_found`, `exec/not_found_bare`, `simple/c_not_found_continues` |  |
| 2.8.1/11 | A shall-exit error in a subshell ends the subshell with a non-zero status and the invoking shell continues | met | `parse/c_error_in_subshell` |  |
| 2.8.1/12 | An interactive shell does not exit on any of these errors, and drops the rest of the command | met | `session:syntax_error_continues`, `session:special_builtin_error`, `session:expansion_error`, `session:c_redirect_error`, `session:readonly_assign` |  |
| 2.8.1/13 | A special built-in's own diagnostic goes to standard error and can be redirected like a utility's | met | `builtin/c_special_diag_redirect` |  |
| 2.8.1/14 | An unrecoverable read error while reading commands makes the shell exit 128 after any EXIT trap | untestable |  | needs a descriptor that fails mid-read (EIO); no portable way to make one in the corpus |
| 2.8.2/1 | Not found is 127; found but not executable is 126 | met | `exec/not_found`, `exec/not_executable`, `exec/directory`, `simple/slash_not_found`, `simple/c_126_127` |  |
| 2.8.2/2 | A command ended by a signal has a status above 128 that identifies the signal | met | `signal/child_term`, `signal/child_kill`, `signal/child_hup`, `signal/child_int` |  |
| 2.8.2/3 | Otherwise the status is the low eight bits of what the command exited with | met | `simple/c_exit_mod_256` |  |

### 2.9 Shell commands

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| 2.9/1 | The exit status of a command is that of the last simple command it executed, unless stated otherwise | met | `control/loop_status`, `control/if_status` |  |
| 2.9.1.1/1 | The command name is the first field left after expanding the non-assignment words; empty expansions are passed over | met | `simple/command_name_from_var`, `simple/empty_command`, `simple/c_name_after_empty` |  |
| 2.9.1.1/2 | After export and readonly, words that look like assignments are expanded as assignments: no splitting, tilde after = and : | met | `simple/c_declaration_utility`, `simple/declaration_forms` | POSIX.1-2024 requires assignment context; bash --posix is the oracle. sh06 wrote that dash 0.5.13.4 splits the value: it does not (black-box, sh07: `export e=$y` keeps `p q`, and the case records dash=agree) |
| 2.9.1.1/3 | For other commands, name=value arguments are ordinary words: split, and tilde only at the start | met | `simple/c_not_declaration` |  |
| 2.9.1.1/4 | Redirections are performed, then assignments are expanded and made | met | `simple/assign_expansion`, `simple/c_assign_expansions` |  |
| 2.9.1.2/1 | With no command name, assignments affect the current environment | met | `simple/assign_only`, `simple/c_assign_current` |  |
| 2.9.1.2/2 | Assignments before a utility are exported to it and do not affect the current environment | met | `env/temp_assign_gone`, `simple/external_env`, `exec/assign_reaches`, `simple/c_assign_temp`, `simple/assign_order_program` |  |
| 2.9.1.2/3 | Assignments before a special built-in stay in effect after it completes | met | `simple/persist_special`, `simple/c_assign_special_persists` |  |
| 2.9.1.2/4 | Assignments before a function call are in effect during the function | met | `func/temp_assign`, `simple/c_assign_function` |  |
| 2.9.1.2/5 | Assignments before a regular built-in do not persist | met | `simple/temp_builtin`, `env/temp_assign_back`, `simple/c_assign_regular_builtin` |  |
| 2.9.1.2/6 | Assigning a readonly variable before any command is a variable assignment error | met | `simple/readonly_assign` |  |
| 2.9.1.3/1 | A command with only redirections performs them in a subshell: files are created, the shell's descriptors unchanged | met | `redir/redir_only`, `simple/c_redirect_only` |  |
| 2.9.1.3/2 | With no command name the status is that of the last command substitution, else zero | met | `simple/assign_status`, `simple/c_status_no_name` |  |
| 2.9.1.4/1 | Search order without a slash: special built-in, function, other built-in, then PATH | met | `func/name_shadows_builtin`, `simple/c_search_order` |  |
| 2.9.1.4/2 | A function cannot shadow a special built-in | not counted | `simple/c_special_not_shadowed` | defining a function named after a special built-in is an error in dash and in bash --posix |
| 2.9.1.4/3 | PATH is searched in order, and only executable files are taken | met | `simple/path_search`, `exec/path_assign_search`, `simple/c_path_order` |  |
| 2.9.1.4/4 | After PATH is assigned, a remembered location is not used | met | `simple/c_path_rehash` |  |
| 2.9.1.4/5 | An empty PATH component or an unset PATH names the current directory or the default | met | `simple/c_path_empty_component` |  |
| 2.9.1.4/6 | A name with a slash is executed directly, without a PATH search | met | `simple/slash_not_found`, `simple/c_slash_direct` |  |
| 2.9.1.6/1 | The utility is run with arg0 the command name and the arguments as given | met | `simple/external_args`, `simple/c_arg0` |  |
| 2.9.1.6/2 | A file the system refuses with ENOEXEC is run as a shell script by the shell | met | `exec/script_no_shebang`, `simple/script_no_shebang`, `simple/c_enoexec` |  |
| 2.9.1.6/3 | A file that cannot be a script (a NUL before a newline) is refused with status 126 | pending (enoexec) | `simple/c_enoexec_binary` |  |
| 2.9.2/1 | Each command's standard output is connected to the next command's standard input | met | `pipe/three`, `pipe/many_stages`, `pipe/stdin_through` |  |
| 2.9.2/2 | The pipe is assigned before the command's own redirections | met | `pipe/c_redirect_overrides` |  |
| 2.9.2/3 | The pipeline's status is the last command's | met | `pipe/status_last`, `pipe/pipeline_status`, `pipe/c_status_last` |  |
| 2.9.2/4 | ! inverts the status of the pipeline | met | `pipe/negation`, `control/not`, `pipe/c_bang` |  |
| 2.9.2/5 | With set -o pipefail the status is the last non-zero status in the pipeline, zero if all succeed | met | `pipe/c_pipefail`, `pipe/pipefail_rightmost`, `pipe/pipefail_programs`, `pipe/pipefail_compound` | new in POSIX.1-2024; dash 0.5.13.4 has `set -o pipefail` (sh17 measured), recorded from it |
| 2.9.2/6 | The pipefail setting used is the one in effect when the pipeline starts | met | `pipe/c_pipefail_at_start` |  |
| 2.9.2/7 | Each command of a multi-command pipeline runs in a subshell environment (or the current one, as an extension, for some) | met | `pipe/stage_is_subshell`, `pipe/cd_in_stage`, `pipe/exit_in_stage`, `pipe/c_stage_environment` |  |
| 2.9.2/8 | The shell waits for the last command of a foreground pipeline; stages run concurrently | met | `pipe/sigpipe_producer`, `pipe/large_in_process`, `pipe/c_concurrent_stages` |  |
| 2.9.2/9 | A reader that exits early ends a producer written in the shell itself (SIGPIPE or EPIPE) | met | `pipe/c_shell_producer_ends`, `signal/c_trap_ignore_pipe`, `pipe/endless_producer` |  |
| 2.9.2/10 | A pipeline stage that is a compound command or function reads the previous stage as it arrives | met | `pipe/compound_stage`, `pipe/function_stage`, `pipe/builtin_to_program`, `pipe/program_to_builtin`, `pipe/c_incremental_reader` |  |
| 2.9.3/1 | && and \|\| have equal precedence and associate left | met | `control/and_or`, `control/c_andor_assoc` |  |
| 2.9.3/2 | ; and newline run lists in sequence; & runs the list asynchronously | met | `control/async_list`, `jobs/background`, `control/c_separators` |  |
| 2.9.3.1/1 | The shell does not wait for an asynchronous list; its status is zero | met | `jobs/background`, `jobs/two`, `jobs/c_async_status` |  |
| 2.9.3.1/2 | Without job control an asynchronous list's standard input is /dev/null unless redirected | met | `jobs/stdin_null`, `jobs/c_async_stdin` |  |
| 2.9.3.1/3 | An asynchronous list runs in a subshell: its assignments and cd do not affect the shell | met | `jobs/c_async_subshell` |  |
| 2.9.3.1/4 | The shell does not wait for background children before exiting | met | `jobs/c_exit_no_wait` |  |
| 2.9.3.1/5 | The whole AND-OR list is run in the background, not only its last pipeline | met | `jobs/c_async_andor` |  |
| 2.9.3.3/1 | The second command of an AND list is expanded and run only if the first succeeds | met | `control/c_and_lazy` |  |
| 2.9.3.4/1 | The second command of an OR list runs only if the first fails; status is the last command run | met | `control/c_or_lazy` |  |
| 2.9.4/1 | A redirection on a compound command applies to every command in it that does not override it | met | `redir/compound_out`, `redir/while_in`, `redir/exec_in_group`, `control/c_compound_redirect` |  |
| 2.9.4.1/1 | ( list ) runs in a subshell: assignments, cd, options, functions and traps set there do not remain | met | `control/subshell`, `cd/cd_subshell`, `cd/subshell_restores`, `env/subshell_export`, `env/subshell_unset`, `control/c_subshell_isolation` |  |
| 2.9.4.1/2 | { list; } runs in the current environment | met | `control/brace_group`, `control/c_brace_current` |  |
| 2.9.4.1/3 | The status of a grouping command is the status of its list | met | `control/c_group_status` |  |
| 2.9.4.2/1 | for runs the list once per item of the expanded words, setting the variable; it remains set afterwards | met | `control/for_in`, `control/for_var_after`, `control/c_for_words` |  |
| 2.9.4.2/2 | for without in iterates over "$@"; with an empty in list it runs nothing and returns zero | met | `control/for_positional`, `control/for_empty`, `control/c_for_forms` |  |
| 2.9.4.2/3 | for's status is that of the last list run | met | `control/c_for_status` |  |
| 2.9.4.3/1 | case runs the list of the first pattern that matches the expanded word; later patterns are not expanded | met | `control/case_basic`, `control/case_multi`, `control/c_case_first_match` |  |
| 2.9.4.3/2 | The case word undergoes tilde, parameter, command, arithmetic expansion and quote removal, but no splitting or globbing | met | `control/c_case_word` |  |
| 2.9.4.3/3 | Patterns are expanded; quoted parts of a pattern match literally | met | `control/case_quoted_pattern`, `control/c_case_pattern_quoting` |  |
| 2.9.4.3/4 | An optional ( may precede the pattern list, and \| separates patterns | met | `control/c_case_syntax` |  |
| 2.9.4.3/5 | ;& falls through to the next clause's list without testing its pattern | met | `control/case_fallthrough`, `control/c_case_fallthrough_chain` | new in POSIX.1-2024; dash 0.5.13.4 has no ;&, so bash --posix is the oracle |
| 2.9.4.3/5b | The last clause of a case may itself end with ;& | met | `control/c_case_fallthrough_last` | dash 0.5.13.4 refuses ;& before esac as a syntax error; the grammar allows it, so bash --posix is the oracle |
| 2.9.4.3/6 | case's status is zero when nothing matches, else the status of the last list run; an empty list gives zero | met | `control/case_status`, `control/c_case_status_forms` |  |
| 2.9.4.4/1 | if runs the then list when the condition list succeeds, else each elif in turn, else the else list | met | `control/if_elif_else`, `control/c_if_chain` |  |
| 2.9.4.4/2 | if's status is that of the list run, or zero if none ran | met | `control/if_status`, `control/c_if_status_none` |  |
| 2.9.4.4/3 | The condition's status is visible in $? at the start of the then or else list | met | `control/c_if_status_visible` |  |
| 2.9.4.5/1 | while repeats its body while the condition list succeeds; status is the last body status or zero | met | `control/while`, `control/while_break_value`, `control/c_while_status` |  |
| 2.9.4.6/1 | until repeats its body until the condition list succeeds | met | `control/until`, `control/c_until_status` |  |
| 2.9.5/1 | fname() compound-command defines a function; any compound command can be the body | met | `func/basic`, `func/compound_body`, `parse/func_simple_body`, `func/c_bodies` |  |
| 2.9.5/2 | Functions and variables have separate name spaces | met | `func/c_namespaces` |  |
| 2.9.5/3 | The body is expanded when called, not when defined | met | `func/c_expanded_at_call` |  |
| 2.9.5/4 | A redirection after the body applies each time the function is called | met | `redir/func_body`, `func/c_redirect_on_definition` |  |
| 2.9.5/5 | During the call the operands are the positional parameters and $# changes; both are restored after; $0 is unchanged | met | `func/positional_restore`, `func/args`, `func/c_positional_scope` |  |
| 2.9.5/6 | return ends the function; execution resumes after the call | met | `func/return_in_loop`, `builtin/return_status`, `func/c_return_resumes` |  |
| 2.9.5/7 | The status of a definition is zero; the status of a call is that of the last command run | met | `func/status_of_def`, `func/c_call_status` |  |
| 2.9.5/8 | A function can call itself and other functions, and can be redefined, including from inside itself | met | `func/recursion`, `func/redefine`, `func/c_redefine_self` |  |
| 2.9.5/9 | Variables assigned in a function are global; a function called in a subshell or pipeline does not change the caller | met | `func/global_assign`, `func/in_cmdsub` |  |
| 2.9.5/10 | A function name that is not a valid name is refused or accepted as an extension (recorded from dash) | not counted | `parse/bad_funcname` |  |

### 2.10 Grammar

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| 2.10/1 | A newline may follow \| && \|\| and the reserved words that open a list; ; cannot begin a command | met | `parse/newlines_ok`, `parse/leading_semicolon`, `parse/trailing_pipe`, `parse/trailing_andand`, `parse/c_newline_continues` |  |
| 2.10/2 | Empty compound lists are syntax errors: { }, ( ), then with no list, do with no list | met | `parse/empty_brace`, `parse/then_empty`, `parse/c_empty_lists`, `parse/c_empty_do`, `parse/c_empty_subshell` |  |
| 2.10/3 | Missing or stray closing words are syntax errors | met | `parse/missing_done`, `parse/missing_esac`, `parse/missing_fi`, `parse/missing_then`, `parse/done_late`, `parse/stray_dsemi`, `parse/stray_paren`, `parse/fi_unexpected`, `parse/case_no_in` |  |
| 2.10/4 | Unterminated quotes and substitutions are syntax errors | met | `parse/unterminated_backquote`, `parse/unterminated_cmdsub`, `parse/unterminated_dquote`, `parse/unterminated_squote` |  |
| 2.10/5 | A redirection needs a target word; a for needs a name | met | `parse/redirect_no_target`, `parse/for_bad_name` |  |
| 2.10.2/1 | Rule 1: a reserved word is recognized only as the whole unquoted token | met | `parse/c_rule1` |  |
| 2.10.2/2 | Rule 4: the case terminator esac is recognized where a pattern could begin | met | `parse/c_rule4` |  |
| 2.10.2/3 | Rule 5: the for variable must be a name | met | `parse/for_bad_name` |  |
| 2.10.2/4 | Rule 6: in and do after the for name are recognized on the same or a following line | met | `parse/c_rule6` |  |
| 2.10.2/5 | Rule 7: a word with = after a valid name at the start of a command is an assignment; otherwise it is a command name | met | `parse/c_rule7` |  |
| 2.10.2/6 | Rule 8: name() begins a function definition; a reserved word cannot be a function name | met | `parse/c_rule8` |  |
| 2.10.2/7 | Rule 9: words in a function body are not expanded or assigned at definition | met | `parse/c_rule9` |  |
| 2.10.2/8 | An io number is digits immediately before < or > | met | `parse/c_io_number` |  |
| 2.10.2/9 | Comments and blank lines form no command; a script of only those exits zero | met | `stdin/no_prompt`, `parse/c_only_comments` |  |
| 2.10.2/10 | A subshell and a brace group can be nested and combined with every list operator | met | `parse/c_nesting` |  |

### 2.11 Job control

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| 2.11/1 | An interactive shell with a controlling terminal puts itself in its own process group and makes that the terminal's foreground group | met | `session:c_jc_shell_is_leader` |  |
| 2.11/2 | With job control on, each foreground pipeline runs in its own process group, which is made the terminal's foreground group | met | `session:c_jc_foreground_group` |  |
| 2.11/3 | With job control on, an asynchronous list becomes a background job with a job number, in its own process group | met | `session:c_jc_background_job`, `session:c_jc_background_group`, `session:jc_background_subshell` |  |
| 2.11/4 | When a foreground job ends or stops, the shell makes its own group the terminal's foreground group again | met | `session:c_jc_terminal_back` |  |
| 2.11/5 | A foreground job stopped by SIGTSTP becomes a suspended job with a job number, and the shell writes a message and prompts | met | `session:c_jc_ctrl_z` |  |
| 2.11/6 | $? after a foreground job is stopped is the status it would have had if the signal had ended it | met | `session:c_jc_ctrl_z` |  |
| 2.11/7 | fg continues a suspended job in the foreground: terminal first, then SIGCONT to its group | met | `session:c_jc_fg`, `session:c_jc_fg_number` |  |
| 2.11/8 | bg continues a suspended job in the background | met | `session:c_jc_bg` |  |
| 2.11/9 | A background job that stops (SIGTTIN on reading the terminal) becomes a suspended job, reported before the next prompt | met | `session:c_jc_bg_ttin` |  |
| 2.11/10 | When a background job completes, an interactive shell writes a message before the next prompt | met | `session:c_jc_done_message` |  |
| 2.11/11 | With set -b the completion message is written at once | gap |  | no session case: the harness types when the shell is quiet and cannot place a message that arrives between two keys; dash 0.5.13.4 writes it at the next prompt anyway (sh18, black-box p11), bash at once; pelt writes it at once and edits the line again (notes/sh18-evidence/probe/keys/p24, p25) |
| 2.11/12 | The interactive shell saves the terminal settings when a job is suspended and fg restores them | gap |  | no session case: the harness does not read the terminal's settings |
| 2.11/15 | The terminal's interrupt character reaches the foreground job and not the shell | met | `session:c_jc_ctrl_c_job_only`, `session:ctrl_c_child`, `session:c_jc_ctrl_c_loop` |  |
| 2.11/16 | With job control, exit with stopped jobs warns and the shell stays, unless the line before was an exit that warned | not counted | `session:c_jc_exit_stopped` | XCU 2.11 lets the shell warn; dash does (black-box p07, p08) |
| 2.11/17 | A new job takes the lowest job number no job holds | not counted | `session:c_jc_numbering` | unspecified by POSIX; dash, black-box p02 |
| 2.11/18 | Ctrl-Z stops a whole foreground pipeline, the stages the shell runs itself included, as one job | met | `session:c_jc_mixed_pipeline` |  |
| 2.11/13 | set -m in a non-interactive shell puts each asynchronous list in its own process group | met | `jobsctl/c_monitor_script_pgid` |  |
| 2.11/14 | With job control off, a background command stays in the shell's process group | met | `jobsctl/c_no_monitor_pgid` |  |
| 2.11/19 | With set -m in a non-interactive shell, a job that ended is told after the complete command it ended during, never inside it: a loop's jobs after the loop, newest first, the ones wait answered and the ones the shell ran itself too | not counted | `jobsctl/c_monitor_loop_notices`, `jobsctl/c_monitor_loop_builtin`, `jobsctl/c_monitor_list_notices` | POSIX writes the message before a prompt, which a script never issues; dash tells them after the complete command, black-box (sh22 probe m01-m08, pelt#41) |
| 2.11/20 | With job control on, a subshell ( … ) run in the foreground is a job of its own: Ctrl-Z stops it, fg continues it | met | `session:jc_subshell_stop` |  |

### 2.12 Signals

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| 2.12/1 | With job control off, commands of an asynchronous list start with SIGINT and SIGQUIT ignored | met | `signal/background_ignores_int`, `signal/c_async_ignores_quit` |  |
| 2.12/2 | Otherwise commands inherit the signal actions the shell inherited, unless trap changed them | met | `signal/trap_ignore_inherited`, `signal/trap_caught_default_in_child`, `signal/c_inherited_ignore` |  |
| 2.12/3 | A trapped signal that arrives while a foreground command runs is acted on after that command completes | met | `signal/trap_deferred_to_foreground_end` |  |
| 2.12/4 | A trapped signal that arrives during wait makes wait return at once with a status above 128, then the trap runs | met | `signal/wait_interrupted`, `signal/c_wait_interrupted_term` |  |
| 2.12/5 | Signals for every name in signal.h can be trapped (USR1, ALRM, PIPE, CHLD, CONT, WINCH and the rest) | met | `signal/trap_usr1`, `signal/trap_ignore_usr1`, `signal/c_trap_alrm`, `signal/c_trap_pipe`, `signal/c_trap_usr1_self`, `signal/c_trap_abrt_number`, `signal/c_trap_winch_cont`, `signal/trap_every`, `signal/trap_ignore_every`, `signal/trap_chld`, `signal/trap_ignore_pipe_fifo` |  |

### 2.13 Execution environment

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| 2.13/1 | A utility is run with the shell's open files, working directory and file creation mask | met | `redir/child_inherits_fd`, `exec/fd3_inherited`, `cd/child_sees_it`, `env/c_utility_environment` |  |
| 2.13/2 | A utility receives the exported variables and those assigned for the command, and no others | met | `env/exact`, `env/never_exported`, `env/empty`, `env/only_pwd`, `env/c_exported_only` |  |
| 2.13/3 | A utility cannot change the shell's environment | met | `env/c_child_cannot_change` |  |
| 2.13/4 | A shell script run as a utility starts with caught traps at default and ignored signals still ignored | met | `signal/trap_caught_default_in_child`, `signal/trap_ignore_inherited` |  |
| 2.13/5 | A subshell is a duplicate of the shell environment: variables (exported or not), functions, options, positional parameters | met | `control/subshell`, `cmdsub/function`, `env/c_subshell_duplicate` |  |
| 2.13/6 | In a subshell, traps that are not ignored are reset to default | met | `signal/trap_subshell_reset`, `signal/trap_in_subshell`, `signal/trap_subshell_ends_restores`, `signal/c_subshell_trap_reset` |  |
| 2.13/7 | A subshell killed by a signal does not take the parent with it, and the parent sees a status above 128 | met | `signal/subshell_signal` |  |
| 2.13/8 | Changes made in a subshell do not affect the shell, for every subshell form: ( ), $( ), pipeline stage, & | met | `pipe/stage_is_subshell`, `cmdsub/isolation`, `env/c_subshell_forms` |  |
| 2.13/9 | exit in a subshell ends only the subshell, for every subshell form | met | `cmdsub/exit_inside`, `pipe/exit_in_stage`, `env/c_exit_in_subshell_forms` |  |
| 2.13/10 | A subshell has its own working directory and descriptors: cd and exec redirections there do not leak | met | `env/c_subshell_cwd_fds` |  |
| 2.13/11 | Subshells of one shell run concurrently as separate processes when asked to (& and pipeline stages) | met | `env/c_subshell_concurrent`, `env/subshell_is_process` |  |

### 2.14 Pattern matching

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| 2.14.1/1 | An ordinary character matches itself; a quoted or escaped special character matches itself | met | `glob/quoted`, `glob/edge_quoted`, `glob/c_quoted_specials` |  |
| 2.14.1/2 | ? matches any one character | met | `glob/question`, `glob/c_question` |  |
| 2.14.1/3 | [...] matches one character of the set; ranges, and ! for the complement | met | `glob/bracket`, `glob/edge_negate`, `glob/c_bracket` |  |
| 2.14.1/4 | Character classes [[:alpha:]] and the rest match by class | met | `glob/class`, `glob/edge_class`, `glob/c_classes` |  |
| 2.14.1/5 | A [ that does not open a valid bracket expression matches itself | met | `glob/edge_lone_open`, `glob/edge_open_a`, `glob/c_lone_bracket` |  |
| 2.14.1/6 | A backslash in a pattern that came from an expansion escapes the next character | met | `glob/edge_backslash`, `glob/c_backslash_from_expansion` |  |
| 2.14.1/7 | Equivalence classes and collating symbols in a bracket expression ([[=a=]], [[.a.]]) | met | `glob/c_equiv_collating` |  |
| 2.14.2/1 | * matches any string, the null string included; several * in one pattern each match as needed | met | `glob/star`, `glob/c_star` |  |
| 2.14.3/1 | In pathname expansion a slash must be matched explicitly, by neither * nor ? nor a bracket expression | met | `glob/path`, `glob/edge_slash`, `glob/c_slash_explicit` |  |
| 2.14.3/2 | A leading period in a file name must be matched explicitly, at the start or after a slash | met | `glob/hidden`, `glob/c_leading_period` |  |
| 2.14.3/3 | Matches are substituted in collating order; a pattern that matches nothing is left unchanged | met | `glob/sorted`, `glob/no_match`, `glob/c_sorted_nomatch` |  |
| 2.14.3/4 | Each pattern component is matched in its own directory; trailing slash selects directories | met | `glob/dirs_only`, `glob/c_components` |  |
| 2.14.3/5 | A directory that cannot be read or searched is not an error: the pattern is left as is | met | `glob/c_unreadable` |  |
| 2.14.3/6 | A word with no unquoted pattern character is left unchanged without reading any directory | met | `glob/edge_test_cmd`, `glob/edge_lone_close`, `glob/edge_a_close`, `glob/edge_empty`, `glob/edge_star_open` |  |
| 2.14.3/7 | Pattern characters produced by quoting inside an otherwise unquoted word stay literal | met | `glob/quoted`, `glob/c_mixed_quoting` |  |
| 2.14.3/8 | Matching in parameter expansion and case is not subject to the slash and period rules | met | `glob/c_no_file_rules_in_case` |  |

### 2.15 Special built-ins

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| 2.15/1 | An assignment before a special built-in affects the current environment; before a regular built-in it does not | met | `simple/persist_special`, `simple/temp_builtin` |  |
| 2.15/2 | A special built-in is found before a function or PATH entry of the same name | met | `builtin/c_special_first` |  |
| break/1 | break leaves the innermost loop; break n leaves n loops; more than the depth leaves the outermost | met | `builtin/break_n`, `builtin/c_break` |  |
| break/2 | break with an operand that is not a positive integer fails | met | `builtin/c_break_bad` |  |
| break/3 | A loop encloses a break only in the same execution environment: not across a subshell or a function body defined in the loop | met | `builtin/break_outside`, `builtin/c_break_lexical` |  |
| continue/1 | continue resumes the next iteration of the innermost loop, continue n of the nth enclosing loop | met | `builtin/continue_n`, `builtin/c_continue` |  |
| colon/1 | : does nothing and returns zero; its arguments are expanded | met | `builtin/colon_true_false`, `builtin/c_colon` |  |
| dot/1 | . file runs the file's commands in the current environment | met | `builtin/dot`, `builtin/c_dot_current_env` |  |
| dot/2 | Without a slash, the file is searched for in PATH and need not be executable | met | `builtin/c_dot_path` |  |
| dot/3 | When no readable file is found a non-interactive shell exits | met | `builtin/c_dot_missing` |  |
| dot/4 | The status is that of the last command in the file, zero if there is none | met | `builtin/c_dot_status` |  |
| dot/5 | return in a dot script ends the script, not the caller | met | `builtin/c_dot_return` |  |
| dot/6 | A syntax error in a dot script is a special built-in error | met | `builtin/c_dot_syntax_error` |  |
| dot/7 | Positional parameters of the caller are visible in the dot script | met | `builtin/c_dot_positional` |  |
| eval/1 | eval joins its arguments with spaces and runs the result in the current environment | met | `builtin/eval`, `builtin/c_eval_join` |  |
| eval/2 | eval with no arguments or only null arguments returns zero | met | `builtin/c_eval_empty` |  |
| eval/3 | eval's status is that of the command it ran; a syntax error is a special built-in error | met | `builtin/eval_syntax_error`, `builtin/c_eval_status` |  |
| eval/4 | return, break and continue inside eval act on the enclosing function or loop | met | `builtin/c_eval_flow` |  |
| exec/1 | exec with no utility makes its redirections permanent in the current shell | met | `redir/exec_fd`, `redir/exec_stdout`, `builtin/c_exec_redirects` |  |
| exec/2 | exec utility replaces the shell: nothing after it runs | met | `builtin/exec`, `redir/exec_command`, `exec/status`, `builtin/c_exec_replaces` |  |
| exec/3 | A failed exec ends a non-interactive shell with 126 or 127 | met | `exec/not_found`, `exec/not_executable`, `exec/exit_trap_when_it_fails`, `builtin/c_exec_fails` |  |
| exec/4 | exec in a subshell replaces only the subshell | met | `exec/subshell`, `exec/cmdsub`, `env/exec_subshell_exact`, `builtin/c_exec_subshell`, `exec/exec_replaces_subshell` |  |
| exec/5 | exec -- utility is accepted (utility syntax guidelines) | met | `builtin/c_exec_dashdash` |  |
| exec/6 | A redirection error on exec gives a status 1-125 and a non-interactive shell exits | met | `redir/special_fail_exits` |  |
| exit/1 | exit n ends the shell with status n; without n, with the last status | met | `builtin/exit_code`, `builtin/exit_default`, `builtin/c_exit_n` |  |
| exit/2 | The EXIT trap runs before the shell ends; exit inside it ends at once with that status | met | `builtin/trap_exit`, `builtin/trap_in_exit`, `builtin/trap_exit_status`, `signal/trap_exit_runs_exit_trap`, `builtin/c_exit_trap` |  |
| exit/3 | exit in an EXIT or signal trap action with no operand uses the status from before the trap | pending (exit-in-exit-trap) | `signal/trap_exit_no_operand`, `builtin/c_exit_in_trap_status` |  |
| exit/4 | exit in a function, loop, dot script or eval ends the whole shell | met | `builtin/exit_in_function`, `builtin/c_exit_everywhere` |  |
| exit/5 | exit with an operand above 256 that names a signal status ends the shell as if by that signal (new in 2024) | not counted | `builtin/c_exit_signal_status` | POSIX.1-2024 addition; neither dash 0.5.13.4 nor bash 5.3 --posix does it (both exit n mod 256); recorded, not counted |
| export/1 | export name gives the variable the export attribute: later commands see it | met | `env/reexport`, `env/export_no_value`, `builtin/c_export` |  |
| export/2 | export -p writes export name=value lines suitable for reinput | met | `builtin/export_p`, `builtin/c_export_p` |  |
| export/3 | export of a readonly variable with a new value fails | met | `builtin/c_export_readonly` |  |
| export/4 | export -- and invalid names | pending (builtin-dashdash) | `builtin/c_export_invalid` |  |
| readonly/1 | readonly name makes later assignment and unset fail | met | `builtin/readonly_error`, `builtin/unset_readonly`, `builtin/c_readonly` |  |
| readonly/2 | readonly -p writes readonly name=value lines suitable for reinput | pending (readonly-p-unset) | `builtin/readonly_p`, `builtin/c_readonly_p` |  |
| readonly/3 | A readonly variable cannot be changed by read, getopts, for, export, or an arithmetic assignment | met | `builtin/c_readonly_everywhere`, `getopts/readonly_target` |  |
| return/1 | return n ends the function with status n; without n, with the last status | met | `builtin/return_status`, `builtin/c_return` |  |
| return/2 | return in a trap action with no operand uses the status from before the trap | met | `builtin/c_return_in_trap` |  |
| return/3 | return outside a function or dot script (recorded from dash; unspecified by POSIX) | not counted | `builtin/return_top` |  |
| set/1 | set with no arguments writes every variable as name=value, quoted for reinput, sorted | met | `builtin/c_set_lists` |  |
| set/2 | set -- args sets the positional parameters, replacing all; set -- alone clears them | met | `builtin/set_positional`, `builtin/c_set_positional` |  |
| set/3 | set -a exports every variable assigned afterwards, however assigned | met | `option/allexport`, `option/c_allexport_forms` |  |
| set/4 | set -C prevents > from overwriting an existing regular file | met | `redir/noclobber` |  |
| set/5 | set -e exits when a command fails | met | `option/errexit`, `option/c_errexit_basic` |  |
| set/6 | set -e ignores failures in the condition of if, while, until, in a ! pipeline, and in all but the last of an AND-OR list | met | `option/errexit_if`, `option/errexit_while`, `option/errexit_not`, `option/errexit_andor`, `option/c_errexit_exempt` |  |
| set/7 | Under set -e only the pipeline's own status matters, not an earlier stage's or a command substitution's inside a word | met | `pipe/set_e`, `option/c_errexit_pipeline` |  |
| set/8 | Under set -e an assignment from a failing command substitution exits | met | `option/c_errexit_assign_cmdsub` |  |
| set/9 | set -e is ignored inside a compound command or function that runs in an exempt context | met | `option/errexit_function`, `option/c_errexit_ignored_inside` |  |
| set/10 | set -e applies in each subshell separately; a failing subshell then fails in the parent | met | `option/errexit_subshell`, `option/c_errexit_subshell_forms` |  |
| set/11 | Under set -e the EXIT trap still runs, and the status is the failing command's | met | `option/c_errexit_trap` |  |
| set/12 | A compound command whose status came from an ignored failure does not trigger -e | met | `option/c_errexit_compound_status` |  |
| set/13 | set -f disables pathname expansion | met | `option/noglob`, `glob/noglob` |  |
| set/14 | set -n reads commands without executing them | met | `option/c_noexec` |  |
| set/15 | set -u makes expanding an unset parameter an error, except $@ and $* | met | `option/nounset`, `option/nounset_positional`, `option/c_nounset_forms` |  |
| set/15b | set -u applies to an unset variable named in an arithmetic expansion | met | `option/c_nounset_arith` | POSIX.1-2024 names arithmetic expansion in -u; dash 0.5.13.4 reads the unset variable as 0, so bash --posix is the oracle |
| set/16 | set -v writes input lines to standard error as they are read | pending (verbose) | `option/c_verbose`, `option/c_verbose_stderr` | pelt#6 |
| set/17 | set -x writes each expanded command to standard error before running it | pending (xtrace-assignment) | `option/xtrace`, `option/c_xtrace_forms` |  |
| set/18 | set -o name and set +o name are the long forms of the option letters | met | `option/set_o`, `option/c_long_names` |  |
| set/19 | set +o writes commands that restore the current option settings; set -o lists them | met | `option/c_plus_o` |  |
| set/20 | set -o ignoreeof, nolog, vi are accepted | met | `option/c_up_options` |  |
| set/21 | set -o pipefail is accepted and reported (new in 2024) | met | `option/c_pipefail_option`, `option/pipefail_cluster` |  |
| set/22 | set -h and set -b are accepted | met | `option/c_h_b` | dash 0.5.13.4 refuses -h; POSIX requires it be accepted, so bash --posix is the oracle |
| set/23 | An invalid option is an error: a non-interactive shell exits | met | `option/bad_option` |  |
| set/24 | Options given on the sh command line are set, and appear in $- | met | `sh/c_options_on_command_line` |  |
| shift/1 | shift n drops the first n positional parameters; default 1; shift 0 changes nothing | met | `builtin/shift`, `builtin/c_shift` |  |
| shift/2 | shift by more than $# fails with a message (a non-interactive shell may exit) | met | `builtin/shift_error` |  |
| times/1 | times writes two lines of user and system times in the form NmN.NNs NmN.NNs | met | `builtin/times`, `builtin/c_times_format` |  |
| times/2 | times reports real accumulated times: after burning CPU the shell's user time is not zero | met | `builtin/c_times_real` |  |
| trap/1 | trap action condition... sets the action; it runs via eval when the condition arises | met | `signal/trap_int`, `signal/trap_term`, `signal/trap_hup`, `signal/trap_quit`, `signal/trap_usr2`, `signal/trap_eval`, `signal/trap_two` |  |
| trap/2 | trap - condition resets to default; a first operand that is an unsigned integer resets all operands | met | `signal/trap_reset`, `signal/trap_reset_number`, `builtin/trap_reset`, `signal/c_trap_reset_forms` |  |
| trap/3 | trap '' condition ignores the signal | met | `signal/trap_ignore`, `signal/trap_ignore_int` |  |
| trap/4 | $? after a trap action is what it was before the action | met | `signal/trap_status_kept`, `signal/trap_action_status_dropped` |  |
| trap/5 | Conditions may be EXIT, 0, a name without SIG, or a number | met | `signal/trap_number`, `signal/c_trap_condition_names` |  |
| trap/6 | trap with no operands writes trap -- 'action' condition for each condition not at default, quoted for reinput | met | `signal/trap_print`, `builtin/trap_print`, `signal/c_trap_print_reinput` |  |
| trap/7 | trap -p writes the action of each named condition, and of every condition with no operand (new in 2024) | pending (trap-p) | `signal/c_trap_p` | POSIX.1-2024 addition; dash 0.5.13.4 has no -p, so bash --posix is the oracle |
| trap/8 | An invalid condition gives a warning and a non-zero status, and the shell does not exit | met | `signal/trap_bad_condition`, `signal/c_trap_invalid` |  |
| trap/9 | Traps stay in place until changed; an action can itself set or reset traps | met | `signal/trap_replaced`, `signal/trap_twice_same`, `signal/c_trap_in_action` |  |
| trap/10 | $(trap) in a command substitution shows the parent's traps | met | `signal/trap_in_cmdsub`, `signal/c_trap_cmdsub_shows_parent`, `signal/trap_cmdsub_lone_exit` |  |
| trap/11 | The EXIT trap runs in the environment of the last command: variables and $? are visible; it runs once | met | `builtin/trap_exit`, `signal/trap_exit_in_action`, `signal/c_exit_trap_env` |  |
| trap/12 | An EXIT trap set in a subshell runs when that subshell ends; the parent's EXIT trap does not run there | met | `signal/trap_in_subshell`, `signal/c_exit_trap_subshell` |  |
| trap/13 | A signal ignored on entry to a non-interactive shell cannot be trapped or reset | met | `signal/c_ignored_on_entry`, `signal/ignored_at_start` | since sh14 (wolf 0.2.29, `os_signal_ignored`); from outside, tools/signal-witness |
| trap/14 | A trap action runs between commands of a list, loop or function, not only at the end of the script | met | `signal/trap_in_loop`, `signal/trap_in_function`, `signal/trap_breaks_loop`, `signal/trap_action_runs_program`, `signal/trap_action_sets_variable` |  |
| trap/15 | trap -- action condition is accepted | met | `signal/c_trap_dashdash` |  |
| trap/16 | A signal with a default action of terminate ends the shell with that signal when not trapped; the EXIT trap may or may not run | met | `signal/death_runs_no_exit_trap` |  |
| unset/1 | unset name removes the variable and its export attribute; unset -v the same | met | `builtin/unset`, `env/unset_var`, `env/unset_exported`, `builtin/c_unset_forms` |  |
| unset/2 | unset -f removes a function, and not a variable of that name | met | `func/unset_f`, `builtin/c_unset_f` |  |
| unset/3 | unset of a readonly variable fails with a non-zero status | met | `builtin/unset_readonly` |  |
| unset/4 | Unsetting IFS, PATH and other shell variables works and has the specified effect | met | `builtin/c_unset_shell_vars` |  |

### `sh` (utility page)

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| sh/1 | sh -c string runs the string; the next operand is $0 and the rest are positional parameters | met | `sh/c_dash_c` |  |
| sh/2 | sh -c with an empty string exits zero | met | `sh/c_dash_c_empty` |  |
| sh/3 | sh -c reads no commands from standard input, which stays available to the commands | met | `sh/c_dash_c_stdin` |  |
| sh/4 | sh file args runs the file with $0 the file name and the operands as positional parameters; the file need not be executable | met | `exec/argv0`, `sh/c_command_file` |  |
| sh/5 | A command file with no slash is looked for in the current directory first | met | `sh/c_command_file_cwd` |  |
| sh/6 | A command file that cannot be found gives status 127 | met | `sh/c_command_file_missing`, `sh/c_dashdash_operand` | dash 0.5.13.4 exits 2; the sh page says 127, so bash --posix is the oracle |
| sh/7 | sh -s reads commands from standard input and takes operands as positional parameters; no operands and no -c means -s | met | `stdin/program_takes_rest`, `sh/c_dash_s`, `sh/lone_hyphen` |  |
| sh/8 | The shell does not read ahead on standard input: a command it starts reads the bytes after its own line | met | `stdin/read_takes_next_line`, `stdin/program_takes_rest`, `sh/c_no_read_ahead`, `sh/c_no_read_ahead_file` |  |
| sh/9 | A script of only blank lines and comments exits zero; the status is otherwise that of the last command | met | `parse/comments_ok`, `sh/c_exit_status` |  |
| sh/10 | A syntax error in a non-interactive shell gives a status from 1 to 125 | met | `sh/c_syntax_status` |  |
| sh/11 | A shell given -i, or reading standard input with input and error on a terminal, is interactive; otherwise not | met | `session:default_interactive`, `stdin/no_prompt`, `sh/c_not_interactive` |  |
| sh/12 | -c and -s combine with option letters in one argument and with -o | met | `sh/c_combined_options`, `sh/option_clusters` |  |
| sh/13 | Input lines may be of any length | met | `sh/c_long_line` |  |
| sh/14 | The shell's own exit: the EXIT status is that of the last command when input ends | met | `sh/c_eof_status` |  |
| sh/15 | An interactive shell ignores SIGQUIT and SIGTERM and survives SIGINT | met | `session:ctrl_c_prompt`, `session:term_at_prompt` |  |
| sh/16 | With -m an interactive shell ignores SIGTSTP, SIGTTIN and SIGTTOU | met | `session:c_jc_shell_ignores_tstp` |  |
| sh/17 | set -o ignoreeof keeps an interactive shell alive at end-of-file | pending (ignoreeof) | `session:c_ignoreeof` |  |
| sh/18 | The command history list: commands typed are kept, at least 128 of them, HISTSIZE and HISTFILE honoured | met | `session:c_hist_fc_list`, `session:c_hist_histsize`, `session:c_hist_file_read` | HISTFILE read at the start is a session (c_hist_file_read); written by one shell and read by the next, two shells sharing one file, and the file cut to HISTSIZE are tools/hist-witness (sh12, CI on both tiers): one session is one shell |
| sh/19 | set -o vi: ESC enters command mode; motion, editing and history keys as the vi-mode sections list (about 60 commands) | met | `session:c_vi_basic`, `session:c_vi_motion`, `session:c_vi_history` |  |
| sh/20 | In vi insert mode the erase, kill, ^V, ^W and end-of-file characters act as described | met | `session:c_vi_insert`, `session:c_vi_basic`, `session:c_vi_insert_ctrl_w`, `session:c_vi_insert_kill`, `session:c_vi_insert_erase`, `session:c_vi_insert_ctrl_v`, `session:c_vi_eof`, `session:c_vi_stty_erase`, `session:c_vi_stty_intr` |  |
| sh/21 | MAIL, MAILCHECK, MAILPATH: the shell tells the user before a prompt when a mailbox file changes | pending (mail) | `session:c_mail` |  |
| sh/24 | An interactive shell accepts an input line longer than the terminal's own line limit (input lines are of unlimited length) | met | `session:c_long_line` |  |
| sh/25 | With no editing mode on, the terminal's erase, kill and word-erase characters edit the line before the shell sees it | met | `session:c_tty_erase` |  |
| sh/26 | Lines that arrive together are run one after the other | met | `session:c_paste_two_lines` |  |
| sh/27 | set -o vi turns any other editing mode off; set +o vi turns vi mode off | met | `session:c_vi_emacs_switch`, `option/c_edit_modes` |  |
| sh/28 | In vi command mode a count before a command repeats it (x, ~, r, the repeat command) | met | `session:c_vi_count_x`, `session:c_vi_tilde`, `session:c_vi_replace_char`, `session:c_vi_dot_count` |  |
| sh/29 | vi motions: l, h, w, W, e, E, b, B, ^, $, 0, \|, f, F, t, T, ; and , move as the page says | met | `session:c_vi_motions`, `session:c_vi_E_e`, `session:c_vi_bigword`, `session:c_vi_caret`, `session:c_vi_bar`, `session:c_vi_find`, `session:c_vi_till`, `session:c_vi_back_find` |  |
| sh/30 | vi a, A, i, I and R enter insert mode at the places the page gives | met | `session:c_vi_dollar_append`, `session:c_vi_insert_start`, `session:c_vi_R` |  |
| sh/31 | vi c, d and y with a motion, cc, dd and yy, and C, D, S, Y change, delete or yank the range the page gives | met | `session:c_vi_dw`, `session:c_vi_cw`, `session:c_vi_D_C`, `session:c_vi_S`, `session:c_vi_dd_cc`, `session:c_vi_yank_put` |  |
| sh/32 | vi x, X, p, P, _ and # act as the page lists | met | `session:c_vi_X`, `session:c_vi_yank_put`, `session:c_vi_underscore`, `session:c_vi_hash` |  |
| sh/33 | vi . repeats the last change, even one made on an earlier line, with its count unless a new count is given | met | `session:c_vi_dot`, `session:c_vi_dot_count` |  |
| sh/34 | vi u undoes the last change and U every change to the line | met | `session:c_vi_undo`, `session:c_vi_undo_all` | U: POSIX says all changes to the edit line; bash, as a user sees it, goes back to the line as command mode first found it, and so does pelt |
| sh/35 | vi k, -, j, +, G walk the history; /pattern and ?pattern search it (a leading ^ anchors), n and N repeat the search | met | `session:c_vi_history`, `session:c_vi_history_jk`, `session:c_vi_history_G`, `session:c_vi_search`, `session:c_vi_search_n`, `session:c_vi_search_anchor` |  |
| sh/36 | vi =, \ and * expand the bigword at the cursor as pathnames; @letter inserts the alias _letter, and does nothing when there is none | met | `session:c_vi_star`, `session:c_vi_backslash`, `session:c_vi_at_letter` |  |
| sh/37 | vi v edits the line with vi in a temporary file, then runs it | met | `session:c_vi_v`, `session:c_vi_v_number`, `session:c_vi_v_fail` |  |
| sh/38 | SIGINT while a line is edited ends the line and reissues the prompt on the next line | met | `session:c_vi_ctrl_c`, `session:c_ed_ctrl_c`, `session:c_ed_ctrl_c_continued` |  |
| sh/22 | ENV is ignored when the real and effective user or group IDs differ | untestable |  | needs a set-user-ID shell; not built by the corpus (and wolf has no uid surface, wolf-lang#633) |
| sh/23 | A FIFO or terminal standard input set non-blocking is put back to blocking reads | untestable |  | needs a descriptor inherited with O_NONBLOCK; measured by hand (docs/CENSUS.md) |

### `alias` (utility page)

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| alias/1 | alias name=value defines an alias; alias name writes it as name=value quoted for reinput; alias alone writes all | met | `alias/c_alias_print`, `alias/forms` |  |
| alias/2 | alias for a name with no definition fails with a message, and other operands are still processed | met | `alias/c_alias_missing` |  |
| alias/3 | unalias name removes it; unalias -a removes all; removing a missing alias fails | met | `alias/c_unalias` |  |
| alias/4 | An alias may name a reserved word position and aliases apply after reserved words that take a command | met | `alias/c_after_reserved`, `alias/function_names` |  |
| alias/5 | An alias defined in a function or compound command is not in effect for the rest of that already-parsed command | met | `alias/c_parse_time`, `alias/parse_time_more` |  |
| alias/6 | Alias names may contain ! % , @ and the portable filename characters | met | `alias/c_alias_names` |  |

### `command` (utility page)

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| command/1 | command name runs the utility ignoring functions | met | `builtin/command_bypass`, `command/c_bypass_function` |  |
| command/2 | command -v name writes how the name would be run: a path, the name of a built-in or function, an alias definition, a reserved word | met | `builtin/command_v`, `command/c_v`, `command/v_forms`, `command/v_alias` |  |
| command/3 | command -V name writes a description in words for each kind | met | `command/c_big_v` |  |
| command/4 | command -p uses a default PATH that finds the standard utilities | met | `command/c_p` |  |
| command/5 | command before a special built-in removes its special properties: errors do not exit, assignments do not persist | met | `builtin/command_bypass`, `command/c_special_properties` |  |
| command/6 | The status of command is that of the utility; 127 not found, 126 not executable | met | `command/c_status` |  |
| command/7 | command is not a declaration utility by itself, but command export keeps assignment context | met | `command/c_declaration` |  |

### `type` (utility page)

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| type/1 | type name writes how each name would be interpreted, and fails for a name that is not found | met | `type/c_type`, `type/statuses` |  |
| type/2 | type's output names the path of a utility found in PATH | met | `type/c_type_path` |  |

### `hash` (utility page)

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| hash/1 | hash name remembers the utility's location; hash alone lists; hash -r forgets; a missing utility fails | met | `hash/c_hash`, `hash/remembers`, `hash/forgets` |  |
| hash/2 | A remembered location that stops working is searched for again | met | `hash/c_stale`, `hash/kept_path` |  |

### `cd` (utility page)

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| cd/1 | cd with no operand goes to HOME; with HOME unset or empty it fails or does nothing as recorded | met | `cd/home`, `cd/c_home_forms` |  |
| cd/2 | cd - goes to OLDPWD and writes the new directory | met | `cd/minus`, `cd/oldpwd`, `cd/c_minus` |  |
| cd/3 | cd sets PWD and OLDPWD, and they are what a later child sees when exported | met | `cd/oldpwd`, `cd/child_sees_it`, `cd/c_pwd_oldpwd` |  |
| cd/4 | cd -L (default) keeps symbolic links in PWD and resolves dot-dot against it; cd -P uses the physical path | met | `cd/symlink`, `cd/dotdot`, `cd/c_logical_physical` |  |
| cd/5 | CDPATH is searched for a relative operand that does not begin with dot or dot-dot, and the result is written when found there | met | `cd/cdpath`, `cd/cdpath_prints`, `cd/c_cdpath_forms` |  |
| cd/6 | cd to a missing directory, a file, or with too many operands fails with a non-zero status and PWD unchanged | met | `cd/fail`, `cd/relative_file`, `cd/c_failures` |  |
| cd/7 | cd -e with -P exits 1 when the new directory's name cannot be determined (new in 2024) | pending (cd-e) | `cd/c_dash_e` | POSIX.1-2024 addition; dash 0.5.13.4 has no -e; bash --posix is the oracle |
| cd/8 | cd canonicalizes: dot components and repeated slashes are removed from PWD | met | `cd/c_canonical`, `cd/c_root_relative` |  |
| cd/9 | An explicit leading // is kept in PWD, and a relative cd from // stays under it | not counted | `cd/c_double_slash`, `cd/c_double_slash_path` | POSIX leaves a leading // implementation-defined (XBD 4.13, XCU cd step 8c); dash and bash keep it (sh19, pelt#37) |

### `pwd` (utility page)

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| pwd/1 | pwd writes the absolute pathname of the current directory; -L from PWD when valid, -P with no symbolic links | met | `builtin/pwd`, `pwd/c_pwd` |  |
| pwd/2 | pwd with a bad option fails | pending (pwd-bad-option) | `pwd/c_pwd_bad` |  |

### `echo` (utility page)

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| echo/1 | echo writes its arguments separated by spaces and a newline | met | `builtin/echo_n`, `builtin/echo_escapes`, `echo/c_echo` |  |
| echo/2 | echo with XSI escapes (\c \n \t \\ \0nnn) — recorded from dash, which is XSI; bash --posix differs | not counted | `builtin/echo_escapes` | implementation-defined when the first operand is -n or any operand has a backslash; dash is the oracle because scripts under /bin/sh rely on it |

### `true` (utility page)

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| true/1 | true returns zero and false non-zero, ignoring arguments | met | `builtin/colon_true_false`, `echo/c_true_false` |  |

### `test` (utility page)

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| test/1 | test with no operands is false; one operand is true if not null | met | `builtin/test_strings`, `test/c_arity_0_1` |  |
| test/2 | Two operands: ! negates; a unary primary is applied | met | `test/c_arity_2` |  |
| test/3 | Three operands: a binary primary is applied first; then ! with two; then ( x ) | met | `builtin/test_logic`, `test/c_arity_3` |  |
| test/4 | Four operands: ! with three | met | `test/c_arity_4` |  |
| test/5 | String primaries: = != -n -z, and < > by byte order (new in 2024) | met | `builtin/test_strings`, `builtin/test_string_order`, `test/c_strings` |  |
| test/6 | Integer primaries: -eq -ne -gt -ge -lt -le, with signs and leading zeros and blanks | met | `builtin/test_integers`, `test/c_integers` |  |
| test/7 | An operand that is not an integer makes an integer primary an error: status above 1 | met | `builtin/test_errors`, `test/c_integer_errors` |  |
| test/8 | File primaries: -e -f -d -r -w -x -s -L -h | pending (host-dir-size) | `builtin/test_files`, `test/c_files` |  |
| test/9 | File type primaries: -b -c -p -S -g -u -k, and -t for a terminal | met | `test/c_file_types` |  |
| test/10 | -ef -nt -ot compare two files (new in 2024) | met | `test/c_file_compare`, `test/primaries_more` |  |
| test/11 | -O and -G test ownership by the effective user and group | pending (uid) | `test/c_owner` | wolf-lang#633 (no uid surface) |
| test/12 | -a and -o and parentheses (obsolescent XSI forms scripts still use) | met | `builtin/test_logic`, `test/c_and_or` |  |
| test/13 | [ needs a closing ] and reports its absence | met | `builtin/bracket` |  |
| test/14 | -r -w -x reflect the permissions that apply to the caller | met | `test/c_permissions` |  |

### `printf` (utility page)

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| printf/1 | printf format with %s %d %c and literal text; the format is reused until operands run out | met | `builtin/printf_formats`, `builtin/printf_reuse`, `printf/c_basic` |  |
| printf/2 | Escape sequences in the format: \\ \a \b \f \n \r \t \v \ddd | met | `builtin/printf_escapes`, `printf/c_format_escapes` |  |
| printf/3 | %b interprets backslash escapes in its operand, including \c which stops output and \0ddd | met | `builtin/printf_b`, `printf/c_b` |  |
| printf/4 | Integer conversions %d %i %o %u %x %X with flags, width and precision | met | `builtin/printf_zero_pad`, `builtin/printf_unsigned`, `builtin/printf_width_star`, `printf/c_integers` |  |
| printf/5 | String conversions with width and precision; %c takes the first character; %% is a percent sign | met | `printf/c_strings` |  |
| printf/6 | A numeric operand starting with a quote is the character's code | met | `builtin/printf_char_value`, `printf/c_quote_value` |  |
| printf/7 | A bad numeric operand gives a diagnostic and a non-zero status, and output still happens | pending (printf-partial-number) | `builtin/printf_bad_number`, `printf/c_bad_operand` |  |
| printf/8 | Floating conversions %e %f %g %a (required when the system has them: recorded from dash) | pending (printf-float) | `printf/c_floats` |  |
| printf/9 | printf with no format operand fails; -- ends options | pending (builtin-dashdash) | `printf/c_usage` |  |
| printf/10 | Numbered argument conversions %n$ (new in 2024) | not counted | `printf/c_numbered` | POSIX.1-2024 addition; neither dash 0.5.13.4 nor bash 5.3 implements it; recorded, not counted |

### `read` (utility page)

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| read/1 | read assigns fields split by IFS to the variables; the last gets the rest, trimmed of IFS white space | met | `builtin/read`, `builtin/read_ifs`, `read/c_fields`, `read/trailing_delimiter` |  |
| read/2 | Without -r a backslash escapes the next character and backslash-newline continues the line; with -r backslash is literal | met | `builtin/read_raw`, `read/c_backslash` |  |
| read/3 | read returns non-zero at end-of-file, having assigned what it read | met | `read/c_eof` |  |
| read/4 | read reads exactly one line, leaving the rest of the input for the next reader | met | `read/c_one_line` |  |
| read/5 | read with no variable name: REPLY as an extension, or an error (recorded from dash) | not counted | `read/c_no_var` | POSIX requires at least one var operand; behaviour without one is unspecified |
| read/6 | read -d delim reads up to the delimiter; -d '' reads up to a NUL (new in 2024) | met | `read/c_delim`, `read/delim_forms` | POSIX.1-2024 addition; dash 0.5.13.4 has no -d; bash --posix is the oracle |
| read/7 | read into a readonly variable or an invalid name fails | met | `read/c_bad_target`, `read/target_order` |  |
| read/8 | read uses the shell's IFS when none is given for the command, and does not expand what it reads | met | `read/c_no_expansion` |  |
| read/9 | read from a descriptor other than 0 through redirection, and from a here-document | met | `redir/heredoc_read`, `redir/read_fd` |  |

### `getopts` (utility page)

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| getopts/1 | getopts walks options, setting the variable and OPTIND; returns non-zero at the end with the variable set to ? | met | `builtin/getopts`, `getopts/c_basic` | dash 0.5.13.4 sets OPTARG to the empty string for an option with no argument, and restarts oddly after OPTIND=1; the page says unset, so bash --posix is the oracle for the getopts cases that show OPTARG |
| getopts/2 | Grouped options, an option-argument in the same word, and -- to end options | met | `getopts/c_grouping` |  |
| getopts/3 | An unknown option: ? with a diagnostic and OPTARG unset; with a leading colon in optstring, ? with OPTARG the letter and no diagnostic | met | `builtin/getopts_bad`, `getopts/c_unknown` |  |
| getopts/4 | A missing option-argument: ? with a diagnostic, or : with OPTARG the letter when optstring starts with a colon | met | `getopts/c_missing_arg` |  |
| getopts/5 | getopts parses explicit operands in place of the positional parameters | met | `getopts/c_explicit_args` |  |
| getopts/6 | OPTIND starts at 1; setting OPTIND=1 restarts parsing; a first non-option operand ends it | met | `getopts/c_optind` |  |
| getopts/7 | getopts in a function uses the function's parameters; OPTIND is a shell-wide variable | met | `getopts/c_in_function` |  |

### `wait` (utility page)

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| wait/1 | wait with no operands waits for every child and returns zero | met | `jobs/wait_all`, `wait/c_all` |  |
| wait/7 | wait does not wait for a stopped job; wait for a stopped job answers its stop status | not counted | `session:c_jc_wait_stopped` | dash, black-box p12 |
| wait/2 | wait pid returns that child's status; several operands: the status of the last | met | `jobs/wait_program_status`, `jobs/wait_subshell_status`, `signal/wait_two_jobs`, `wait/c_pid` |  |
| wait/3 | wait for a pid that is not a child of this shell returns 127 | met | `jobs/wait_unknown`, `wait/c_unknown` |  |
| wait/4 | wait reports a child ended by a signal with a status above 128 | met | `signal/child_bg_wait`, `wait/c_signalled`, `wait/waited_signal_said` |  |
| wait/5 | The status of a child that ended before wait is still collected, for any of the known process IDs | met | `signal/wait_twice`, `signal/child_bg_unwaited`, `wait/c_already_ended`, `wait/c_pid_again`, `wait/c_unwaited_many_status`, `wait/reaped_signal_quiet` |  |
| wait/6 | wait with a job ID operand (%1, %%) | met | `wait/c_job_id`, `wait/job_ids` |  |
| wait/7 | wait in a subshell cannot wait for the parent's children | met | `wait/c_subshell` |  |
| wait/8 | An ended job whose status wait answered by its process ID is forgotten once the next asynchronous list starts: a later wait for that ID returns 127 | not counted | `wait/c_pid_forgotten` | POSIX 2.9.3.1 keeps an ID known only until the application waits for it; when it is forgotten is the shell's: dash, black-box (sh19 w01, w08); bash forgets it at once |

### `kill` (utility page)

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| kill/1 | kill pid sends SIGTERM; kill -s name and kill -name and kill -number send that signal; the status of a signalled child shows it | met | `signal/child_bg_wait`, `kill/c_send`, `kill/forms`, `kill/status_names`, `kill/self` |  |
| kill/2 | kill -l lists signal names; kill -l number names that signal; kill -l with an exit status names the signal that caused it | met | `kill/c_list`, `kill/list` |  |
| kill/3 | kill -0 pid tests for the process without sending; a missing process fails | met | `kill/c_zero`, `kill/targets` |  |
| kill/4 | kill is built in: it signals by job ID (%1), and works on the shell's own children without a search of PATH | met | `kill/c_job_id`, `kill/builtin`, `kill/job_ids` |  |
| kill/5 | kill with a bad signal name or no operand fails | met | `kill/c_bad`, `kill/refused` |  |
| kill/6 | kill accepts several pids, a negative pid for a process group, and -- before it | met | `kill/c_multiple` | no differential case sends to a group, under the oracle or pelt: the corpus runs in the harness's own group; a group a session made is signalled in kill/7 (sh18: `os_signal_send_group`) |
| kill/7 | With job control kill %job signals the job's process group, and kill -- -N group N | met | `session:c_jc_kill_group` |  |

### `umask` (utility page)

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| umask/1 | umask writes the mask as octal; umask -S symbolically; umask mode sets it for the shell and its children | met | `umask/c_umask` |  |
| umask/2 | umask accepts a symbolic mode | met | `umask/c_symbolic` |  |
| umask/3 | umask with an invalid mode fails | met | `umask/c_bad` |  |

### `ulimit` (utility page)

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| ulimit/1 | ulimit -f reports or sets the file size limit in 512-byte blocks; unlimited is written as the word | pending (ulimit) | `ulimit/c_file_size` |  |
| ulimit/2 | A file-size limit applies to children: a write past it fails | pending (ulimit) | `ulimit/c_enforced` |  |
| ulimit/3 | ulimit -H and -S select hard and soft limits; -a reports all; -c -d -n -s -t -v name resources (new in 2024) | pending (ulimit) | `ulimit/c_resources` |  |
| ulimit/4 | Raising a hard limit without privilege, or a bad operand, fails | pending (ulimit) | `ulimit/c_bad` |  |

### `fc` (utility page)

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| fc/1 | fc -l lists the history; fc -l first last selects a range; -n omits numbers; -r reverses | met | `session:c_hist_fc_list`, `session:c_hist_fc_list_default`, `session:c_hist_fc_list_reverse`, `session:c_hist_fc_list_string`, `session:c_hist_fc_list_clamp` | where bash and POSIX part (-r with first newer than last cancels, POSIX example; a multi-line entry keeps its lines) the table checks pin pelt to POSIX (src/sh/selftest.lu) |
| fc/2 | fc -s re-executes a command, optionally with old=new substituted | met | `session:c_hist_fc_s`, `session:c_hist_fc_s_prev`, `session:c_hist_fc_s_string` |  |
| fc/3 | fc first last edits the commands with FCEDIT or -e editor and then runs the result | met | `session:c_hist_fc_edit`, `session:c_hist_fc_e_fail`, `session:c_hist_fc_e_range`, `session:c_hist_fc_fcedit` |  |
| fc/4 | fc in a non-interactive shell with no history fails without ending the shell | met | `fc/c_noninteractive` |  |
| fc/5 | A string operand that names no command is an error (status >0) and the shell goes on | met | `session:c_hist_fc_notfound` |  |

### `jobs` (utility page)

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| jobs/1 | jobs lists each job: [n], current (+) or previous (-), state, command; -l adds process IDs; -p writes only process group IDs | met | `session:c_jc_jobs_list`, `session:c_jc_job_ids`, `session:c_jc_jobs_l_pipeline` |  |
| jobs/2 | jobs in a non-interactive shell lists background commands and jobs -p writes their process IDs | met | `jobsctl/c_jobs_script` |  |
| jobs/3 | A job's state is reported as Running, Done, Done(n), Stopped (signal) as the page lists | met | `session:c_jc_jobs_states`, `session:c_jc_states` |  |
| jobs/4 | One simple command forked as a command substitution or a pipeline stage lists the shell's jobs; a ( … ) subshell, and a pipeline inside a substitution, start with none, and in no subshell is a job one to wait for or signal by its job ID | not counted | `jobs/subshell_jobs`, `session:subshell_jobs` | POSIX gives jobs the current shell environment's jobs and leaves a subshell's copy of them unspecified; dash, black-box (sh20, notes/sh20-the-fork.md) |

### `fg` (utility page)

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| fg/1 | fg with no operand runs the current job in the foreground; fg %n that job; its command is written first | met | `session:c_jc_fg`, `session:c_jc_fg_number`, `session:c_jc_fg_pipeline` |  |
| fg/2 | fg and bg with job control off fail with a message | met | `jobsctl/c_fg_bg_no_monitor` |  |

### `bg` (utility page)

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| bg/1 | bg resumes a suspended job in the background and writes [n] command | met | `session:c_jc_bg`, `session:c_jc_bg_running` |  |

### Line editing beyond POSIX (not counted)

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| ed/1 | Left and right arrows move the cursor; a character typed is inserted there | not counted | `session:c_ed_left_insert` |  |
| ed/2 | Ctrl-A and Ctrl-E (Home and End) move to the ends of the line | not counted | `session:c_ed_home_end` |  |
| ed/3 | Ctrl-K kills to the end of the line; Ctrl-D deletes the character under the cursor | not counted | `session:c_ed_kill_to_end`, `session:c_ed_delete_char` |  |
| ed/4 | Up and down arrows walk the history, and a recalled line can be edited | not counted | `session:c_ed_up_arrow`, `session:c_ed_up_down_edit` |  |
| ed/5 | Ctrl-R searches the history backwards as the pattern is typed | not counted | `session:c_ed_search`, `session:c_ed_search_again`, `session:c_ed_search_edit`, `session:c_ed_search_abort`, `session:c_ed_search_backspace`, `session:c_ed_search_screen` |  |
| ed/6 | Tab completes a file name, and a command name in command position | not counted | `session:c_ed_complete_file`, `session:c_ed_complete_command`, `session:c_ed_complete_names`, `session:c_ed_complete_after_ops`, `session:c_ed_complete_after_assign`, `session:c_ed_complete_slash_cmd` |  |
| ed/7 | Alt-B and Alt-F move by words | not counted | `session:c_ed_word_motion` |  |
| ed/8 | In a UTF-8 locale backspace erases one character, and the cursor moves by characters, whatever their byte length or width | not counted | `session:c_ed_utf8_erase`, `session:c_ed_utf8_left` |  |
| ed/9 | Ctrl-B, Ctrl-F, Ctrl-A, Ctrl-E and the terminal's Home and End keys move; Ctrl-W, Ctrl-U, Ctrl-K, Alt-D kill and Ctrl-Y puts the kill back | not counted | `session:c_ed_keys_abf`, `session:c_ed_home_end_keys`, `session:c_ed_ctrl_w`, `session:c_ed_ctrl_u_y`, `session:c_ed_ctrl_k_y`, `session:c_ed_alt_word`, `session:c_ed_insert_mid` |  |
| ed/10 | Backspace, Ctrl-H and Delete erase a character; Ctrl-V inserts the next key as itself | not counted | `session:c_ed_backspace_delete`, `session:c_ed_ctrl_v`, `session:c_ed_tab_literal` |  |
| ed/11 | A wide character takes two cells and a combining mark none: the cursor, erase and redraw count cells, and a wide character is never split at the margin | not counted | `session:c_ed_wide_insert`, `session:c_ed_wide_wrap`, `session:c_ed_wide_wrap_edit`, `session:c_ed_combining` |  |
| ed/12 | A line wider than the terminal wraps onto the next rows and is edited there | not counted | `session:c_ed_wrap_insert`, `session:c_ed_wrap_erase`, `session:c_ed_wrap_exact` |  |
| ed/13 | Ctrl-L clears the screen and redraws the prompt and the line | not counted | `session:c_ed_ctrl_l` |  |
| ed/14 | Ctrl-C abandons the line with $? 130 and runs an INT trap at once; with INT ignored the key does nothing | not counted | `session:c_ed_ctrl_c`, `session:c_ed_ctrl_c_trap`, `session:c_ed_ctrl_c_ignored`, `session:c_ed_ctrl_c_continued` |  |
| ed/15 | A command, exec, and the shell's exit find the terminal in the user's modes, after Ctrl-C too | not counted | `session:c_ed_mode_command`, `session:c_ed_mode_exec`, `session:c_ed_mode_after_ctrl_c` | and tools/session fails any pelt session that exits with the terminal's ICANON, ECHO or ISIG changed |
| ed/16 | A recalled line keeps its changes while another is shown, until a line is accepted | not counted | `session:c_ed_history_screen` |  |
| ed/17 | The arrow keys move and walk the history in vi insert mode too | not counted | `session:c_vi_arrows_insert` |  |
| ed/18 | The terminal's erase, kill, interrupt, end-of-file, word-erase and literal-next characters, as stty set them, act in the editor | not counted | `session:c_ed_stty_intr`, `session:c_ed_stty_erase`, `session:c_ed_stty_kill`, `session:c_ed_stty_werase`, `session:c_ed_stty_eof`, `session:c_ed_stty_lnext`, `session:c_vi_stty_intr`, `session:c_vi_stty_erase` |  |
| ed/19 | Ctrl-S and Ctrl-Q reach the editor (flow control is off while a line is edited) and never stop the shell | not counted | `session:c_ed_flow_stop` |  |
| ed/20 | A resize while a line is edited draws it again at the new width, and a WINCH trap still runs | not counted | `session:c_ed_resize_narrow`, `session:c_ed_resize_trap` |  |
| ed/21 | Tab completes a variable name after $ and ${ (closed with }) and inside "$ | not counted | `session:c_ed_complete_var`, `session:c_ed_complete_var_in_word`, `session:c_ed_complete_list_vars` |  |
| ed/22 | A directory completes with / and no space; a file, command or variable with a space when nothing follows the cursor; only the text before the cursor is completed | not counted | `session:c_ed_complete_dirs`, `session:c_ed_complete_mid_word`, `session:c_ed_complete_tilde`, `session:c_ed_complete_tilde_alone`, `session:c_ed_complete_abs`, `session:c_ed_complete_redirect`, `session:c_ed_complete_hidden` |  |
| ed/23 | A completed name is quoted so the shell reads it back as itself (blanks, $, quotes, metacharacters, pattern characters, a newline), and inside a quote the word opened it is closed | not counted | `session:c_ed_complete_quoting`, `session:c_ed_complete_newline`, `session:c_ed_complete_in_quotes` |  |
| ed/24 | Several matches complete to their longest common prefix with the bell; the second Tab in a row lists them in columns sized to the terminal, then the prompt and line are drawn again; a list taller than the window is asked about first; no match rings the bell | not counted | `session:c_ed_complete_lcp`, `session:c_ed_complete_list`, `session:c_ed_complete_list_wide`, `session:c_ed_complete_list_prompt`, `session:c_ed_complete_query`, `session:c_ed_complete_nomatch` |  |
| ed/25 | Tab completes in vi insert mode too; Ctrl-V then Tab inserts a tab | not counted | `session:c_vi_complete`, `session:c_ed_tab_literal`, `session:c_vi_insert_ctrl_v` |  |

### `test` (utility page)

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| test/1b | test -r, -w and -x answer for this process's access (a mode-000 file is unreadable to a user, an executable is executable), -L/-h for a link, -ef for two names of one file | met | `test/c_s_test_access` | from the script census: `test -x` is false for an executable regular file, `-w` true for a read-only one, `-r` true for a mode-000 one, `-L`/`-h` false for a symbolic link, `-ef` false for two links to one file (XCU test). The most-counted gap: git's test-lib, ltmain.sh, debconf's confmodule, every init script, `service`, `which`. Since sh07 the primaries read `fs_stat`/`fs_lstat` and decide access by the shell's own effective ids (`/proc/self/status`, else `id`); a read-only or noexec mount, ACLs and capabilities are where this can still part from access(2) (W07). |

### `umask` (utility page)

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| umask/4 | umask sets the mask that files made by the shell and its children receive, and reports it in octal and with -S | met | `umask/c_s_umask_set` | from the script census (sh06): `umask` was not implemented ("not supported yet", status 2) (XCU umask), and install-sh, mkinstalldirs, config.guess, lesspipe and two Debian postinst scripts stopped or misbehaved on it; a built-in since sh13 (wolf 0.2.28's `os_umask`). |

### 2.15 Special built-ins

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| trap/17 | trap takes a condition as a signal number for every signal it takes by name (1 2 13 15, 14), and lists it by name | met | `signal/c_s_trap_by_number`, `signal/trap_numbers_common` | from the script census: `trap action 13` (a signal number with no wolf meaning) is refused with "no such condition" and status 1 where dash and bash record it (XCU 2.15 trap, XSI numbers). `trap action PIPE` by name is accepted. Seen in config.guess, test-driver, tap-driver.sh, ylwrap, configure. Since sh07 13 and the other numbers every host agrees on (4, 5, 8, 11) are taken and listed; catching SIGPIPE still waits on wolf-lang#679. |

### 2.14 Pattern matching

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| 2.14.1/8 | A bracket expression holding a slash matches a slash in a case pattern and in the four trim forms (the explicit-slash rule is for file names only) | met | `glob/c_s_bracket_slash_case` | from the script census: `case` and ${x#pat}: a bracket expression that contains `/` matches a slash (XCU 2.14.1; the explicit-slash rule of 2.14.3 is for pathname expansion only). Stops every autoconf configure at its directory check; also ylwrap. Fixed in sh07: the slash rule is applied only to pathname expansion. |

### 2.13 Execution environment

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| 2.13/12 | A pipeline stage inside a command substitution writes to a descriptor the substitution duplicated (exec 4>&1), not to the shell's own output | met | `redir/c_s_cmdsub_fd_pipeline` | from the script census: In `$( exec 4>&1; { echo x >&4; } \| cmd >&3 )` the stage's write to descriptor 4 does not reach the substitution (it is empty) (XCU 2.7.5, 2.12). zdiff, zgrep and xzgrep read a decompressor's exit status this way and fail. |

### 2.5 Parameters and variables

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| 2.5.2/16 | Unquoted $* on the right of an assignment or as a case word joins with the first character of IFS | met | `param/c_s_star_assign_ifs`, `param/at_star_nosplit` | from the script census: Unquoted `$*` on the right of an assignment (and as a `case` word) joins with nothing instead of the first character of IFS (XCU 2.5.2). configure computes host_os as `linuxgnu`, so every `*-gnu*` host check takes its default arm (two checks answer "guessing no", two extra checks run). Fixed in sh07. |

### 2.2 Quoting

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| 2.2/1 | Any byte but NUL is data: bytes above 0x7f pass unchanged to a program's arguments, file names, read, command substitution and here-documents | pending (non-utf8-bytes) | `quote/c_s_high_bytes`, `quote/utf8_bytes` | from the script census: Every byte above 0x7f becomes `?` when a word is handed to a program as an argument or a file name, when `read` reads it, and in a here-document (XCU 2.2: only NUL is excluded). update-ca-certificates loses a certificate whose file name is not ASCII. Since sh07 valid UTF-8 passes unchanged everywhere (quote/utf8_bytes); a byte that is not UTF-8 still cannot be a wolf `str` (W06), so the statement stays pending on quote/c_s_high_bytes. |

### 2.15 Special built-ins

| id | statement | verdict | cases | note |
|---|---|---|---|---|
| dot/8 | . reads any readable file, not only a regular one: /dev/null is an empty script, a FIFO is read | met | `builtin/c_s_dot_special_file`, `builtin/dot_fifo_program` | from the script census: `. /dev/null` (and a FIFO, /dev/stdin) is "not found", which ends a non-interactive shell with status 2 (XCU 2.15 dot). pfetch does `. "${PF_SOURCE:-/dev/null}"` and prints nothing. Since sh07 `.` reads /dev/null and a FIFO (builtin/dot_fifo_program); builtin/c_s_dot_special_file has the shell write the FIFO from an in-process background subshell, which waits on fork. |
