# sh15 — the terminal (pelt on wolf 0.2.30)

Contract: `sprints/pelt/15-the-terminal/sh15-the-terminal.md` in the
planning repo (`ae2dd72`). This file is the lane's record: §1 to §3 are
committed before the pin and before the first change under `src/`,
`tools/` or `tests/`; the evidence index (§4) is filled in as the work
lands.

## 1. Forbidden

As the contract. No shell's source is read or searched for (dash, bash,
zsh, busybox, mksh, any other), nor a libc's, a kernel's or a
line-editing library's (rulings #42–#45): POSIX.1-2024, man pages as
documentation (`termios(3)`, `stty(1)`, `ioctl_tty(2)`), wolf's spec
at `v0.2.30`, and black-box runs of dash 0.5.13.4 only. **This lane runs
no bash**: the sh11 cases recorded from `bash --posix` keep their
transcripts, and every new case is recorded from dash alone
(`tools/session-record --no-second`, added here) or written by hand
and said so. A signal's meaning is named (`std.signal`'s functions);
no literal signal bit, no host signal number, and no literal mode bit
outside the one table of `[os.term.mode]`'s names. The toolchain from
the release archives by digest, each read twice. No merge, no tag, no
issue filed or closed (listed in the report), no package installed, no
other lane's CI run cancelled, nothing under `~/.claude`, no
attribution trailers. No build on nomad-1: kasumi, under `~/lanes/sh15/`
(one target directory per tree, pruned), detached jobs by `setsid` with
the pid recorded and stopped by that pid only, never by name, pattern
or group. A signal in a test goes only to a process the test started.
Scratch under `~/lanes/sh15/` (`TMPDIR` points there), never `/tmp`.
Strict evidence (#571): `wolf build` exit 2 is a compile error; SigBlk
and SigIgn are read before a signal row is called red; terminal and
signal tests also run under `taskset -c 0-3`. If the harness refuses an
action, the lane stops and reports.

## 2. Inputs, verified (2026-10-15, re-derived before any change)

| input | contract says | measured | drift |
|---|---|---|---|
| pelt trunk | `00e15ca` | `origin/trunk` = `00e15ca4cc24…` (sh14's merge); branch `sh15` cut from it; no open PR | none |
| wolf 0.2.30 | tag `v0.2.30` at `1b37f368` | tag → `1b37f368228db92eca505c8c4cd3c531ea60be48` (read twice); release 413582739; `wolf 0.2.30 (wolfgang, pin 1b37f36)`, "paired with lupin 0.1.53 (reference interpreter), pin 294d626" | none |
| lupin 0.1.53 | tag `v0.1.53` at `7896edd` | tag → `7896eddc17fd9e3e015b025b354ccf62a766734b` (read twice); release 413375414; `lupin 0.1.53 (wolf-interp, reference interpreter at pin 294d626)` | none |
| the digests | by digest, each read twice | the release API read twice, both reads equal; the three wolf and three lupin archives pelt pins downloaded on kasumi and hashed twice, equal to the API (`notes/sh15-evidence/logs/fetch6.log`); the linux x86-64 lupin's `5db55332…` is the CHANGELOG's | none |
| the bundled std | wolf-std `fd6bcdc` | the linux x86-64 archive's `std/STD-REV` is `fd6bcdcb1dfe…`; `9e5bd6b` (pelt's pin) is its ancestor; `std.term.Mode` has `flow` and `extended` (sc61). It has **no wrappers** for `os_term_size`, `os_term_chars`, `os_signal_wait_fd` (CHANGELOG: "Call them directly; they are in the prelude"), so pelt calls the builtins | the std pin moves to `fd6bcdc`, the commit the archive bundles |
| the 0.2.30 CHANGELOG | — | "pelt: the toolchain digests; the line editor adopts the terminal surface (#719, W05) … A hand-built mode there must now name bits 3 and 4 to keep `IXON`/`IEXTEN`." The eleven new prelude names: a grep of pelt `00e15ca4` found no declaration. s233's new E1010 (a proc left running): pelt spawns no `proc` | none |
| the spec at `v0.2.30` | `[os.term.*]`, `[os.signal.wait.fd]` | `[os.term.size]` rows then columns, 0 for a size never told, `RESIZE` (`SIGWINCH`) to the foreground group on a change; `[os.signal.wait.fd]` the meaning (taken off the queue, first when both are ready) or 0 when the descriptor has a byte, the end of input or a hang-up, nothing read, no deadline (`VMIN`/`VTIME` time the read that follows), a refused set `io`; `[os.term.chars]` twelve in a fixed order, -1 disabled; `[os.term.mode]` `FLOW` 8 (`IXON`), `EXTENDED` 16 (`IEXTEN`), every other field left as found | — |
| how pelt's editor uses the terminal at trunk | (sh11, sh14 notes) | `src/sh/edit.lu`: `raw_mode` keeps bits 3..7 of the mode it read and clears CANONICAL, ECHO, SIGNALS with `VMIN 0, VTIME 1`; `ed_query` writes `ESC[6n ESC 7 ESC[999C ESC[6n ESC 8` before every prompt unless `COLUMNS` is set (0.3 s at most; a terminal that never answered is not asked again); `next_byte` reads with `VTIME 1` and polls `HUP` and `INT` between reads; the special keys are the defaults (`^?`/`^H`, `^U`, `^C`, `^D`, `^W`, `^V`) | — |
| the bare pin's behaviour | — | read from the code: `raw_mode`'s `old & 248` carries bits 3 and 4 through, so at 0.2.30 the editor leaves `IXON`/`IEXTEN` as the user set them, as it did at 0.2.29 (the CHANGELOG's hand-built-mode change does not reach pelt) | — |
| the session harness | — | `tools/lib_session.py` sizes the pty (`TIOCSWINSZ`, 80×24 or the case's `cols=`/`rows=`), answers a cursor-position report, and fails a session that changes ICANON, ECHO or ISIG; it cannot resize mid-session, and does not look at IXON or IEXTEN | both added (§3.6) |
| pelt's open issues | which close | open: #6, #10–#18, #20, #27, #28. None is about the terminal, the editor, a resize or the special characters (the terminal gaps were wolf-lang#719, closed by s234) | **none closes** (predicted) |
| kasumi | `/home` ~30G | 29G free at the start; dash 0.5.13.4-1.1 (the oracle of record) | none |

The baseline (trunk `00e15ca` on 0.2.29, every gate, kasumi) is
re-taken before the pin and filed in §4 (`logs/base.status`); sh14's
merged numbers for this code are corpus 880/0/80, sessions 201/0/19,
statements 450 of 545, real scripts 76 aided.

## 3. Prediction (committed before the pin and the first change)

### 3.1 The pin (its own commit)

wolf 0.2.30 / lupin 0.1.53 by the six digests; std at wolf-std
`fd6bcdc` (the archive's `STD-REV`; it carries sc60's `std.signal`, which
pelt names meanings by). pelt builds on both tiers with
`--deny-warnings` and **no source change**. Every binary's bytes move.
At the bare pin: corpus **880/0/80**, sessions **201/0/19**, every
other gate as at trunk, the clause table 450 of 545, the script census
verdict for verdict as at trunk. Behaviour at the prompt is unchanged
(above: the bare pin keeps `IXON`/`IEXTEN` as found).

### 3.2 Size and resize

- **Width from `os_term_size(0)`**: `COLUMNS` first when it is a
  positive number (XBD 8.3, the user's preferred width), else the
  terminal's columns, else (a size never told: 0) 80. The height is read
  with it and kept beside the width.
- **The cursor report loses its width half**: before each prompt only
  `ESC[6n` is written (the column the prompt will start in); no `ESC 7
  ESC[999C ESC[6n ESC 8`. Bytes written to the terminal before a
  prompt: 15 → 4. A terminal that never answers is asked once, as
  before.
- **`RESIZE` mid-edit**: while a line is edited the editor listens for
  `RESIZE` (unless a trap already does, or it was ignored at start),
  and the wait (§3.3) ends for it: the editor reads the new size and
  redraws — back to the row the prompt's last line started on, clear
  below, the prompt's last line and the line at the new width, the
  cursor where it was in the text. The terminal is assumed to keep its
  rows (xterm's way; an emulator that reflows them on a resize is not
  modelled, said in §8). A `trap … WINCH` still runs: a resize the
  editor took off the queue is given back when the line ends.
- Predicted: `edit-witness`'s new `resize` row red at trunk (no byte on
  the terminal within 2 s of a resize) and green at the head; a new
  session `c_ed_resize_narrow` (40 → 20 columns mid-line, screen written
  by hand from this design) green; a wrapped line typed after a resize
  wraps at the new width.

### 3.3 The wait (the timed poll retired)

- The editor's mode keeps `VMIN 0, VTIME 1` (the escape-sequence timing
  lives in the read that follows, `[os.signal.wait.fd]`), but no read
  waits for a key any more: `next_byte` blocks in
  `os_signal_wait_fd(0, set)` with `set` = `HUP` (when the editor
  listens for it) | `INT` (when the shell listens) | `RESIZE`; 0 means a
  byte, the end of input or a hang-up, then one read takes it. `HUP`
  ends the shell as before, `INT` abandons the line as before, `RESIZE`
  redraws. The polls between reads go. If the wait answers an error the
  editor falls back to sh11's timed reads and polls for that line (said,
  not expected on linux or macOS).
- **Idle cost, measured from outside** (`edit-witness`'s new `idle` row:
  the shell's context switches, every thread, over 10 s at an idle
  prompt; linux `/proc/<pid>/task/*/status`, macOS `top -stats csw`):
  trunk **about 10 a second** (s234's probe: 9.7), the head **0** (the
  row fails above 2 in 10 s). Red at trunk, green at the head.
- **A `kill -INT` at the prompt**, answered (the new prompt on standard
  error), 20 tries: trunk median about 50 ms (a uniform wait inside a
  0.1 s read), the head median under 5 ms (the row fails at a median of
  30 ms or more). Red at trunk, green at the head.
- The other `edit-witness` rows (`editing`, `hup`, `term`, `int`,
  `hangup`, `kill`) unchanged; `hangup` still ends the shell (a hang-up
  makes the wait answer 0 and the read come back empty at once).

### 3.4 The special characters and the mode bits

- **`raw_mode` clears `FLOW` and `EXTENDED`** as well as CANONICAL, ECHO
  and SIGNALS; the mode read before the line is set back after it, on
  every way out, as now. While a line is edited `IXON` and `IEXTEN` are
  off (`edit-witness`'s new `flags` row reads the termios from the other
  side: red at trunk, green at the head), and they are back on when a
  command runs and when the shell exits (the harness's exit check now
  covers `IXON` and `IEXTEN` beside ICANON, ECHO, ISIG, on every
  session).
- **`os_term_chars(0)` for each line.** The user's erase, kill,
  interrupt, end-of-file, word-erase and literal-next characters act as
  the editor's `^?`, `^U`, `^C`, `^D`, `^W` and `^V` do (emacs, and vi
  insert mode; in vi command mode only interrupt and end of file, so a
  printable erase such as `#` stays vi's `#` command there). A default
  key whose character the user moved or disabled does nothing; `^?` and
  `^H` always erase (a Backspace key sends either) unless one of them is
  another special character. Quit, suspend, start and stop do nothing
  in the editor (so Ctrl-S and Ctrl-Q, which now reach it, never freeze
  output). Reprint and discard are not taken from the terminal (Ctrl-R
  stays search; Ctrl-O does nothing). If the call fails, the defaults.
- **New sessions, against dash** (its terminal's line discipline does
  what the user set; `compare=stdout`): `stty intr ^X` then `^X`
  abandons the line and `$?` is 130 (emacs and vi); `stty erase '#'`,
  `stty kill @`, `stty werase ^T`, `stty eof ^B`, `stty lnext ^T` each
  act; Ctrl-S typed mid-line does not stop the shell (with `IXON` on the
  editor's own write of the line would never drain, and the mode's
  restore waits for the drain: the session hangs). Predicted: each red
  at the bare pin and green at the head.
- **macOS:** with `EXTENDED` off, Ctrl-V reaches the editor, so
  `c_ed_ctrl_v`, `c_ed_tab_literal` and `c_vi_insert_ctrl_v` leave
  pending (`lnext`) on both hosts: PEND-ok on linux today, passing on
  macOS in CI at the head.

### 3.5 The numbers

| | trunk / bare pin | predicted at the head |
|---|---|---|
| corpus | 880/0/80 | **880/0/80** (nothing a script sees moves) |
| sessions | 201/0/19 | **(204 + new)/0/16**: the three `lnext` cases leave pending; about ten new cases, all passing; falsified if any case fails or pending is not 16 |
| statements met | 450 of 545 | **451 of 545** (83.5%): `sh/20` (vi insert mode's erase, kill, ^V, ^W, EOF) is met once `c_vi_insert_ctrl_v` leaves pending |
| real scripts, unaided / aided | as trunk | **verdict for verdict as trunk** (`configure-sed` is a coin, sh14) |
| `edit-witness` | 6 rows | 10 rows: `flags`, `idle`, `int-latency`, `resize` red at trunk, all green at the head, both tiers, also under `taskset -c 0-3` |
| bytes before a prompt | 15 (two reports) | 4 (one) |
| idle context switches | ~10/s | 0 in 10 s |
| `kill -INT` to a new prompt, median | ~50 ms | < 5 ms |

### 3.6 Tools

- `tools/lib_session.py`: a `.keys` line `\size COLS ROWS` resizes the
  terminal (`TIOCSWINSZ` on the terminal; the kernel sends `SIGWINCH` to
  the foreground group) and the `Screen` with it, keeping its rows (no
  reflow, cut at the new margin, as xterm); the exit check reads `IXON`
  and `IEXTEN` too.
- `tools/session-record --no-second`: dash alone, the meta's `bash=`
  left out (this lane runs no bash).
- `tools/edit-witness`: `flags`, `idle`, `int-latency`, `resize`.

### 3.7 The machines

native and release, as every lane. lupin and the checked machine:
predicted unchanged from sh14 (lupin refuses at resolve by name; the
checked machine `unsupported`, "home-module method calls"), now also
because lupin refuses the three terminal builtins by name (ruling #73
R6); asked once each and recorded.

### 3.8 Plant

On branch `sh15-plant` (never to merge): the head with `raw_mode`
keeping `FLOW` and `EXTENDED` and the wait disabled (the timed reads
back). Predicted red in CI: `edit-witness`'s `flags`, `idle` and
`int-latency` rows on both tiers of linux and macOS, `c_ed_flow_stop`,
the three `lnext` cases on macOS.
