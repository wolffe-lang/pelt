# sh12 — the history (`fc`, HISTFILE, HISTSIZE, Ctrl-R, vi `v`)

Contract: `sprints/pelt/12-the-history/sh12-the-history.md` in the
planning repo (ruling #69 R4: no `!!` history expansion). This file is
the lane's record: §1 to §3 are committed before the first change under
`src/`, `tools/` or `tests/`, and the evidence index (§4) is filled in
as the work lands.

## 1. Forbidden

Clean-room (ruling #43): no shell's or line-editing library's source is
read or searched for. The facts come from POSIX.1-2024 (XCU `fc`; XCU
`sh`: Command History List, `HISTFILE`, `HISTSIZE`, vi-mode `v`, `k j G
/`; XCU 2.5.3 `PS1`'s exclamation-mark expansion), wolf's `spec/11-os.md`
at the `v0.2.28` tag, and black-box sessions of `dash` 0.5.13.4 and
`bash --posix -i` 5.3 as a user sees them (`notes/sh12-evidence/probe/`).
No `extern "c"`; no history expansion (`!!`, `!n`, `^old^new`: R4). No
merge, no tag, no issue filed or closed, no package installed, no other
lane's CI run cancelled, nothing under `~/.claude`; no attribution
trailers. Toolchain from the release archives by digest. kasumi jobs by
`setsid` with the pid recorded, killed by that pid only; scratch under
`~/lanes/sh12/`; no build on nomad-1. Strict evidence (#571). sh08
(memory) runs beside this lane in pelt: its areas (`exec.lu`'s fast
path, the rss gates, `session-rss`, `loop-rss`) are not touched here;
whichever lands second rebases.

## 2. Inputs, verified (2026-10-12, re-derived before any change)

| input | contract says | measured | drift |
|---|---|---|---|
| pelt trunk | `96828ac` | `origin/trunk` = `96828ac` (sh13 merged); branch `sh12` cut from it | none |
| toolchain | 0.2.28 | `wolf-toolchain.toml`: wolf 0.2.28 `f71ece8e`, lupin 0.1.51 `f72e78d`, std `98e1b7b`; `tools/fetch-toolchain` on kasumi verified the linux x86-64 digests and staged them | none |
| sessions at trunk | — | `tools/session --bin target/release` on kasumi: **pass 171, fail 0, pending 26 (4 PEND-ok)** (`~/lanes/sh12/session-base.log` on kasumi) | none |
| sh11's seam | in-memory history walk; `c_vi_v` pending; the Ctrl-R case | `src/sh/edit.lu`: a ring of `HISTSIZE` lines (128 when unset) in `EdKeep`, `hist_add` called per physical line from `interact.next_line`; Up/Down, vi `k j - + G / ? n N` walk it; vi `v` alerts. Pending on "history": `c_hist_fc_edit`, `c_hist_fc_list`, `c_hist_fc_s`, `c_ps1_bang`, `c_vi_v`; on "history search": `c_ed_search`; the diff case `fc/c_noninteractive` (passing only because no `fc` exists) | `hist_add` is per physical line: a command continued over `PS2` lines becomes several entries — fixed here (§3.1) |
| `c_hist_fc_edit` | — | its editor is `sed -i s/me/done/`: GNU sed's form; macOS's `sed -i` takes the next word as a backup suffix, so the case cannot pass there whatever pelt does | re-recorded with a stand-in editor in `.files/` (§3.6) |
| the clause table | — | `fc/1`–`fc/4`, `sh/18`, `sh/37`, `2.5.3/10`, `ed/5` name the history cases; `sh/18`'s note: "HISTFILE across two sessions has no case" | answered by a witness (§3.6) |
| POSIX `fc` | — | `~/lanes/sh06/posix/fc.txt` (Issue 8): `%d\t%s\n`, continuation lines `\t%s\n`; `-n` `\t%s\n`; the fc that edits is not entered; the edited lines are entered and run; a non-zero editor status suppresses both; out-of-range first/last substitute the oldest or newest; the default 16; `FCEDIT`, else `ed` | — |
| dash 0.5.13.4 | — | **has `fc` when interactive** (built with libedit); non-interactive `fc -l`: "history not active", status 2. Lists `%5d %s` (not POSIX's tab), `-n` without the tab, keeps a multi-line command as one entry, enters the `fc -s` line itself (POSIX says it is not), reads no `HISTFILE`, no `!` in `PS1` (probes p01–p03, d06–d08) | dash is not the oracle for history; bash is |
| bash --posix 5.3 | — | `%d\t%s`; the `fc` that edits is not entered and the result is; `fc -s` and `fc -e` echo the commands to standard error before running them; a failed editor runs nothing; `fc -l 99` / `fc -l -99` (beyond either end) start at the OLDEST (dash agrees); `fc -l 2 99` ends at the newest before the `fc`; `0` is the previous command, `-0` the `fc` itself; `+2` is refused ("no command found"; POSIX allows `[+]number`); a multi-line command is entered joined with `;` (POSIX's `\t%s` continuation format implies lines are kept); `HISTSIZE` takes effect at once; `HISTFILE` read at start, numbers continue after it; `PS1`'s `!` is the next number, `!!` one `!`, applied before parameter expansion (`x='!'; PS1='$x>'` shows `!>`; `'${y:-!}>'` shows `9>`) (probes p01–p07) | where bash and POSIX part, pelt takes POSIX and says so |
| wolf 0.2.28 surface | — | `spec/11-os.md` at `v0.2.28`: `fs_open_mode` 2 append (create), 4 create-new (exclusive); `fs_open_perm(path, open, mode)` (mode less the umask from its first instant); `fs_rename` (replaces); `fs_remove`; `fs_stat` (size, inode); `os_proc_pid` | none |
| kasumi | near full | 35 GB free of 928 GB (97%); load 27 on 16 cpus while measuring (other lanes) | stated |

## 3. Prediction (committed before the first change under `src/`)

### 3.1 The history list (`src/sh/hist.lu`, new)

- **Entries are complete commands as typed**, entered by `run_stdin`
  once a command is complete (not per physical line, as sh11 did): a
  `for` loop typed over three `PS2` lines is one entry of three lines.
  Empty and all-blank commands and a line abandoned by Ctrl-C are not
  entered. Entered only by an interactive shell; a non-interactive
  shell has no history and `fc` there fails with status 2 (dash).
- **Numbers**: each entry gets the next number (1 for the first a
  session ever sees, after the entries read from `HISTFILE`); numbers
  never wrap (POSIX "may"). The list keeps the newest `HISTSIZE`
  entries (a positive decimal ≤ 32767, else 128), read at every entry
  so a change takes effect at the next command (bash).
- **The current command**: the line being run is the newest entry when
  `fc` runs from it; `-1` is the one before it (POSIX's "previous"),
  `-0` the `fc` line itself, `0` the previous (bash), `+n`/`n` absolute
  (POSIX `[+]number`; bash refuses `+n`), a string the newest entry
  before the `fc` starting with it.

### 3.2 `fc` (a regular built-in)

- `fc -l [-nr] [first [last]]`: `%d\t%s\n`, continuation lines
  `\t%s\n`, `-n` `\t%s\n` (POSIX; bash's format). Defaults: the previous
  16 (first `-16` from the `fc` line, last the previous). A `first`
  beyond either end of the list is the oldest (bash and dash agree,
  measured); a `last` beyond the newest is the previous command, before
  the oldest is the oldest. `first` newer than `last` lists in reverse
  (as `-r`); `-r` reverses again.
- `fc -s [old=new] [first]` (and the historical `fc -e - …`): the
  command (default the previous), `old` replaced once by `new`; the `fc`
  line is removed from the list, the command written to standard error,
  entered, and run; the status is its status.
- `fc [-r] [-e editor] [first [last]]`: the commands (default the
  previous one) written one after another to a new file (`fs_open_perm`
  create-new, mode 0600, in `TMPDIR` or `/tmp`, named from the pid and a
  counter), the editor run as the command `editor path` (so `-e 'sed
  -f x'` works, as in bash) with `fc`'s redirections; a non-zero status
  runs nothing and enters nothing; otherwise the file is read, the `fc`
  line removed, the text written to standard error, each complete
  command entered, and the text run as `eval` runs it. The editor is
  `-e`, else `FCEDIT` if set and not empty, else `ed`. The file is
  removed in every case.
- Errors (pelt's own words): no such command (status 1), a bad option
  or operand (2), the editor's file not creatable (1); the shell goes
  on (a regular built-in). A re-executed `fc` that re-executes itself
  stops at a depth of 32 (status 1).

### 3.3 HISTFILE and HISTSIZE

- **Initialised** right after the `ENV` file has run, before the first
  prompt (POSIX allows it; the first `PS1` `!` needs the count). The
  path: `HISTFILE` if set (empty: no file), else `$HOME/.sh_history`
  (POSIX's suggestion) when `HOME` is set. Read once at that point;
  later changes to `HISTFILE` do nothing (POSIX "may").
- **Format** (POSIX: unspecified): one entry a line, UTF-8 text; a
  backslash written `\\` and a newline inside an entry `\n`, so a
  multi-line command is one line of the file; a backslash before any
  other byte is read as itself (so a file of plain lines from another
  shell reads as written). A file that is not text (a NUL byte, or not
  UTF-8) is not ours: it is neither read nor written, and the history
  is kept in memory only (POSIX's "unspecified mechanism"). So is a
  path that cannot be read or created; nothing is printed.
- **Written** as each command is entered: one append (`fs_open_mode`
  2, one `fs_write_chunk` of the whole encoded line, so concurrent
  appends from several shells do not interleave). A new file is created
  0600 (`fs_open_perm`).
- **Shared**: before each prompt and before `fc`, the file's size and
  inode are read (`fs_stat`); bytes another shell appended since are
  read and entered (numbered in this shell's sequence); a file replaced
  under us (another shell truncated it) is read again from the start.
  So a command typed in one shell is in the other's `fc -l` and Up at
  its next prompt (POSIX's rationale: "commands that are entered in one
  shell shall be accessible by the other shell"; how updates interact
  is unspecified).
- **Truncated** oldest first: at initialisation when the file holds
  more than `HISTSIZE` entries, and during a session when it reaches
  twice `HISTSIZE`, the newest `HISTSIZE` are written to a new file
  beside it and renamed over it (`fs_rename`). An append another shell
  makes between that read and the rename is lost (stated, unspecified
  by POSIX).

### 3.4 `PS1`'s `!` (XCU 2.5.3)

Before parameter expansion (bash's order, measured): each `!` becomes
the number the next command will get, `!!` one `!`. Only `PS1`, only
an interactive shell. `PS2` untouched.

### 3.5 The editor

- **Ctrl-R** (emacs mode): incremental search backwards through the
  history, plain substring, the newest match first. The line shows
  pelt's own status, `(search 'pat') ` before the matched line, the
  cursor on the match; a failed search shows `(failed search 'pat') `
  and rings the bell. Keys: a character extends the pattern; Ctrl-R
  the next older match (on an empty pattern, the last pattern searched
  this session); Backspace shortens the pattern and searches again from
  the newest; Enter runs the matched line; Ctrl-G restores the line as
  it was before Ctrl-R; Ctrl-C abandons the line as always; any other
  key ends the search with the match as the line shown (as Up would
  leave it) and then acts. Ctrl-S (forward) is out of reach: IXON keeps
  it (sh11, W05).
- **vi `[number]v`** (XCU `sh`): the line (or command `number`) is
  edited with `vi` (POSIX names vi; `VISUAL`/`EDITOR` are not read)
  through `fc`'s editing path: the commands that come back are written
  to standard error, entered and run; a non-zero status runs nothing.
  The line itself is not entered (the edited text is).
- **vi `G` with a count** goes to that history NUMBER (XCU), not the
  countth oldest line.

### 3.6 Cases and witnesses

- **Move to pass**: `c_hist_fc_list`, `c_hist_fc_s`, `c_ps1_bang`,
  `c_ed_search`, `c_vi_v`, `c_hist_fc_edit` (after its editor becomes a
  stand-in script, re-recorded from bash), and the diff case
  `fc/c_noninteractive` (pending mark cleared). Pending after: **20**
  (the 26 less these six).
- **New session cases, recorded from `bash --posix -i`**, about 20:
  `fc -l` defaults, ranges, reversal, strings, clamping, `-n`; `fc -s`
  with and without `old=new`, by string, the result entered and the
  `fc` not; `fc -e` with a failing editor, two commands, `FCEDIT`; an
  unknown command; `HISTSIZE=3`; `HISTFILE` read at start
  (`.files/home/` holds the same lines as `.bash_history` and
  `.sh_history`, so each shell reads its own); `PS1='!> '`; Ctrl-R
  again, edited, aborted, Backspace; `2v`; `v` with a failing editor.
  Screens for Ctrl-R are pelt's own text, written by hand
  (`screen_by=hand`), said so in `why=`.
- **Where bash and POSIX part** (no session case can pin pelt there,
  the oracle being bash): a multi-line entry, `+n`. Those are in the
  table checks (`src/sh/selftest.lu`): operand resolution and clamping,
  the list format with continuation lines, the file encoding and its
  reading of foreign plain lines.
- **`tools/hist-witness`** (new, CI on both tiers of both hosts): pelt
  on ptys with a `HISTFILE` in a scratch directory — (1) commands
  written as typed (a backslash, a multi-line command), (2) read at the
  next start (`fc -l` numbers, Up), (3) two shells at once on one file:
  a command typed in A is in B's `fc -l` and Up at B's next prompt, (4)
  a 40-entry file with `HISTSIZE=5`: 5 entries at start, and twice
  `HISTSIZE` during a session truncates, (5) an unwritable path and a
  binary file: history in memory, the file untouched, nothing printed,
  (6) `HISTFILE` unset: `$HOME/.sh_history` created 0600.
- **Predicted counts**: sessions **pass 171 + 6 + new (~20), fail 0,
  pending 20** on both tiers of linux and macOS; the corpus unchanged
  but `fc/c_noninteractive` no longer pending; the clause table gains
  `fc/1`–`fc/4`, `sh/18`, `sh/37`, `2.5.3/10` met.
- **Planted reds in CI** (branch `sh12-plant`, never merged): (a) the
  append skipped — `hist-witness` red on (1)–(3); (b) `-1` resolved one
  too far back — the `fc` session cases red.

### 3.7 Numbers

- **Memory** (`tools/session-rss -n 20000`, kasumi, release; HOME=`/`,
  so no file): within **±16 B a command** of trunk (the entry is the
  same string sh11 kept). With a `HISTFILE` (through `env HISTFILE=…`):
  at most **64 B a command** over no file, the file's bytes read and
  written inside regions.
- **Latency** (Enter to the next prompt, `:`): with a `HISTFILE`, at
  most **+0.15 ms** median over none (one `fs_stat`, one open-append-
  close a command). Ctrl-R over a full 32,767-entry history: a key
  answered in under **10 ms** median (release).
- **Start**: reading a 32,767-entry file adds under **60 ms** (release)
  to an interactive start.
- **Wrong predictions will be reported as such in §5.**

## 4. Evidence index

Hosts: kasumi (linux x86-64, CachyOS, 16 cpus, shared: load 6–27
while measuring) for every build, session and measurement; nomad-1 for
editing only (no build). Toolchain: wolf 0.2.28 `f71ece8e`, lupin
0.1.51 `f72e78d`, std `98e1b7b` (the pin, unchanged). Logs under
`notes/sh12-evidence/logs/`; black-box probes of dash and bash under
`notes/sh12-evidence/probe/` (`probe.log`, `d09.log`, `nonint.log`).

### 4.1 What was built

- `src/sh/hist.lu` (new, `025d7e1`) — the history list (a ring of
  `HISTSIZE` complete commands, numbered), `HISTFILE` (read after `ENV`,
  appended before the next prompt and at the end, other shells' appends
  read before each prompt, cut to `HISTSIZE` at start and at twice
  `HISTSIZE`), `fc` (`-l -n -r -s -e`, `-e -`, `old=new`, the operands
  and their clamping), `PS1`'s `!`, and `hist_visual` (vi `v`).
- `src/sh/edit.lu` (`bdc13b6`) — the editor reads `sh.hist`'s list;
  Ctrl-R (`isearch`, pelt's own `(search 'pat') ` / `(failed search
  'pat') `); vi `[number]v` ends the line for `hist_visual`; vi `G` with a
  count goes to that history number.
- `src/sh/interact.lu` (`4b853b0`) — a command is entered once it is
  complete (sh11 entered each physical line), the file read after `ENV`
  and brought up to date before each `PS1`, `PS1`'s `!` before the other
  expansions, vi `v` run through `fc`'s editing path.
- `fc` a regular built-in (`35b7989`); `PS1`, `PS2`, `PS4` from the
  environment win over the defaults, as in dash (`78e1ec1`; found here:
  pelt overwrote them, so no session could set `PS1` by `env=`).
- Table checks (`2c7df10`): `fc`'s operands and clamping, the list
  format, `-r` against reversed operands, a multi-line entry, the file's
  lines, `PS1`'s `!` — the places bash and POSIX part, pinned to POSIX.
  Seen to fail when an expectation is broken (`-1` wanted as 3: "fc_number(-1,
  first=true) = 4, want 3", kasumi, before the commit).
- `tools/hist-witness` (`3f8fc79`), in CI on both tiers (`47848a4`).
- Sessions (`4203394`, `9ffd8de`, `df48430`, `fa29d18`, `a95d65f`,
  `0e208e0`), the diff case `param/c_ps_from_env` (`881efb5`),
  `fc/c_noninteractive` out of pending (`6fef2d9`), the clause table
  (`c2549b4`), `docs/CENSUS.md` (`4becba5`), `docs/PLAN.md` (`b08cdb3`),
  README (`6921b7c`).

### 4.2 Each feature against dash and bash --posix

| feature | pelt | bash --posix 5.3 | dash 0.5.13.4 |
|---|---|---|---|
| `fc -l` format | `%d\t%s`, continuation `\t%s` (POSIX) | `%d\t%s` | `%5d %s`; `-n` with no tab |
| a multi-line command | one entry, its lines kept | one entry joined with `;` | one entry, lines kept |
| the `fc` that edits / `-s` | not entered; the result is (POSIX) | same | enters the `fc -s` line |
| `fc -s`, `fc -e` | the commands written to standard error, then run | same | same |
| a failing editor | nothing run, nothing entered | same | — |
| `first` beyond either end | the oldest | the oldest | the oldest |
| `-r` with first newer than last | the two cancel (POSIX's example) | does not cancel | cancels |
| `-0` alone | from the `fc` line back to the previous | only the `fc` line | as pelt |
| `+n` | command n (POSIX `[+]number`) | "no command found" | — |
| non-interactive `fc` | status 2, the shell goes on | status 0, nothing | status 2 |
| `HISTFILE` | read at start, appended per command, shared, cut to `HISTSIZE`; default `$HOME/.sh_history` | read at start, written at exit; `.bash_history` | not read |
| `HISTSIZE` | at once | at once | at once (its own numbering) |
| `PS1` `!` / `!!` | the next number / `!`, before parameter expansion | same | not expanded |
| Ctrl-R | pelt's own screen; Enter runs, Ctrl-G restores, Backspace searches again, any other key ends and acts | the same keys (the `c_ed_search*` transcripts); its own screen | not measured |
| vi `[number]v` | `vi` from `PATH` (POSIX names vi) on the line or command `number`, through `fc`'s path | the same with the cases' stand-in `vi` (`c_vi_v*`) | not measured |
| `PS1`/`PS2`/`PS4` from the environment | imported (new here) | `PS1`, `PS2` not imported non-interactively | imported |

### 4.3 Session and corpus results

| head | where | sessions pass / fail / pending (PEND-ok) | corpus | log |
|---|---|---|---|---|
| `96828ac` trunk | kasumi, release and native | 171 / 0 / 26 (4) | 835 / 0 / 99 (8) | `logs/base-96828ac/` |
| `806b7d2` + `0e208e0`'s transcripts | kasumi, native and release | 197 / 0 / 20 (4) (the gauntlet's own run: 195 / 2, the two transcripts recorded before two steps were dropped; re-recorded and both pass on both tiers) | 837 / 0 / 98 (8), both tiers | `logs/g1-806b7d2/` |
| idem | kasumi, release, `taskset -c 0-3` | 197 / 0 / 20 (4) | — | `logs/g1-806b7d2/session-release-taskset.log` |

Every other gate in that gauntlet exits 0: fmt, the clause table,
the width table, `wolf test`, glob-rss, loop-rss, exec-witness,
edit-witness and hist-witness (6 of 6) on both tiers, both harness
self-tests (`logs/g1-806b7d2/summary`). Clause census: **439 of 545
met (81.3%)**, trunk 431 of 544 (80.0%).

### 4.4 Memory and speed (kasumi, quiet only by luck; load 6–16)

`tools/session-rss -n 20000` (`logs/measure/`, `logs/base-96828ac/`),
KB at 0 → 20,000 commands, release:

| binary | KB | per command |
|---|---|---|
| trunk `96828ac` (no file: `HOME=/`) | 3,116 → 10,096 | 357.4 B |
| head, no file | 3,156 → 10,124 | 356.8 B (−0.6 B) |
| head, `HISTFILE` in scratch (`env HISTFILE=…`) | 3,156 → 10,160 | 358.6 B (+1.8 B over no file); the file 162 lines at the end (`HISTSIZE` 128, cut at 256) |

`notes/sh12-evidence/hist-bench.py` (`logs/measure/bench-*.log`):

| | release | native |
|---|---|---|
| Enter to the next prompt, `:`, no file: median / p99 (2,000 lines) | 0.012 / 0.027 ms | 0.019 / 0.057 ms |
| the same with a `HISTFILE` | 0.017 / 0.066 ms | 0.024 / 0.091 ms |
| start to the first prompt, empty file / 32,767 entries | 1.0 / 5.1 ms (+4.1) | 1.1 / 7.7 ms (+6.6) |
| Ctrl-R, a key no line holds, over 32,767 entries: median / p99 | 5.54 / 5.71 ms | 9.49 / 10.05 ms |
