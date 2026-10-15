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

### 3.9 The result against the prediction

Measured on kasumi (linux x86-64, CachyOS, 16 cpus; dash 0.5.13.4)
and in CI (linux x86-64, macOS arm64, linux aarch64). **native** is
`tools/build --native`, **release** `tools/build --release`.

| prediction | predicted | measured | held? |
|---|---|---|---|
| 3.1 the pin builds with no source change | both tiers, `--deny-warnings` | both tiers, no change (`logs/pin.status`, at `7859c3e`) | held |
| 3.1 at the bare pin | corpus 880/0/80, sessions 201/0/19, every gate as at trunk | **880/0/80 (3)** on native, release and both under `taskset -c 0-3`; **201/0/19** on both tiers and both under `taskset`; every gate 0 (`logs/pin.status`), as trunk (`logs/base.status`) | held |
| 3.1 behaviour at the prompt unchanged at the bare pin | `IXON`/`IEXTEN` kept | the four new `edit-witness` rows red on the pin's binary exactly as on trunk's (`logs/red-edit-witness-pin.log`), and the eleven new sessions 1 pass / 10 fail on it as on trunk's (`logs/red-new-cases-pin.log`, `red-new-cases-base.log`) | held |
| 3.2 the width from `os_term_size`; one report, not two | 15 → 4 bytes before a prompt | `ed_query` writes `ESC[6n` only (`src/sh/edit.lu`); the sessions' screens, which the harness's terminal answers, are unchanged | held (read from the code and the screens; the byte count was not captured by a tool) |
| 3.2 resize mid-edit | `resize` row red at trunk, green at the head; `c_ed_resize_narrow` green | red at trunk and the pin ("redrawn after the resize False"), green at the head on both tiers and under `taskset` (redrawn in 10.2 ms on kasumi, 89.6 ms on macOS CI); `c_ed_resize_narrow` green on kasumi and both CI hosts, red at trunk; `c_ed_resize_trap` green (and green at trunk too: the trap never depended on the editor) | held |
| 3.3 idle context switches | trunk ~10/s, head 0 | trunk **96 in 10 s** (9.6/s), the plant 96–101; the head **0 in 10 s** on both tiers, under `taskset -c 0-3`, and on macOS CI (`top -stats csw`) | held |
| 3.3 `kill -INT` latency | trunk median ~50 ms, head < 5 ms | trunk median **106 ms** (max 109), the pin 106; the head **1.1 ms** median on kasumi (the harness's own 1 ms pump is the floor), 7.3 ms on macOS CI | head held; **trunk's figure missed**: about one tenth of a second, not half (each `kill` lands in a fresh `VTIME` read started by the previous prompt, so the wait is nearly the whole read, not a uniform part of it) |
| 3.3 the other witness rows unchanged | as trunk | as trunk, except `hangup`: status **−1** (SIGHUP) at the head where trunk exited 0 | **changed, not predicted**: the hang-up's SIGHUP now ends the wait before the empty read is seen; pelt then dies of it with the mode put back, as it already did for a `kill -HUP` (dash dies of SIGHUP on a hang-up too) |
| 3.4 `FLOW`/`EXTENDED` off while editing, back after | `flags` red at trunk, green at the head | red at trunk, the pin and the plant ("while editing (True, True)"); green at the head on both tiers, `taskset`, and macOS CI | held |
| 3.4 the stty characters, against dash | each red at the bare pin, green at the head | `c_ed_stty_intr`, `c_vi_stty_intr`, `c_ed_stty_erase`, `c_vi_stty_erase`, `c_ed_stty_kill`, `c_ed_stty_werase`, `c_ed_stty_eof`, `c_ed_stty_lnext`: all red at trunk and the pin, all green at the head | held |
| 3.4 Ctrl-S | red at the bare pin, green at the head | `c_ed_flow_stop` red at trunk and the pin on linux and in the plant on linux CI; green at the head everywhere. **On macOS the plant's run passed it**: macOS did not hold pelt in the mode's restore with output stopped | held on linux; **not red on macOS** |
| 3.4 the three `lnext` cases pass on macOS | pending leaves on both hosts | they reach the editor on macOS now, and **then failed on macOS for another reason**: macOS's `od -c` pads its columns, which no run had shown because the key never arrived (CI 38745068019). Re-recorded from dash with the blanks taken out (`198cb96`); green on both hosts | held, after a test fix |
| 3.5 sessions | (204 + new)/0/16 | **215/0/16** (11 new) on both tiers and under `taskset`, kasumi and CI | held |
| 3.5 statements | 451 of 545 | **451 of 545 (83.5%)** | held |
| 3.5 corpus | 880/0/80 | **880/0/80 (3)** on both tiers and under `taskset` | held |
| 3.5 real scripts | verdict for verdict as trunk | trunk (`sc/pelt-base`, the static build of `00e15ca`): unaided 76 same / 3 differ / 1 unstable, aided the same. Head (`9acf62c`): aided **76 / 3 / 1, verdict for verdict as trunk**; unaided printed **75 same / 5 differ**, the two moved rows being `configure-sed` (its filesystem-timestamp-resolution line, sh14's coin) and `pfetch` (its memory-in-use line; dash agreed with itself that run, so it was not called unstable). Re-run three times at the head: `configure-sed` same, same, differs; `pfetch` unstable all three (`scripts/sc-head-recheck.txt`) | held in substance (the three real differences are trunk's: xzgrep, zgrep, zdiff, a process per pipeline stage); **missed as printed** on the unaided pass, for the two known timing coins |
| 3.7 lupin and the checked machine | unchanged; lupin also refuses the three builtins | the checked machine: `unsupported`, "home-module method calls in checked execution", `phase_reached mem`; lupin: `unsupported` at resolve naming `os_signal_default` (`logs/machines.txt`) | held in kind; lupin names the first refusal it meets, which is still `os_signal_default`, so its refusal of the three terminal builtins is not seen through pelt |
| 3.8 the plant | `flags`, `idle`, `int-latency` red both tiers both hosts; `c_ed_flow_stop`; the `lnext` cases on macOS | CI 38745143567 (`ci/plant-38745143567.txt`): `flags`, `idle`, `int-latency` **and `resize`** red on both tiers of linux and macOS (the plant's timed-read fallback does not poll `RESIZE`); `c_ed_flow_stop` and `c_ed_resize_narrow` red on linux; on macOS `c_ed_resize_narrow` and the four Ctrl-V cases red (those four were also red at the unplanted head then, for `od`'s padding, so on macOS they do not isolate the plant) | held, with `resize` red too and Ctrl-S not red on macOS |

**Not predicted.**

- **A hang-up ends pelt by SIGHUP now** (above).
- **macOS's `od -c` pads**: the Ctrl-V cases had never produced output on
  macOS before.
- **A plant with `FLOW` on does not hang on macOS** when Ctrl-S is typed
  (linux: the restore's drain waits for ever; macOS: it went on).
- **dash needs an empty line after an interrupt at its prompt** before a
  following line is read cleanly (the first recording of
  `c_ed_stty_intr` ran `echo st=$?` and the next line together); the
  cases type one, as sh11's `ctrl_c_prompt` does.

## 4. Evidence index

- **The prediction:** `2f644d4`, before the pin (`7859c3e`) and the
  first change under `tools/` (`26cf3fa`) and `src/` (`f436961`).
- **The toolchain:** `notes/sh15-evidence/logs/fetch6.log` (six archives
  hashed twice, the version lines, `STD-REV`).
- **The gauntlets** (`notes/sh15-evidence/logs/`): `base.status` (trunk
  `00e15ca` on 0.2.29), `pin.status` (`7859c3e`), `head.status`
  (`9acf62c`, the code of the head): fmt, both builds, `wolf test`, the
  clause census, the width table, difftest on both tiers and both under
  `taskset -c 0-3`, the difftest plant, sessions on both tiers and both
  under `taskset`, the session plant, glob-rss, loop-rss, shape-rss,
  exec-witness, edit-witness on both tiers and both under `taskset`,
  hist-witness, signal-witness on both tiers and both under `taskset`,
  `oracle-record --check`, the static build: every exit status 0. The
  sessions again at `198cb96` (the `od` re-recording):
  `final-sess-*.log`, `final.status`.
- **Seen red:** `red-edit-witness-pin.log` (the pin's binary),
  `red-new-cases-base.log` and `red-new-cases-pin.log` (the eleven new
  sessions on trunk's and the pin's binaries: 1 pass, 10 fail),
  `plant-edit-release.log` (the plant on kasumi), and CI run
  38745143567 on `sh15-plant` (`ci/plant-38745143567.txt`).
- **The machines:** `logs/machines.txt`.
- **The census:** `notes/sh15-evidence/scripts/` — `base-*` and `head-*` (`.tsv`, `.log`, `.bin`: the static binary's digest), the head re-checks of the two coins.
- **CI:** PR wolffe-lang/pelt#29; run 38749457787 green at `198cb96` on all three jobs (linux x86-64 and macOS arm64: corpus 880/0/80, sessions 215/0/16 on both tiers, edit-witness 10 of 10 on both tiers: idle 0 switches, `kill -INT` median 1.1 ms linux / 7.2–8.0 ms macOS; linux aarch64: both tiers still refused by name at 0.2.30). The PR run at `a0ab931` (38745068019) was red on macOS for the four Ctrl-V cases (`od`), fixed in `198cb96`.

## 5. Done-when

- Branch `sh15`, PR #29 open and unmerged, CI green at the head;
  `wolf/tools/lane-audit.sh pelt sh15 29` run from the org directory,
  its exit status read directly.
- pelt issues: **none closes** (§2: none of the open issues is about the
  terminal). wolf-lang#719 (W05) was closed by s234.

## 6. Wolf findings

No defect found in wolf 0.2.30's terminal surface: every call answered
as `[os.term.size]`, `[os.term.chars]`, `[os.signal.wait.fd]` and
`[os.term.mode]` say, on linux and macOS, both tiers. Observations, not
filed:

1. **wolf-std `fd6bcdc` still has no wrappers** for `os_term_size`,
   `os_term_chars` and `os_signal_wait_fd` (owed at the next std pin,
   the CHANGELOG says); pelt calls the builtins.
2. **lupin names `os_signal_default` first** when it refuses pelt, so
   ruling #73 R6's refusals of the three terminal builtins are not
   visible through pelt.
3. **The checked machine still refuses pelt** ("home-module method
   calls"), as at 0.2.28 and 0.2.29.
4. **`os_signal_wait_fd` with an empty set** was not asked; pelt never
   passes one (it falls back to timed reads if the set would be empty,
   which needs every one of `HUP`, `INT` and `RESIZE` ignored at start).

## 7. Not verified, and inferred

- **A reflowing terminal** (VTE, kitty, iTerm2 rewrap rows on a resize):
  the redraw assumes the rows stay as they were (xterm, the harness's
  `Screen`). On a reflowing terminal a wrapped line can leave a stale
  row above or below after a resize. No real emulator was driven by a
  person.
- **Two resizes inside one escape sequence or one UTF-8 character**: the
  redraw runs between bytes and the key in progress is finished after
  it; not typed by any case.
- **The timed-read fallback** (a host where `os_signal_wait_fd` fails)
  runs only in the plant; it does not redraw on a resize.
- **`COLUMNS` set and a resize**: the width stays `COLUMNS` (XBD 8.3) and
  nothing is redrawn; read from the code, no case.
- **The height** is read and kept beside the width; nothing in the
  layout uses it yet.
- **Reprint and discard** (Ctrl-R, Ctrl-O on most terminals) are not
  taken from `os_term_chars`; Ctrl-O reaching the editor is shown by
  `EXTENDED` being off (`flags`), not by a key typed.
- **macOS** by CI only (no build on nomad-1). The census scripts are
  linux-only. linux aarch64: no tier builds at 0.2.30 either (asserted
  in CI).
- **The bytes before a prompt** (15 → 4) are read from the code.
- **bash was not run** by this lane; the sh11 cases recorded from bash
  keep their transcripts, except the three Ctrl-V cases, now dash's.
