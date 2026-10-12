# sh11 — the line editor

Contract: `sprints/pelt/11-the-line-editor/sh11-the-line-editor.md` in
the planning repo (ruling #69 R2: emacs keys by default, POSIX
`set -o vi`). This file is the lane's record: §2 and §3 are committed
before the first change to pelt's code, and §4 is filled in as the work
lands.

## 1. Forbidden, absolutely

As the contract's §1. **Clean-room (ruling #43):** no shell's or
line-editing library's source is read or searched for (readline,
libedit, linenoise, zle, bash, dash, ksh, mksh, busybox, yash, fish,
oksh, or any other). The facts come from POSIX.1-2024 XCU `sh`
(Command Line Editing, vi-mode; ASYNCHRONOUS EVENTS), ECMA-48 and the
terminal's documented control sequences, `termios(3)`, Unicode's
character database as data (East Asian Width, general categories, read
through Python's `unicodedata`, Unicode 16.0.0), and black-box sessions
with `dash` (no editor) and `bash --posix -i` as a user sees them. No
`extern "c"`. No `rm` outside `~/lanes/sh11/`; no `git add -A`; nothing
under `~/.claude`; no merge, no tag, no issue filed or closed; no
attribution trailers; kasumi jobs killed by recorded pid only; no build
on nomad-1; at most one CI run at a time; scratch under `~/lanes/sh11/`.

## 2. Inputs, verified (2026-10-11, re-derived from origin)

| input | contract says | measured | drift |
|---|---|---|---|
| pelt trunk | `84a02dc` (or later if sh07 merges) | sh07 merged while this lane read its inputs: origin/trunk is `251f90a`; branch `sh11` was cut there (no commit of this lane predates it) | trunk moved, as the contract allowed |
| toolchain | wolf 0.2.27 | `wolf-toolchain.toml` at `251f90a`: wolf 0.2.27 `0ddda6b`, lupin 0.1.50 `32b970d`, std `87ba162`; `tools/fetch-toolchain` on kasumi verified the linux x86-64 digests and staged them | none |
| sessions at trunk | — | `tools/session --bin target/release` on kasumi at `251f90a`: **pass 92, fail 0, pending 35 (1 PEND-ok, `c_jc_shell_is_leader`)**, the same at `84a02dc` | none |
| `docs/PLAN.md` | the editor is H3a | H3a: raw mode, emacs keys, history recall, UTF-8 and wide characters, long lines; "wolf 0.2.27 is enough to start"; resize and restoring on a kill need W05; "a terminal on a slow line … the line editor must keep that true, and redraw little". H3d puts vi mode after ruling R2 (made: #69) | none |
| `witness/term_keys` | raw mode, VMIN/VTIME and mode restore work; size only by a cursor-position report | the witness (`notes/sh06-evidence/witness/term_keys/term_keys.lu`) and its log: `24;80` by `ESC[6n` after `ESC[999;999H`, three key bytes `97 27 91`, a `VMIN 0 VTIME 2` read empty after 0.2 s, mode restored `true`. `[os.term.mode]` at the tag: the mode is one int, bits CANONICAL 1, ECHO 2, SIGNALS 4, VMIN bits 8..15, VTIME 16..23; **every other termios field is left as found** (so IXON, IEXTEN, ICRNL, OPOST stay as the user set them) and the special characters (erase, kill, interrupt, eof) cannot be read | the contract does not name the unreadable special characters; added to W05's text (§3.6) |
| `witness/winch` | no SIGWINCH meaning | `[os.signal.set]` at the tag has nine meanings, none SIGWINCH; the witness heard 0 while resized; a listen for bit 512 answers `ok` (not refused) | the over-wide listen being accepted is noted for the issue text |
| `witness/read_vs_signal` | a read not woken by a signal | `[os.term.note]`: "a delivered signal never tears a read"; the witness stayed in its read 2 s after SIGINT | none |
| `tools/session` and how a case is judged | — | `tools/lib_session.py`: the shell's stdin is a pty slave (also its controlling terminal), stdout and stderr are pipes; pelt is paced by the oracle's prompt at the end of standard error; a case compares per step the stdout bytes, whether stderr had anything but the prompt, the prompt, and the exit; `compare=stdout` compares stdout and the exit only. **The pty master's output (what a terminal would show of echo) is read and thrown away; no screen is judged anywhere today, and nobody answers a cursor-position report** | the screen judge is new work (§3.5) |
| the pending editor cases | — | 13 under "line editor" (`c_ed_*`, `c_long_line`), 3 under "vi mode" (`c_vi_*`), 4 under "history"; all recorded from `bash --posix -i`, `compare=stdout` | none |
| POSIX vi-mode text | XCU `sh` | sh06's copy, `~/lanes/sh06/posix/sh.txt` (POSIX.1-2024 XCU `sh`), lines 323–790: insert-mode keys, the command-mode list, motions, counts, `u`/`U`, history `k j - + G / ? n N`, `= \ *`, `@letter`, `v` | none |
| black-box Ctrl-C at the prompt | — | probe on kasumi (`~/lanes/sh11/probe/probe.py`, through `lib_session`): **dash** keeps no prompt after `^C` (the tty echoes it) and runs an INT trap only when the next line is read; `$?` is 130 after. **bash** draws `^C`, a new line and a new prompt, runs an INT trap at once, `$?` 130; with `trap '' INT` bash ignores the key and keeps the line, dash's tty discards the line | decides §3.2's Ctrl-C row |
| sh07 | runs beside, parser/expansions/`test` | merged at `251f90a` (this lane starts after it) | none |
| kasumi | /home at 97% | 35 GB free; no `tmux`, `ksh` or `mksh` (no package may be installed), so bash is the only second opinion and the screen judge is pelt's own emulator | stated |

## 3. Prediction (committed before the first change)

### 3.1 The design

- **Where it runs.** Only when the shell is interactive, shell
  descriptor 0 is the process's descriptor 0, that is a terminal, the
  terminal's mode can be read, `TERM` is not `dumb`, and an editing
  option (`emacs` or `vi`) is on. Otherwise pelt reads bytes exactly
  as today and the terminal's own line discipline edits (a pipe, a
  file, `pelt -i <file`, `exec 0<file`).
- **The mode.** Read once per line; the editor sets CANONICAL, ECHO
  and SIGNALS off with `VMIN 0, VTIME 1`, and sets the mode it read
  back before it returns, on every way out of a line (accepted,
  end of input, Ctrl-C, a hangup). It is never left on while a command
  runs, so `exec`, `exit`, `read`, children and traps all see the
  user's mode. SIGNALS is off so Ctrl-C and Ctrl-Z arrive as bytes the
  editor handles; a `kill -INT` from elsewhere is still polled.
- **Drawing.** The prompt goes to standard error as today (POSIX); the
  edited line is drawn on the terminal itself (descriptor 0, which a
  terminal opens read-write; standard error if a write to 0 is
  refused). So a session's standard error carries exactly what it did
  without an editor, and `2>file` still lets a user see their line.
- **The buffer** is a list of code points; the cursor is an index that
  only rests on a cluster boundary: a code point of width 1 or 2 and
  every zero-width code point after it (combining marks, ZWJ,
  variation selectors) move, erase and redraw as one. Bytes that are
  not UTF-8 are kept as themselves and shown as `?`.
- **Width** of a code point from a table generated from Unicode 16.0.0
  data by a committed tool (`tools/gen-width`, Python's
  `unicodedata`): 0 for Mn, Me and Cf (but U+00AD) and the Hangul
  medial/final jamo; 2 for East Asian Width W and F (and the unassigned
  planes 2 and 3); 1 otherwise; a control character is shown as `^X`
  (2 cells). Emitted as a balanced comparison tree: no table in memory.
- **Layout and redraw.** The editor knows the column the prompt started
  in and the prompt's width (escape sequences in `PS1` take no cells),
  lays the line out cluster by cluster, a wide character that would
  straddle the right margin going to the next row behind a space it
  writes itself, and never moves the cursor while the terminal is in
  its pending-wrap state (a row that ends exactly at the margin is
  followed by CR LF). An edit at cluster `k` redraws from `k` to the
  end, clears below (`ESC[J`) only if the line got shorter, and moves
  the cursor back with relative moves (`\b`, `ESC[nD/C/A/B`, CR).
  Typing at the end of the line writes the character alone; Left is
  one `\b`. Ctrl-L clears the screen and redraws prompt and line.
- **Width learned** in this order: `COLUMNS` if set and a positive
  number (XBD 8.3, the user's preferred width: no query); else a
  cursor-position report — `ESC[6n ESC 7 ESC[999C ESC[6n ESC 8`, one
  round trip giving the prompt's start column and the width — written
  before the prompt, read with a 0.3 s limit; a terminal that never
  answers is not asked again and the width is 80. A terminal that
  answered is asked again before each prompt, which is how a resize is
  seen without SIGWINCH (at the next prompt, or at Ctrl-L).
- **Signals while editing.** No read is torn by a signal
  (`[os.term.note]`), so the editor reads with `VTIME 1` and polls
  between reads: a `kill -INT` ends the line as Ctrl-C does (XCU `sh`
  ASYNCHRONOUS EVENTS); a SIGHUP (listened for only while editing, and
  only when no trap names it and it is not ignored) restores the mode,
  sets HUP back to the default and raises it, so pelt dies of HUP as
  dash does, with the terminal as it found it. SIGTERM and SIGQUIT are
  ignored by an interactive shell (unchanged). A read that comes back
  empty much sooner than 0.1 s, three times running, is a hangup: end
  of input.
- **History, only the seam sh12 needs.** Each non-empty line accepted
  is kept in memory (a ring of `HISTSIZE` lines, 128 when unset), Up
  and Down (Ctrl-P, Ctrl-N) and vi's `k j - + G / ? n N` walk it; no
  file, no `fc`, no Ctrl-R. Editing a recalled line makes it the edit
  line (POSIX's rule, used for both modes).
- **Memory.** Each line is edited inside `copy region` (the line, and
  the few things that outlive it — the kill buffer only when it
  changed — are its value); a read is its own region, so an idle
  prompt allocates nothing.

### 3.2 The emacs key table (the default; `set -o emacs`)

| key | bytes accepted | action |
|---|---|---|
| Left, Ctrl-B | `ESC[D`, `ESCOD`, 0x02 | back one character |
| Right, Ctrl-F | `ESC[C`, `ESCOC`, 0x06 | forward one character |
| Home, Ctrl-A | `ESC[H`, `ESCOH`, `ESC[1~`, `ESC[7~`, 0x01 | start of line |
| End, Ctrl-E | `ESC[F`, `ESCOF`, `ESC[4~`, `ESC[8~`, 0x05 | end of line |
| Alt-B, Alt-F (Ctrl-Left/Right) | `ESC b`, `ESC f`, `ESC[1;5D`, `ESC[1;5C` | back / forward a word (letters, digits, any non-ASCII) |
| Alt-D, Alt-Backspace | `ESC d`, `ESC 0x7f` | kill the word after / before the cursor |
| Ctrl-W | 0x17 | kill back to the previous blank-separated word |
| Ctrl-U | 0x15 | kill from the start of the line to the cursor |
| Ctrl-K | 0x0b | kill from the cursor to the end |
| Ctrl-Y | 0x19 | put the last kill at the cursor |
| Backspace | 0x7f, 0x08 | erase the character before the cursor |
| Delete | `ESC[3~` | erase the character under the cursor |
| Ctrl-D | 0x04 | on an empty line, end of input; else as Delete |
| Ctrl-L | 0x0c | clear the screen, redraw |
| Ctrl-C | 0x03 | `^C`, a new line, the line abandoned, `$?` 130, an INT trap runs now, a new prompt (bash as a user sees it; POSIX's vi rule); with `trap '' INT` the key is ignored and the line kept (bash) |
| Up, Ctrl-P / Down, Ctrl-N | `ESC[A`, `ESCOA`, 0x10 / `ESC[B`, `ESCOB`, 0x0e | previous / next line in memory |
| Ctrl-V | 0x16 | insert the next byte as itself |
| Enter | CR, LF | accept |
| Tab | 0x09 | inserted, shown `^I` (completion is not this lane's; R3) |
| Ctrl-Z, Ctrl-\, other controls, unknown sequences | | ignored (a whole CSI or SS3 sequence is consumed) |

### 3.3 The vi subset (`set -o vi`, XCU `sh`)

Insert mode: newline/CR, erase, interrupt, kill, Ctrl-V, Ctrl-W, EOF at
the start of a line, ESC; arrows also work (bash; POSIX silent).
Command mode, all with counts where POSIX gives one: Ctrl-L, `#`, `=`,
`\`, `*`, `@letter`, `~`, `.`, `l` space `h` `w W e E b B ^ $ 0 |`,
`f F t T ; ,`, `a A i I R`, `c` + motion, `cc`, `C S`, `r`, `_`, `x X`,
`d` + motion, `dd`, `D`, `y` + motion, `yy`, `Y`, `p P`, `u U`,
`k - j + G`, `/pattern` `?pattern` `n N`, newline/CR, interrupt.
**Predicted not done: `v`** (it needs `fc` and history numbers: sh12);
it alerts. `@letter` has no effect because pelt has no aliases yet,
which is what POSIX says when no alias `_letter` exists. `=`, `\` and
`*` use pelt's own pathname expansion.

### 3.4 Options

`set -o emacs` and `set -o vi` turn each other off; `set +o` either
leaves no editor. An interactive shell starts in emacs mode, a
non-interactive one with both off (dash prints both as options; checked
against dash in a new differential case). `set -o`/`set +o` list both.

### 3.5 Session cases and the screen judge

- **Moves from pending to pass (13):** `c_ed_left_insert`,
  `c_ed_utf8_left`, `c_ed_utf8_erase`, `c_ed_home_end`,
  `c_ed_kill_to_end`, `c_ed_delete_char`, `c_ed_word_motion`,
  `c_ed_up_arrow`, `c_ed_up_down_edit`, `c_long_line`, `c_vi_basic`,
  `c_vi_history`, `c_vi_motion`. **Stays pending (8):**
  `c_ed_complete_command`, `c_ed_complete_file` (completion, R3),
  `c_ed_search` (Ctrl-R, sh12), `c_hist_fc_edit`, `c_hist_fc_list`,
  `c_hist_fc_s`, `c_ps1_bang` (sh12), and the rest unchanged.
- **The 92 dash cases keep passing with the editor on**, except
  `ctrl_c_prompt` and `ctrl_c_trap_prompt`, whose dash transcripts are
  the line discipline's Ctrl-C; they are run with `+o emacs` (no
  editor, still against dash) and the editor's Ctrl-C gets its own
  cases against bash. Final count predicted: **pass 105 + the new
  cases, fail 0, pending 22**.
- **A screen judge** (new): `tools/lib_session.py` gains a small
  ECMA-48 terminal (the controls and sequences above, auto-wrap with a
  pending-wrap state, wide characters by `unicodedata`) fed with what
  a real terminal would show of the editor — the pty's output and
  standard error, in order — which also answers the cursor-position
  report; a case with a `<name>.screen` file is judged on the rows its
  steps drew and the cursor, recorded from bash through the same
  terminal at the same size (`TIOCSWINSZ`), or written by hand where
  bash and POSIX part (said so in the meta). And after every pelt
  session the pty's mode must be what it was before pelt started
  (`tcgetattr` on the master): **a session that leaves the terminal
  raw fails**.
- **Planted reds (CI):** a wide character counted as one cell (the
  wrap cases' screens go red), and the mode not restored after Ctrl-C
  (the mode check goes red).

### 3.6 What degrades without W05, and the numbers

- **No window size:** width by `COLUMNS`, or one cursor-position round
  trip per prompt, or 80. **No SIGWINCH:** a resize while a line is
  being edited is seen at the next prompt or at Ctrl-L; until then a
  wrapped line redraws at the old width. **No interruptible read:** 10
  timed reads a second while idle at the prompt; a signal acts within
  0.1 s. **No special characters** (erase, kill, intr, eof, werase,
  lnext): the defaults `^?`/`^H`, `^U`, `^C`, `^D`, `^W`, `^V` are
  assumed, so `stty intr ^X` is not honoured by the editor. **Only
  three mode bits:** IXON (Ctrl-S/Ctrl-Q) and, on linux, IEXTEN's
  Ctrl-V/Ctrl-O stay with the line discipline if the user has them on
  (checked black-box). **No restore on an uncatchable death** (SIGKILL,
  a wolf trap): the runtime restores nothing (`[os.term.mode]`).
- **Latency** (kasumi, release, quiet, 2,000 keys, key written to the
  master until its echo is read back): median **under 0.5 ms**, p99
  under 3 ms; one byte written per ASCII key typed at the end of the
  line.
- **Memory:** `tools/session-rss -n 20000` at trunk `251f90a` grows
  3,036 → 9,064 KB (301 B a command, measured above). With the editor:
  **at most 64 B a command more** (≤ 10,350 KB at 20,000), and an idle
  prompt does not grow.
- **Slow line:** every editor case gives the same transcript and screen
  with `PELT_SESSION_SLOW=0.02` (a byte every 20 ms).
- **Idle cost:** ≤ 3 s of CPU per idle hour at the prompt.
- **Wrong predictions will be reported as such in §5.**

## 4. Evidence index

Hosts: kasumi (linux x86-64, CachyOS, 16 cpus) for every build and
session; nomad-1 for editing and two Python-only probes. Toolchain:
wolf 0.2.27 `0ddda6b`, lupin 0.1.50 `32b970d`, std `87ba162` (the pin,
unchanged). Logs are under `notes/sh11-evidence/`.

### 4.1 What was built

- `src/sh/edit.lu` — the editor: emacs keys, POSIX vi mode, clusters
  and cells, the layout, relative redraw, the width query, the
  in-memory history, the signal polls (`d552b8b`, `c151e79`; what
  crosses a line's region as strings, `3396120`).
- `src/sh/width.lu` — generated by `tools/gen-width` from Unicode
  16.0.0 (`7072afb`); 976 ranges as a comparison tree; CI checks it is
  what the tool makes wherever the runner's Python is Unicode 16.0.0.
- `src/sh/interact.lu` — `next_line`: the editor when `ed_active`, the
  byte reader otherwise; Ctrl-C ends the line with `$?` 130 and runs an
  INT trap at once (`03a95b5`, `50cdaad`).
- `set -o emacs` / `set -o vi` (`ab8100b`); an interactive shell starts
  in emacs mode; `set -o` / `set +o` list both; `option/c_edit_modes`
  (`2e1c2b2`) against bash (dash 0.5.13 leaves vi on under
  `set -o emacs`, which XCU forbids).
- The session harness (`6e6ea40`): `Screen`, a small ECMA-48 terminal
  fed with the pty's output and standard error (pty first); it answers
  a cursor-position report as a terminal does; a case with `screen=N-M`
  is judged on what each of those steps drew and on the cursor,
  recorded from bash at the same size (`cols=`, `rows=`, `TIOCSWINSZ`);
  **every pelt session fails if the terminal's ICANON, ECHO or ISIG
  differ at exit from before pelt started**. A case judged on standard
  output alone is paced by quiet, as it was recorded; `env=PS1=$\s`
  gives a bash-recorded case pelt's first prompt.
- `tools/edit-witness` (`b81609e`), in CI on both tiers;
  `tools/edit-bench` (`37a9f69`).

### 4.2 Key table and vi subset, as built

The emacs table is §3.2's, with these differences: Alt-D and
Alt-Backspace kill a word (added); Ctrl-Left/Right (`ESC[1;5D/C`) move
by words; **a recalled line keeps its changes in place while another
is shown and is not made the edit line in emacs mode** (bash, as a user
sees it; the prediction said "both modes"; vi mode keeps POSIX's rule).
The vi subset is §3.3's, every command listed there, except `v`
(alerts; `c_vi_v` pending on sh12) and `@letter` (pelt has no aliases,
so no `_letter` is enabled: POSIX's "no effect"). `U` returns to the
line as command mode first found it (bash; POSIX's text reads as "all
changes", which would include the typing; said in the clause table,
`sh/34`). Arrows, Home, End and Delete also work in vi insert mode
(bash; POSIX silent).

### 4.3 Session results

| head | where | pass | fail | pending (PEND-ok) | log |
|---|---|---|---|---|---|
| `251f90a` trunk | kasumi, release | 92 | 0 | 35 (1) | `~/lanes/sh11/session-base-251f90a.log` (kasumi) |
| `50cdaad` | kasumi, native and release | 161 | 0 | 36 (14) | `notes/sh11-evidence/logs/50cdaad/` |
| `50cdaad` | kasumi, release, a byte every 20 ms (editor cases) | 70 | 0 | 17 (13) | idem, `session-slow.log` |
| `5474c9d` | CI run 38207820361, linux x86-64, both tiers | 171 | 0 | 26 (4) | the run |
| `5474c9d` | CI run 38207820361, macOS arm64, both tiers | 171 | 0 | 26 (1) | the run |

At `50cdaad` thirteen cleared cases still carried `pending=` (a
re-record kept the marks; `389ace3` removes them), hence 14 PEND-ok.

The two dash Ctrl-C-at-the-prompt cases (`ctrl_c_prompt`,
`ctrl_c_trap_prompt`) record the terminal's own line discipline; they
run pelt with `+o emacs` (no editor, still against dash), and the
editor's Ctrl-C has its own cases against bash (`c_ed_ctrl_c`,
`c_ed_ctrl_c_trap`, `c_ed_ctrl_c_ignored`, `c_ed_ctrl_c_continued`,
`c_vi_ctrl_c`). Black-box: dash shows `^C` and waits; bash draws `^C`,
a new line and a prompt and runs an INT trap at once. POSIX
(ASYNCHRONOUS EVENTS and vi-mode) says the line is abandoned and the
prompt reissued on the next line: bash's behaviour, and pelt's.

Differential corpus: 826 / 0 / 103 on both tiers, kasumi at `50cdaad`
and CI at `5474c9d` (trunk 825; the new case is `option/c_edit_modes`).

### 4.4 The mode-restore proofs

| path | proof |
|---|---|
| a command runs | `c_ed_mode_command`: `stty -a` at the prompt sees ICANON, ECHO, ISIG on (`0`, as bash) |
| `exec` | `c_ed_mode_exec`: `exec sh -c 'stty -a …'` sees the user's modes |
| after Ctrl-C | `c_ed_mode_after_ctrl_c`, and the harness's exit check on every Ctrl-C case |
| `exit`, end of input | the harness's exit check on every session: 171 of 171 passing cases on both hosts |
| SIGHUP (pelt can catch it) | `tools/edit-witness` `hup`: pelt dies of SIGHUP (as dash) and the modes are back |
| SIGINT from `kill` | `edit-witness` `int`: a new prompt, `$?` 130, modes restored |
| SIGTERM | `edit-witness` `term`: ignored (interactive), editing goes on, restored at exit |
| the terminal hangs up | `edit-witness` `hangup`: end of input, the shell exits |
| SIGKILL | `edit-witness` `kill`: **not restored**, reported and not a failure: no handler runs and the runtime restores nothing (`[os.term.mode]`) |

The witness runs in CI on both tiers of linux and macOS (run
38207820361); kasumi's output at `50cdaad`:
`notes/sh11-evidence/logs/50cdaad/witness-release.log`.

### 4.5 Latency, cost, memory

`tools/edit-bench`, kasumi, quiet (`notes/sh11-evidence/logs/bench-*.log`):

| | release | native |
|---|---|---|
| key at the end of the line, 2,000 keys: median / p99 | 0.015 / 0.073 ms | 0.133 / 0.203 ms |
| bytes written per key at the end | 1 | 1 |
| key at the start of a 2,000-character line: median / p99 | 0.044 / 0.149 ms | 0.280 / 0.345 ms |
| Enter to the next prompt (`:`), with / without the editor | 0.060 / 0.101 ms | 0.193 / 0.187 ms |
| CPU while idle at the prompt | 0.00 s in 30 s | 0.02 s in 120 s (0.6 s an hour) |

`tools/session-rss -n 20000` (`notes/sh11-evidence/logs/rss-head.log`,
`rss-trunk-251f90a.log`), KB at 0 → 20,000 commands:

| binary | KB | per command over trunk |
|---|---|---|
| trunk `251f90a`, release | 3,044 → 9,016 | — |
| head, release, editor on | 3,124 → 10,108 | +55 B |
| head, release, `+o emacs` | 3,120 → 9,136 | +6 B |
| head, native, editor on | 3,840 → 11,024 | (native trunk not taken) |
| head, native, `+o emacs` | 3,604 → 9,828 | |

What the editor still keeps per line: the history ring (the line
itself, replaced in the root region once the ring is full: "the kept
value itself") and the prompt string copied out of its region for
redraws. Two findings on the way, both fixed and measured: an `EdMem`
and a `List` copied out of the line's region every line cost about
150 B a command (now strings, "" when unchanged: `3396120`); and **a
`(bool, str)` tuple copied out of a `copy region` charges the root about
15 B even when the `str` is `""`** (9,436 → 9,150 KB at 20,000 on the
plain path when the tuple became a `bool`, `50cdaad`). The commits
between `8681a5b` and `d552b8b` do not build alone (the option state
names the editor's types); the growth was bisected by building
`8681a5b`, `d552b8b` and `03a95b5`.

### 4.6 W05, re-checked, and the issue text

Re-run at wolf 0.2.27 on kasumi: sh06's four witnesses answer as sh06
recorded (`notes/sh11-evidence/witness/w05-recheck-drive.log`): the size
only by a cursor report (`24;80`), 0 signals heard across two resizes,
a listen for bit 512 accepted, a read not woken by SIGINT (the poll
says 16 only after a key). New: the witness `term_chars`
(`notes/sh11-evidence/witness/term_chars/term_chars.lu`, driver
`drive_chars.py`, log `term_chars.log`): with the interrupt character
moved to Ctrl-X and IXON toggled from the other side, `os_term_mode`
reads back the same int (65536); Ctrl-S and Ctrl-Q never reach the
program. And `lnext_probe.py` (Python on a pty, both hosts,
`lnext_probe.log`): in the mode `[os.term.mode]` can set, linux passes
Ctrl-V and Ctrl-O to the program and macOS keeps both.

**Issue text for the orchestrator to file (wolf-lang):**

> **W05: a terminal's size, its resize, its special characters and
> flags, and a read a signal can interrupt**
>
> pelt's line editor (sh11) runs on wolf 0.2.27's `[os.term.mode]` and
> works around four gaps; each has a witness in pelt
> (`notes/sh06-evidence/witness/`, `notes/sh11-evidence/witness/`).
>
> 1. **Window size.** No call answers the terminal's rows and columns
>    (`TIOCGWINSZ`). The editor asks the terminal itself with a
>    cursor-position report before every prompt (0.3 s on a terminal
>    that never answers, after which it assumes 80), or reads
>    `COLUMNS`. Proposed: `os_term_size(fd) -> (int, int) ! {io,
>    unsupported}`.
> 2. **SIGWINCH.** `[os.signal.set]` has nine meanings and none for a
>    resize; `os_signal_listen(512)` is accepted although bit 512 means
>    nothing (witness `winch`: 0 heard across two resizes). A line being
>    edited when the window changes redraws at the old width until the
>    next prompt or Ctrl-L. Proposed: a `RESIZE` meaning (bit 512), and
>    an over-wide set refused with `io`, as `[os.signal.listen]` says.
> 3. **A read a signal can interrupt.** `[os.term.note]`: "a delivered
>    signal never tears a read" (witness `read_vs_signal`: still in the
>    read 2 s after SIGINT). The editor reads with `VTIME 1` and polls
>    between reads: ten wake-ups a second at an idle prompt (0.6 s of
>    CPU an hour, measured) and up to 0.1 s before a signal acts.
>    Proposed: one wait on a descriptor and a signal set together
>    (`os_read_or_signal(fd, n, set)`, or `net_wait`'s shape over a
>    descriptor and the signal pipe).
> 4. **The special characters and the other flags.** The mode int holds
>    ICANON, ECHO, ISIG, VMIN and VTIME only (witness `term_chars`: the
>    int is unchanged after the interrupt character moves to Ctrl-X).
>    An editor cannot learn the user's erase, kill, interrupt,
>    end-of-file, word-erase and literal-next characters, so `stty erase
>    ^H` or `stty intr ^X` is not honoured while editing; nor turn IXON
>    off, so Ctrl-S and Ctrl-Q stay flow control; nor IEXTEN, so **on
>    macOS Ctrl-V and Ctrl-O never reach the program** even with
>    canonical input off (`lnext_probe.log`; linux passes them).
>    Proposed: `os_term_chars(fd) -> List[int]` (VERASE … VLNEXT in a
>    fixed order) and IXON and IEXTEN bits in the mode.
>
> Related, not a defect: the runtime restores nothing when a program
> dies of a signal it cannot catch (SIGKILL, a trap). An interactive
> shell must otherwise leave SIGHUP at its default, so pelt listens for
> it only while a line is edited, restores the mode, and raises it again.

### 4.7 macOS, found by CI

The first two PR runs were red on macOS only; each cause is fixed and
named:

- **The harness's mode check read a revoked terminal.** On macOS the
  pty's slave is revoked when its session leader exits, so `tcgetattr`
  on it is ENOTTY and every session "left the modes changed" (run
  38199834095, cancelled by this lane once its session step had timed
  out). The modes are read through the master now (`af4e3b2`), which answers for the pair on
  both systems (probe: `~/lanes/sh11/probe/macmode.py` on nomad-1 and
  kasumi).
- **A long line deadlocked the harness.** One blocking write of
  `c_long_line`'s 5,010 bytes against pelt echoing them (macOS's pty
  buffers are smaller): run 38203896210's session step timed out at 15
  minutes. The harness types and reads at once, and reads while it
  waits for the exit (`27061d7`); the edit witness likewise
  (`5b2f4df`; it had hung on macOS, "no answer in 60 s").
- **Ctrl-V never reaches a program on macOS** (IEXTEN, above):
  `c_ed_ctrl_v`, `c_ed_tab_literal` and `c_vi_insert_ctrl_v` are
  pending on "lnext", PEND-ok on linux (`d69165e`).
- **macOS's `wc -c` pads its count** (`c_long_line` now `| tr -d ' '`,
  `5474c9d`).
- The session steps' limit is 15 minutes: the corpus grew from 127
  cases to 197.

### 4.8 At the head

**CI run 38207820361 at `5474c9d`: green on all three jobs** (linux
x86-64 and macOS arm64 build both tiers and run everything; linux
aarch64 asserts both refusals, wolf-lang#614). Sessions 171 / 0 / 26 on
both tiers of both hosts; differential corpus 826 / 0 / 103; the edit
witness passes on both tiers of both hosts. kasumi at `d69165e` (the
code of `5474c9d`): 171 / 0 / 26 (4), the witness, the clause census
427 of 544 met (79.2%; trunk `251f90a` 414 of 532, 77.8%).

### 4.9 The planted reds

Both plants in one commit, `8021e35` on branch `sh11-plant` (left on
origin, never to merge; it is `5474c9d` plus the plant), run by
`workflow_dispatch` as **CI run 38209110786: red on linux x86-64 and
macOS arm64**, each break caught by its own cases:

- **a wide character counted as one cell** (`cells` answers 1 for a
  width-2 code point): `c_ed_wide_insert` and `c_ed_wide_wrap_edit`
  fail on their screens, on both hosts;
- **the mode not restored after Ctrl-C** (`ed_line` skips
  `os_term_set_mode` when the line was interrupted): `c_ed_ctrl_c`,
  `c_ed_ctrl_c_trap`, `c_ed_ctrl_c_continued`, `c_ed_mode_after_ctrl_c`
  and `c_vi_ctrl_c` fail on the harness's exit check ("pelt left the
  terminal's modes changed"), and `tools/edit-witness` fails its `int`
  scenario ("modes restored False") on both tiers of both hosts.

Sessions there: 164 pass, 7 fail, 26 pending on both hosts; nothing
else moved. The same plant on kasumi before it was pushed: the same
seven cases (one more, `c_ed_wide_wrap`, stays green: the terminal
wraps a wide character itself when the editor writes only at the end).

## 5. Prediction against result

| predicted (`480e6b5`) | measured | |
|---|---|---|
| 13 pending cases move to pass | 13 moved (`c_ed_delete_char`, `c_ed_home_end`, `c_ed_kill_to_end`, `c_ed_left_insert`, `c_ed_up_arrow`, `c_ed_up_down_edit`, `c_ed_utf8_erase`, `c_ed_utf8_left`, `c_ed_word_motion`, `c_long_line`, `c_vi_basic`, `c_vi_history`, `c_vi_motion`) | hit |
| `c_ed_complete_*`, `c_ed_search`, the history cases stay pending | they do, named "completion" and "history search" | hit |
| the 92 dash cases pass with the editor on, but the two dash Ctrl-C-at-the-prompt cases (run with `+o emacs`) | exactly those two needed `+o emacs` | hit |
| pass 105 + the new cases, fail 0, pending 22 | 171 / 0 / 26: 66 new cases pass; pending adds `c_vi_v` (written after the prediction) and three Ctrl-V cases macOS cannot pass | hit on linux before the lnext marks (174 / 0 / 23); **miss** on macOS, which was not predicted to differ |
| editing a recalled line makes it the edit line, both modes | vi mode only; emacs keeps it in place as bash does (`c151e79`) | **miss** |
| key latency median < 0.5 ms, p99 < 3 ms | release 0.015 / 0.073 ms; native 0.133 / 0.203 ms | hit |
| one byte per key typed at the end | 1 | hit |
| ≤ 64 B a command over trunk, ≤ 10,350 KB at 20,000 | +55 B, 10,108 KB (release) at the head; the first build was +226 B (13,540 KB) until `3396120` and `50cdaad` | hit at the head; **missed** by the first build |
| idle ≤ 3 s of CPU an hour | 0.6 s an hour (native), 0.0 in 30 s (release) | hit |
| slow line: every editor case unchanged at 20 ms a byte | 70 pass, 0 fail at `50cdaad` | hit |
| SIGHUP restores the mode and pelt dies of HUP | witness `hup`, both hosts | hit |
| `v` not done | not done; alerts; `c_vi_v` pending (sh12) | hit |

Not in the prediction, found: macOS's IEXTEN keeps Ctrl-V and Ctrl-O
(§4.6); a `(bool, str)` tuple copied out of a `copy region` costs the
root about 15 B even for `""` (§4.5); dash 0.5.13 leaves vi on under
`set -o emacs` (`option/c_edit_modes`; bash is the oracle); IXON is out
of a wolf program's reach, so Ctrl-S and Ctrl-Q never reach the editor.

### Not verified

- Any real terminal emulator (xterm, kitty, the linux console, macOS
  Terminal) by a person: every screen here is the harness's `Screen`,
  checked against bash drawing on the same `Screen`.
- A resize while a line is edited (no SIGWINCH; W05): the stated
  behaviour (the old width until the next prompt or Ctrl-L) is read
  from the code, not run.
- The cursor-position query against a terminal that answers slowly
  (over 0.3 s) or never: the harness answers every query; "never" is
  exercised only through `edit-witness` and `edit-bench`, which do not
  answer and set no `COLUMNS` (the bench sets it).
- Key sequences other than those typed by a case (`ESC[7~`, `ESC[8~`,
  `ESCO…` are parsed, never typed).
- vi `=` (it draws the expansions; no case judges that screen),
  `@letter` with an alias (pelt has none), counts above 99,999,
  `HISTSIZE` changed while running.
- No pelt binary ran on a Mac outside CI (no build on nomad-1); the
  revoke and IEXTEN findings were probed on nomad-1 with Python alone.
- linux aarch64: no tier builds (wolf-lang#614).
- ksh as a second opinion: not on kasumi, and no package may be
  installed.
