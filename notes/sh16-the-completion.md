# sh16 — the completion (ruling #69 R3: files, commands, variables)

Contract: `sprints/pelt/16-the-completion/sh16-the-completion.md` in the
planning repo (`60ed105`). This file is the lane's record: §1 to §3 are
committed before the first change under `src/`, `tools/` or `tests/`;
the evidence index (§4) is filled in as the work lands.

## 1. Forbidden

As the contract. No shell's source is read or searched for (dash, bash,
zsh, mksh, busybox, readline, libedit or any other), nor a libc's or a
kernel's (rulings #42–#45). Behaviour comes from POSIX.1-2024 XCU `sh`
(Command Line Editing, vi-mode), the shells' manuals as documentation,
and black-box runs of the reference binaries: **bash 5.2.37, mksh 59c
and dash 0.5.12 in a throwaway Debian trixie container on kasumi**
(`notes/sh16-evidence/probe/probe.py`, the session harness driving each
binary through a fresh pty), and the oracles of record on kasumi (dash
0.5.13.4, bash 5.3.20 as `bash --posix`, `tests/diff/ORACLE`) through
`tools/session-record`, as every earlier session case was recorded. mksh
was never installed on a host; its container image is removed at the
end. A signal's meaning is named (`std.signal`); no literal signal bit
or mode bit. The toolchain from the release archives by digest, each
read twice. No merge, no tag, no issue filed or closed (listed in the
report), no package installed on a host, no other lane's CI run
cancelled, nothing under `~/.claude`, no attribution trailers. No build
on nomad-1: kasumi, under `~/lanes/sh16/` (one target directory per
tree, pruned), detached jobs by `setsid` with the pid recorded and
stopped by that pid only. Scratch under `~/lanes/sh16/`, never `/tmp`.
Strict evidence (#571): `wolf build` exit 2 is a compile error; terminal
tests also under `taskset -c 0-3`. If the harness refuses an action,
the lane stops and reports.

## 2. Inputs, verified (2026-10-15, re-derived before any change)

| input | contract says | measured | drift |
|---|---|---|---|
| pelt trunk | `7dd3304` | `origin/trunk` = `7dd330458ee3…` (sh15's merge); branch `sh16` cut from it; no open PR | none |
| wolf 0.2.30 | `v0.2.30` at `1b37f368` | the tag object `ffb7c5b3…` → commit `1b37f368228d…`, read twice; `wolf 0.2.30 (wolfgang, pin 1b37f36)` | none |
| lupin 0.1.53 | `v0.1.53` at `7896edd` | the tag object `83631915…` → `7896eddc17fd…`, read twice; `lupin 0.1.53 (wolf-interp, reference interpreter at pin 294d626)` | none |
| the digests | by digest, each read twice | the release API read twice for all six archives (equal to `wolf-toolchain.toml`); the linux x86-64 pair downloaded on kasumi and hashed twice: wolf `4e55b39e…`, lupin `5db55332…` (`notes/sh16-evidence/logs/fetch.log`) | none |
| the bundled std | wolf-std `fd6bcdc` | the archive's `STD-REV` and the pin both `fd6bcdcb1dfe…` | none |
| ruling #69 R3 | files, commands, variables, not programmable | `sprints/pelt/index.md`: "R3 files/commands/variables" | none |
| the editor at trunk | Tab inserts a literal tab | `src/sh/edit.lu` `is_char_key`: "a character to insert (a tab included)"; emacs and vi insert mode both insert 9, shown `^I`; Ctrl-V (or the `lnext` character) inserts the next byte | none |
| the pending cases | — | `c_ed_complete_command`, `c_ed_complete_file`, pending `completion`, recorded from `bash --posix -i` 5.3 (sh06) | none |
| aliases | "aliases if pelt has them" | pelt has none: `alias`, `unalias`, `type` answer "not supported yet" (`builtin.lu`); P03 open | aliases are out |
| vi command mode `\` `*` `=` | only if dash's vi mode has them | dash (0.5.13.4 on kasumi, 0.5.12 in the container) accepts `set -o vi` and lists it on, but has **no editor at all** (built without libedit: the probe's Tab, Ctrl-A and ESC reach the terminal's own line discipline). POSIX defines `\` (pathname completion), `*` and `=`; pelt has had all three since sh11 (pathname expansion of the bigword, `vi_expand`) | unchanged here; named in §8 |
| the baseline | — | trunk `7dd3304` on kasumi, every gate (`logs/base.status`): corpus 880/0/80 on both tiers and under `taskset -c 0-3`; sessions 215/0/16; statements 451 of 545 | none |
| kasumi | `/home` ~30G | 38G free at the start; no mksh on any host (the container has it) | none |

### 2.1 What the references do (black-box, `logs/probe-refs.txt`, `probe-refs2.txt`, `probe-mksh.txt`)

Every probe types into a fresh pty with `PATH=/usr/bin:/bin`, a scratch
`HOME` and working directory, `LC_ALL=C`. dash completes nothing in any
row (its Tab is a literal tab), so dash is left out of the table.
mksh edits only when its standard error is the terminal, so it ran as
`exec mksh -i +m 2>&0`.

| row | bash 5.2 `--posix` (emacs) | mksh 59c (emacs) |
|---|---|---|
| unique command (`unam`) | `uname ` (space) | `uname ` |
| function, builtin, reserved word (`f_mi`, `alia`, `whil`) | completed, space | completed, space |
| several commands, first Tab | the longest common prefix and a bell | the prefix, and the list at once |
| the Tab after that | another bell if the first Tab made progress; a list on the Tab after a Tab that made none | the list again |
| empty command word, Tab Tab | bell, then "Display all 353 possibilities? (y or n)" | bell, bell (nothing listed) |
| no match | bell | bell |
| after `|`, `;`, `&&`, `$(` | a command | a command |
| after `FOO=1 `, after `if ` | **nothing** (bell) | **nothing** (bell) |
| a command word with a slash (`./sc`) | files: only directories and executables (`scdir/ script.sh`) | every file |
| file, unique | completed, space | completed, space |
| directory | `sub/`, no space; Tab again goes on inside it | the same |
| name with a space, `$`, `'`, `"`, `&;()` | backslash before each (`my\ file`, `a\$b`, `q\'uote`) | the same |
| name with a newline | the whole word rewritten `'nl<NL>name'` | `nl'<NL>'name` |
| `st*` typed | the `*` taken literally: `st\*ar` | `*` as a pattern: lists both, the line loses the `*` |
| typed inside `"my` or `'my` | `"my file" `, `'my file' ` (the quote closed) | backslashes inside the quote (wrong) |
| cursor inside a word (`uniq|ZZ`) | completes the text before the cursor: `unique_file_name|ZZ`, no space | bell |
| cursor on a blank after the word | completes, no extra space | completes, adds a space |
| `~/do` | `~/docs/` (the tilde kept) | `/abs/home/docs/` (the tilde expanded) |
| `~` alone | bell (user names) | the home directory expanded, `/` |
| `/us`, `/usr/bi` | `/usr/`, `/usr/bin/` | the same |
| `cat <uniq`, `>uniq`, `FOO=uniq` | a file name each | a file name each |
| hidden files, empty word | listed (`.hid1 vis`) | not offered (`vis ` completed) |
| `.h` | `.hid1 ` | `.hid1 ` |
| `$ZQV_O`, `${ZQV_O`, `"$ZQV_O` | `$ZQV_ONE `, `${ZQV_ONE} `, `"$ZQV_ONE" ` | no variable completion (bell); `$ZQV_ONE` + Tab **expands** it to its value |
| `a$ZQV_O` (inside a word) | bell | no |
| `$` Tab Tab | every variable listed, `$NAME` | bell |
| the list | below the line, column-major (down, then across), column width the widest name plus 2 cells, columns = (width − 1) / that; directories with `/`, variables with `$`; the prompt and line drawn again below | the same layout (the last column not padded), columns = width / width-per-column |
| more than 100 items | asks "Display all N possibilities? (y or n)" first | lists them |
| taller than the window | lists them all (no pager) | the same |
| wide names (`été`, `日本`) | columns by cells | garbled |
| vi insert mode Tab | **inserts a tab** (`--posix`) | completes (`vi-tabcomplete` on) |
| vi command `\`, `*`, `=` | `\` completes, `*` inserts all, `=` lists | the same |
| Ctrl-V Tab | a literal tab | a literal tab |

## 3. Prediction (committed before the first change)

### 3.1 The design

- **Tab (9) completes** in emacs mode and vi insert mode (the contract;
  mksh does; bash `--posix` inserts a tab in vi insert mode). Ctrl-V
  (or the terminal's `lnext`) then Tab still inserts a tab. vi command
  mode keeps sh11's POSIX `\`, `*`, `=`.
- **What is completed** is the text of the current word up to the
  cursor; text after the cursor stays. A small lexer reads the line up
  to the cursor (blanks, `; & | ( )` and backquote end a word and start
  a command; `<` `>` end a word and make the next a file; `\`, `'…'`,
  `"…"` quote) and decides:
  - **a variable** when the word ends in an unquoted or double-quoted
    `$name` or `${name` (`name` may be empty): the shell's variable
    names. Anywhere in a word (bash only at its start; mksh never).
  - **a command** when the word is in command position and has no `/`:
    pelt's built-ins, the reserved words, the functions, and every file
    with an execute bit in a `PATH` directory, without duplicates.
    Command position: the start of the line, after `; & | ( ` and
    backquote and `$(`, after an assignment word, and after a reserved
    word that a command follows (`if then else elif while until do !
    {`). **Both references complete nothing after `FOO=1 ` or `if `;
    pelt does**, because XCU 2.9.1 makes that word the command name.
  - **a file** otherwise: the directory part as typed (`/` absolute,
    `~/` and a lone `~` from `HOME`, the tilde kept in the line as bash
    keeps it), names starting with the rest. Names starting with `.` only
    when the rest starts with `.` (pathname expansion's rule, as mksh;
    bash offers them). In command position (a word with a `/`) only
    directories and executable files (bash). After `NAME=` in command
    position, the value is completed as a file (both).
- **A unique match** is completed in place: a directory with `/`; a file,
  command or variable with a space when the cursor is at the end of the
  line (none when text follows, bash), after the closing `}` of `${` and
  the closing quote of a quote the word opened (bash).
- **Several matches**: the longest common prefix is inserted and the
  bell rung (bash). **The next Tab in a row lists them** (the
  contract's "a second Tab"; bash needs a third when the first made
  progress, mksh lists at the first), and every Tab in a row after it
  lists again. Any other key ends the row.
- **No match**: the bell, nothing else (both).
- **Quoting what is inserted**, so the shell reads the name back as it
  is: outside quotes a backslash before a blank and each of
  `| & ; < > ( ) $ \` \ " ' * ? [`, and before a `~` or `#` that starts
  the word; a newline as `'<NL>'` (mksh's shape; bash rewrites the whole
  word). Inside `"…"` a backslash before `$ \` " \`; inside `'…'` a `'`
  as `'\''`. A typed `*` is part of the name (bash).
- **The list**: the cursor goes below the line, the names sorted by byte
  in columns down then across, each column the widest name's cells plus
  2 (wide characters by `sh.width`), as many columns as fit in the
  width less one (bash's count), the last column of a row not padded
  (mksh); then the whole prompt and the line again, the cursor where it
  was. Files show `/` after a directory, variables their `$`. **When the
  list would be taller than the window less one row** (`os_term_size`'s
  rows; 24 when never told) pelt asks first, in its own words, and lists
  only on `y`, `Y` or a space (bash asks above 100 items; mksh never).
- **Cost**: the names come when Tab is pressed: one directory read per
  `PATH` entry (one `fs_stat` per name that matches the prefix) for a
  command, one for a file. An idle prompt does nothing new: still 0
  context switches in 10 s.

### 3.2 Tests

- **The two pending cases leave pending** (`c_ed_complete_command`,
  `c_ed_complete_file`), against their bash transcripts.
- **New session cases** (about 20), recorded from `bash --posix -i` on
  kasumi where pelt's standard output must equal bash's (commands,
  functions, built-ins, reserved words, after operators, a slash in a
  command word, files, directories in steps, names needing quotes, a
  newline in a name, inside quotes, mid-word, tilde, absolute,
  redirections, variables in the three forms, Ctrl-V Tab); written by
  hand, said so in their meta, where pelt chose otherwise (vi insert
  mode, after `FOO=1 ` and `if `, a variable inside a word, hidden
  files, `~` alone) and for every screen (the list, its columns at 40
  cells, wide names, the redraw under a two-line prompt, the question
  before a tall list). The harness gains a meta key `tr_by=hand` so
  `session-record` never overwrites a transcript written by hand.
- **Table checks** in `sh.selftest` for the lexer's decision (kind, the
  text completed, the quote open), the quoting, the common prefix and
  the column layout.
- **Census**: new `ed/21`… rows (kind X, not counted) for the
  completion; `ed/6` gains its cases. Statements stay **451 of 545**.

### 3.3 The numbers

| | trunk | predicted at the head |
|---|---|---|
| sessions | 215/0/16 | **(217 + new)/0/14**: the two completion cases leave pending; every new case passes; falsified if any case fails or pending is not 14 |
| corpus | 880/0/80 | **880/0/80** (nothing a script sees moves) |
| statements | 451 of 545 | **451 of 545** |
| `edit-witness` | 10 rows | 10 rows green; `idle` 0 context switches in 10 s |
| real scripts | as trunk (aided 76/3/1) | **verdict for verdict as trunk** (the two known timing coins aside) |
| Tab at an empty command word, kasumi `/usr/bin` | — | answered (bell) in under 50 ms on release; the list question in under 50 ms on the next Tab |

### 3.4 The machines

native and release, as every lane. lupin and the checked machine:
predicted unchanged (lupin refuses at resolve naming
`os_signal_default`; the checked machine `unsupported`, home-module
method calls).

### 3.5 Plant

On branch `sh16-plant` (never to merge): the head with Tab inserting
itself again (`is_char_key` before the completion). Predicted red in CI:
every new completion case and the two former pending cases, on both
tiers of linux and macOS; nothing else.

### 3.6 A static pelt for PAX

`pax/tools/mkpelt` at pax trunk, inside an Ubuntu 24.04 container on
kasumi, against this branch's head: an `ET_EXEC` with no `PT_INTERP`;
its sha256 in the report for PAX's next pin.

### 3.7 The result against the prediction

Measured on kasumi (linux x86-64, CachyOS, 16 cpus; the oracles of
record) and in CI (linux x86-64, macOS arm64, linux aarch64). **trunk**
is `7dd3304` built in its own worktree (`logs/base.status`), **head**
`d8d420c` in its own (`logs/head.status`), both by
`notes/sh16-evidence`'s gauntlet: every gate's exit status 0 on both.

| prediction | predicted | measured | held? |
|---|---|---|---|
| the two pending cases leave pending | pass against bash | `c_ed_complete_command`, `c_ed_complete_file` pass on both tiers, kasumi and CI | held |
| sessions | (217 + new)/0/14 | **241/0/14** (24 new) on both tiers and both under `taskset -c 0-3` (kasumi), both tiers on linux and macOS CI | held |
| every new case red at trunk | — | trunk's release binary: 25 of the 26 completion cases fail (`logs/red-new-cases-trunk.log`); the 26th, `c_ed_complete_tilde_alone`, passed at trunk as first written (`ls ~` and `ls ~<tab>` both list `docs`), was rewritten (`d8d420c`) and is red at trunk now (`logs/red-tilde-alone-trunk.log`) | held after a fix to one case |
| corpus | 880/0/80 | **880/0/80 (3)** both tiers and `taskset` (kasumi); 880/0/80 on both CI hosts | held |
| statements | 451 of 545 | **451 of 545 (83.5%)**; kind X 30 → 35 (`ed/21`–`ed/25`) | held |
| `edit-witness` | 10 rows green, idle 0 | **11 of 11** (the new `tab-latency` row) on both tiers and both under `taskset`; idle **0 context switches in 10 s**; `kill -INT` median 1.1 ms; trunk fails only `tab-latency` (no bell: the tab is inserted, `logs/red-edit-witness-trunk.log`) | held |
| Tab at an empty command name | under 50 ms (release, kasumi `/usr/bin`) | 3,790 names: the bell median **11.7 ms** release, 9.6 ms native (kasumi); 15.0–16.1 ms ubuntu CI, 6.1–6.3 ms macOS CI; the question on the next Tab the same | held |
| memory at the prompt | — (not predicted) | `tools/session-rss -n 20000`: trunk 3,276 → 4,876 KB, head 3,268 → 4,872 KB (`logs/rss-*.log`): the names a line copies die with its region | — |
| real scripts | verdict for verdict as trunk | §3.8 | |
| lupin, checked machine | unchanged | checked: `unsupported`, home-module method calls, `phase_reached mem`; lupin: `unsupported` at resolve naming `os_signal_default` (`logs/machines.txt`) | held |
| the plant | every new case and the two former pending red, both tiers, linux and macOS; nothing else | CI 38797987258 on `sh16-plant` (`dc05d19`: `a8cc525` with Tab inserting itself): sessions **216/25/14** on linux and macOS (native; the release step does not run after a red), the 25 being every completion case of that head but the old `c_ed_complete_tilde_alone` (see above); `edit-witness` `tab-latency` red on both tiers of both hosts; nothing else red (`ci/plant-38797987258.txt`) | held, with `tab-latency` red too |
| a static pelt for PAX | ET_EXEC, no PT_INTERP | pax `b7fb8d1`'s `tools/mkpelt` in Ubuntu 24.04 (gcc 13.3, clang 18.1.3, glibc 2.39) at pelt `d8d420c7055f…`: **sha256 `6774441ba446250e05065fd4dfa384d80bde593c2f4f612db073488b10c0a997`, 14,765,328 bytes**, ET_EXEC, no PT_INTERP, hashed twice; `-c` runs, Tab rings and asks (`logs/mkpelt.log`, `logs/mkpelt-sums.txt`) | held |

**Not predicted.**

- **A question answered left the row of Tabs open**: the first build
  asked again on the very next Tab after `n` (the answer was read inside
  the list, so the loop never saw a key end the row). The new
  `tab-latency` row found it; the answer now ends the row (`ec0c1d6`),
  so asking again takes two Tabs, as everywhere else.
- **bash completes nothing inside a backquote** though it does after
  `$(`: that step moved from the bash-recorded case to the hand-written
  one.
- **kasumi has `uname26`** beside `uname`, so `unam` is ambiguous there;
  the cases use their own `PATH` directory and functions, never a
  host's programs (except `/usr/bin` for the absolute path).
- **The first baseline was contaminated**: the trunk gauntlet ran in the
  tree the lane was editing, and a build mid-run replaced its binaries
  and its static build (`logs/base-contaminated.status`, kept). It was
  re-taken in a worktree of its own, as was the head's.

### 3.8 The script census

(filled when the census finishes)

## 4. Evidence index

- **The prediction:** `7edbe18`, before the first change under `tools/`
  (`c6c0356`) and `src/` (`f706e3a`).
- **The references:** `notes/sh16-evidence/probe/probe.py` (the driver),
  `logs/probe-refs.txt`, `probe-refs2.txt`, `probe-mksh.txt` (bash 5.2,
  mksh 59c, dash 0.5.12 in the Debian container), `probe-refs3.txt` and
  `probe-bash53-lcp.txt` (the LCP-then-type row, container and kasumi).
- **The cases:** `notes/sh16-evidence/cases/mkcases.py` writes every
  new case's keys, meta and files; the bash ones were recorded by
  `tools/session-record` (`logs/record3.log`; dash, the second opinion,
  completes nothing); the `tr_by=hand` ones drafted by
  `cases/hand-draft.py` from pelt and checked line by line against §3.1.
- **The gauntlets:** `logs/base.status` (trunk), `logs/head.status`
  (`d8d420c`) and every step's log beside them.
- **Seen red:** `logs/red-new-cases-trunk.log`,
  `logs/red-tilde-alone-trunk.log`, `logs/red-edit-witness-trunk.log`
  (trunk's binary); `logs/selftest-plant.log` (a wrong table row fails
  `wolf test`); CI run **38797987258** on `sh16-plant`
  (`ci/plant-38797987258.txt`).
- **CI green:** run 38797978346 at `a8cc525` (`ci/head-38797978346.txt`)
  and the run at the PR's head (the PR body).
- **The machines:** `logs/machines.txt`. **Memory:** `logs/rss-*.log`.
- **PAX:** `logs/mkpelt.log`, `logs/mkpelt-sums.txt`.

## 5. Done-when

- Branch `sh16`, PR #30 open and unmerged, CI green at the head;
  `wolf/tools/lane-audit.sh pelt sh16 30` run from the org directory,
  its exit status read directly.
- pelt issues: **none closes** (none of the open ones is about
  completion; ruling #69 R3 had no issue). None filed.

## 6. What Tab does, and whose behaviour it follows

| case | pelt | follows |
|---|---|---|
| unique command, file, variable | completed; a space when nothing follows the cursor | bash, mksh (the space only at the end: bash) |
| directory | `/`, no space | both |
| several | the common prefix and the bell; the next Tab lists | the prefix and bell: bash; the list on the second Tab: the contract (bash needs a third after progress, mksh lists at once) |
| list | columns down then across, width the widest + 2 cells, (width − 1) / that columns, then the whole prompt and the line again; `/` after directories, `$` before variables | bash's layout and counts; mksh's unpadded last column |
| taller than the window | asked first (`list all N? (y or n)`, pelt's own words); `y`, `Y` or space lists; the answer ends the row | pelt: sized to `os_term_size`'s rows (bash asks above 100 items; mksh never) |
| no match | the bell | both |
| commands | built-ins, reserved words, functions, files with an execute bit on `PATH`; no aliases (pelt has none) | both offer reserved words and functions |
| command position | line start, after `; & | ( )`, `$(`, backquote, an assignment, `if then else elif while until do ! {` | operators and `$(`: both; assignment, reserved words, backquote: pelt (XCU 2.9.1), neither reference |
| a slash in the command word | directories and executables only | bash (mksh offers every file) |
| `~`, `~/x` | from `HOME`, the tilde kept; a lone `~` → `~/`; `~user` nothing | bash keeps the tilde; the lone `~`: pelt (bash offers users, mksh expands) |
| hidden files | only when the typed part starts with `.` | mksh and pathname expansion (bash offers them) |
| quoting | backslashes outside quotes (blanks, `|&;<>()$\`\"'*?[`, a leading `~` or `#`); a newline as `'<NL>'`; inside `"…"` and `'…'` their own rules, the quote closed on a unique match | bash's backslashes and closing; the newline: mksh's shape |
| `$name`, `${name`, `"$name` | completed; `}` and the quote closed | bash; anywhere in a word (bash only at its start; mksh never) |
| mid-word | the text before the cursor; text after kept | bash (mksh rings) |
| vi insert mode | completes | mksh, the contract (bash `--posix` inserts a tab) |
| vi command `\` `*` `=` | sh11's pathname expansion, unchanged | POSIX (dash has no editor to measure) |
| Ctrl-V Tab, `lnext` Tab | a tab | both |

## 7. Wolf findings

None. Every builtin used (`fs_read_dir`, `fs_stat`, `fs_is_dir`,
`os_term_size` through sh15's width) answered as the spec at `v0.2.30`
says; nothing filed.

## 8. Not verified, and named out

- **A typed unquoted `*`, `?` or `[` stays as typed**: completion only
  appends, so `st*` + Tab gives `st*ar` (it reads back as a pattern that
  matches the file) where bash rewrites it `st\*ar`. `st\*` gives
  `st\*ar`.
- **Executability in a listing** is any execute bit (`mode & 0111`); the
  command search itself asks `may` with the shell's ids. A file only
  root may run is offered to a user.
- **`~login`** is not completed (pelt has no user lookup at the prompt).
- **Programmable completion, aliases, `$(…)` inside double quotes,
  `case` patterns, `for … in`**: none is special; the last two complete
  files as any argument.
- **A list with control characters in names** is drawn with `^X`
  (sh11's `show_cp`); measured by the newline case's line, not by a
  list screen.
- **Bytes that are not UTF-8 in a name**: `text` turns them into `?`
  before they are inserted, so such a name does not complete to itself
  (W06, wolf strings are UTF-8).
- **No person drove a real terminal emulator**; the screens are the
  harness's ECMA-48 terminal. The bell is counted in the probes' raw
  bytes, not judged by `tools/session`.
- **bash in the container is 5.2, the oracle of record 5.3**; every
  recorded transcript is 5.3's, and the probe rows that decided a
  choice were the same on both where both were run (the LCP row).
- **macOS** by CI only. linux aarch64 still builds no tier at 0.2.30
  (asserted in CI).
