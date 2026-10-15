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
