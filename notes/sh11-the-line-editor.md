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
