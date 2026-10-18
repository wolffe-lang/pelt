# The plan: from here to a shell you would log in to

Written 2026-10-11 from the measurements in [`CENSUS.md`](CENSUS.md),
at pelt `b32bebc` (wolf 0.2.27). It is for a contributor: where pelt
is, what is missing ranked by what it breaks, the pieces of work that
remain and the order they can land in, and for every piece what it
needs from [wolf-lang](https://github.com/wolffe-lang/wolf-lang) or
[PAX](https://github.com/wolffe-lang/pax). Issue numbers are wolf-lang's
unless marked; a "to be filed" item has its text and witness in the
sh06 record (`notes/sh06-the-census.md`) and gets a number when it is
filed.

## Where pelt is

- **The language is nearly whole.** Grammar, expansions, redirection
  and shell commands meet 91–100% of their POSIX statements
  (CENSUS.md §1). The special built-ins meet 87%.
- **Three in four POSIX statements are met**: 400 of 527 testable
  statements of XCU chapter 2 and the built-ins' pages; 414 since
  sh07 (S1, below); since sh11 the table has 544 statements, and
  since sh13 (S4) 431 of them are met; since sh12 (H3b) 439 of 545;
  since sh14 (the signals, wolf 0.2.29) 450 of 545; since sh15 (the
  terminal, wolf 0.2.30) 451 of 545; since sh17 (the POSIX gaps:
  aliases, `$'…'`, `pipefail`, `type`, `hash`, `command -p`, `read`,
  the command line) 487 of 545; since sh18 (job control, wolf 0.2.32)
  505 of 546.
- **Five in eight real scripts run as under dash**: 50 of 80
  (configure, automake and libtool helpers, git's test library, Debian
  and Alpine package scripts, init scripts, small utilities). With four
  gaps fixed it would be 72 of 80. **Since sh07: 66 of 80**, one more
  (pfetch) differing only where dash differs from itself; the other 13
  stop at `umask` (10, S4) or need a process per pipeline stage (3,
  gap 7). **Since sh13: 76 of 80**; the 3 left are gap 7.
- **Interactive pelt is a prompt, not yet a place to work.** `PS1`,
  `PS2`, `ENV`, Ctrl-C and Ctrl-D behave as dash's do. There is no line
  editor, no history, no completion, no job control and no aliases.
  (Since sh11, sh12 and sh16 it has the editor, the history and
  completion; since sh17, aliases; since sh18, job control.)
- **PAX already runs pelt as pid 1** (pax `5afb903`), threads and
  signals included. H4's milestone is met in substance, ahead of H3.
- **Speed.** Running programs costs about 1.5 times what dash does.
  Pelt's own work per command costs 3.9 times on the release tier and
  10 times on the native tier.
- **Memory.** A loop of simple commands stays flat. But each pipeline,
  command substitution or function call keeps 1 to 10 KB that is never
  freed. A script of 20,000 pipelines peaks at 258 MB. **Since sh08
  (S2) every shape is flat**: pipelines, substitutions, subshells,
  calls, `case`, `for`, long scripts and typed lines keep under 0.2 KB
  a turn, and the 20,000-line script peaks at about 3.5 MB.

## The gaps, ranked by what they break

The order is by real scripts broken first, then by silent wrong answers,
then by statements and by what a person at the prompt meets. "Scripts"
counts the 80 in `tools/script-census`.

| # | gap | breaks | whose |
|---|---|---|---|
| 1 | **done in sh07**: `test -r/-w/-x/-L/-h/-ef` answer wrongly | 14 scripts (libtool, git's tests, debconf and so four Debian postinsts, init scripts, `service`, `which`) | pelt; exact access as the caller wants a wolf call (to be filed: W07) |
| 2 | `umask` missing | 9 scripts (install-sh, config.guess, every configure through it) | wolf-lang s230 (`os_umask`, merged for the release after 0.2.27), then pelt |
| 3 | **done in sh08**: memory kept per pipeline, substitution, function call and script line | any long script or session; not a script failure in the census, which runs each script once | pelt |
| 4 | **done in sh07** (recorded) **and sh14** (caught: wolf 0.2.29 has a meaning for every signal POSIX names): `trap ACTION 13` (a signal number with no wolf meaning) refused | 7 scripts | done |
| 5 | **done in sh07**: a bracket expression holding `/` never matches outside file names | 4 scripts, the first wall of every autoconf configure | pelt |
| 6 | **done in sh07**: unquoted `$*` in an assignment joins with nothing: **a silent wrong answer** (`host_os=linuxgnu`) | 3 scripts | pelt |
| 7 | no process for a subshell or an in-process pipeline stage: stages run one after another, a descriptor written from a stage is lost, an endless producer never ends | 3 scripts, 7 statements | wolf-lang or pelt, by ruling R1 (to be filed: W01) |
| 8 | **UTF-8 half done in sh07**: bytes above 0x7f become `?` on their way out: **a silent wrong answer** (a certificate with a non-ASCII name is left out of the bundle) | 1 script; every non-ASCII file name | pelt; bytes that are not UTF-8 need wolf byte strings (to be filed: W06) |
| 9 | **done in sh17**: aliases | 17 statements; daily use | pelt |
| 10 | **done in sh18** (wolf 0.2.32: `os_wait_poll`, the group sends, `os_set_pgid`): job control on linux and macOS. What is left waits on gap 7: a subshell, a compound command after `&` and a pipeline stage pelt runs itself are not processes, so they are not jobs | 14 statements; daily use | done; gap 7 for the rest; PAX's own is px48's |
| 11 | line editing and history | daily use; 7 statements (`fc`, vi mode, `!` in `PS1`) | pelt; the terminal's size, resize, a wait a signal ends and the special characters are in (sh15, wolf 0.2.30) |
| 12 | **done in sh17**: `$'…'` (new in POSIX.1-2024) | 7 statements | pelt |
| 13 | **done in sh14** (wolf 0.2.29): `kill` built in, `$$`/`PPID` everywhere; **sh18**: `kill %job`, `kill 0`, `kill -- -N` and `kill -1` reach groups | 8 statements | done |
| 14 | `ulimit` | 4 statements | wolf-lang (to be filed: W02) |
| 15 | about forty corners, one or two statements each (`type`, `hash`, `command -p`, `pipefail`, declaration utilities, `read -d`, `trap -p`, `set -v`, `PS4`, `.` of a FIFO, …); **sh17 did `type`, `hash`, `command -p`, `pipefail`, `read` and the command line** (P02–P06, P08); P09 and P10 remain | 53 statements | pelt |
| 16 | speed: the interpreter's per-command allocation; 57 system calls per program started; a `PATH` search per command (**gone in sh17**: a table of found utilities, as `hash` lists) | 3.9× and 10× dash on expansion loops | pelt; a cheaper spawn (to be filed: W08) |

Each gap has a pending case named in `tests/diff/PENDING.md` or
`tests/session/PENDING.md`. When a case passes, the commit that makes
it pass removes it from that list.

## The phases from here

The old phase table (H1 language, H2 plumbing, H3 interactive, H4 PAX)
stays. H1 and H2 are met. Below, H3 is split into pieces that can each
land alone, and a script phase comes first: it breaks the most and
needs the least from upstream.

### S: the scripts (pelt's own work, nothing upstream)

- **S1, the script walls:** gaps 1, 4, 5, 6 and 8 (the UTF-8 half),
  plus `.` of a FIFO. Done when `tools/script-census` reports 72 or
  more of 80 without `--aided`. **Landed in sh07 at 66 of 80**: the
  72 counted `umask` as routed around, and `umask` is S4's; after S4
  at most 76 of 80 can run as under dash, the last 3 being gap 7 (`notes/sh07-the-script-walls.md`).
- **S2, memory:** gap 3. Done when `tools/loop-rss` also holds flat a
  loop of `true | true`, `x=$(true)`, a function call and a 20,000-line
  script. **Landed in sh08**: `tools/shape-rss` holds 22 shapes flat
  (loops, scripts, typed lines) on both tiers in CI; what a turn still
  keeps is a superseded variable value and the editor's history line
  (`notes/sh08-the-memory.md`).
- **S3, the small built-ins and corners:** gap 15, `type`, `hash` (it
  also removes the per-command `PATH` search), aliases (gap 9) and
  `$'…'` (gap 12). Done when those cases leave `PENDING.md`.
  **Landed in sh17** for P02–P06 and P08 (`notes/sh17-the-posix-gaps.md`):
  every one of their cases left `PENDING.md`; P09's and P10's corners
  are what is left of S3.
- **S4, when the release carrying s230 lands:** `umask` (gap 2). Done
  when the census is 80 of 80, or each script left is named with what
  it waits on. **Landed in sh13 on wolf 0.2.28 at 76 of 80**: the ten
  `umask` scripts run as under dash; xzgrep, zgrep and zdiff wait on
  gap 7, and pfetch's output moves between dash's own runs
  (`notes/sh13-the-umask.md`).

### H3, split

- **H3a, the line editor.** Raw mode, emacs keys, history recall,
  UTF-8 and wide characters, lines longer than the terminal's limit.
  wolf 0.2.27 is enough to start: `os_term_set_mode`, byte reads and a
  timed read (CENSUS.md §3). A resized window needs the window size and
  `SIGWINCH` (W05). Restoring the terminal when the shell is killed is
  also W05. Proved by the `c_ed_*` sessions. **Moved to wolf 0.2.30 in
  sh15**: the width from `os_term_size`, a redraw on `RESIZE` mid-line,
  the wait in `os_signal_wait_fd` (an idle prompt makes no context
  switch), the user's `stty` characters, and `FLOW`/`EXTENDED` off while
  a line is edited. Restoring the terminal after an uncatchable death
  stays out (the runtime restores nothing, by rule).
- **H3b, history.** The history list, Up and Down, Ctrl-R, `fc`,
  `HISTFILE`, `HISTSIZE` and `!` in `PS1`. Nothing upstream on Linux.
  On PAX a history file needs a writable tree (px27). Proved by
  `c_hist_*` and `c_ps1_bang`. **Landed in sh12**: `fc` (POSIX's
  forms; bash --posix the oracle, POSIX where they part), a shared
  `HISTFILE` (`$HOME/.sh_history` by default) cut to `HISTSIZE`, Ctrl-R,
  vi `[number]v`, `!` in `PS1`; the file across shells is
  `tools/hist-witness` (`notes/sh12-the-history.md`).
- **H3c, the prompt's own:** aliases at the prompt, `ignoreeof`,
  `MAIL`. Nothing upstream. Aliases at the prompt landed in sh17.
- **H3d, completion and vi mode,** after rulings R3 and R2. vi mode is
  POSIX (`set -o vi`). Completion is not POSIX. **Landed in sh16**
  (ruling #69 R3: files, commands, variables, not programmable): Tab in
  emacs mode and vi insert mode, the second Tab lists, names quoted to
  read back; bash's and mksh's black-box behaviour where POSIX is
  silent, each choice recorded (`notes/sh16-the-completion.md`).
- **H3e, job control on Linux.** A wait that reports a stopped child
  and can be woken by a signal or by any child (W03, #680). `SIGCONT`
  and a signal to a process group (W03). **Landed in sh14 on wolf
  0.2.29:** `kill` built in, with job ids for the shell's own `&` lists
  (#141); signals ignored on entry left alone (#681); the poll race
  gone and pelt's barrier with it (#691, `tools/signal-witness`); a
  trap for every signal POSIX names (#679). **Landed in sh18 on wolf
  0.2.32** (`notes/sh18-job-control.md`): each pipeline of programs in
  a group of its own, the terminal handed over and taken back, the
  wait on `os_wait_poll` and `os_signal_wait`, stops as `128 + N`,
  `jobs` (`-l`, `-p`), `fg`, `bg`, Ctrl-Z, every job id, the notices,
  `set -b` (at once, as POSIX), `kill`'s groups, an interruptible
  `wait`, `exit` with stopped jobs. Proved by the eleven `c_jc_*`
  sessions and eleven new ones under `dash -i -m`. Pending on H3f: a
  subshell, `{ … } &` and an in-process pipeline stage are not jobs.
- **H3f, subshells as processes.** Gap 7, by ruling R1: either wolf
  gains a fork (W01), or pelt starts itself again for a subshell and
  hands it the state it needs. Until then, job control's "a pipeline is
  one process group" can only hold for pipelines of programs.

### H4, restated

pelt is PAX's pid 1 today, and its script plumbing, `trap` and Ctrl-C
run there. What is left of M-SH4 ("init's scripts run under it"):

- the S phase (above), so that init-style scripts run on Linux;
- a writable tree on PAX (px27) for history files, here-documents into
  files, `>` anywhere, and pid files;
- job control on PAX: process groups, sessions, `tcsetpgrp` and stopped
  processes are PAX work (a pax lane). It comes after H3e works on
  Linux;
- a terminal on a slow line: a session typed a byte at a time at about
  500 baud already gives the same output (CENSUS.md §3). The line
  editor must keep that true, and redraw little.

### "Drop-in `/bin/sh`": what proves it

1. **The script census as a gate.** `tools/script-census` runs in CI on
   a schedule (it needs podman and about 2 GB of images, so not on every
   push) and must report 80 of 80, or every remaining script named in
   `PENDING.md` with its reason. The set grows: more configure scripts,
   whole Debian package installs.
2. **pelt as `/bin/sh` in a container that builds software.** Replace
   `/bin/sh` with pelt in a Debian and an Alpine image. Then
   `./configure && make && make check` four autoconf packages, and
   `dpkg -i` / `apk add` the packages whose scripts are in the census.
   Everything must pass as it does with dash.
3. **The clause table.** `tools/clause-census` at 100% of testable
   statements, with every untestable one argued in the table.
4. **Speed and memory bounds.** At most 1.5 times dash on `tools/bench`'s
   four loops on the release tier, and memory flat under every loop and
   session shape in CENSUS.md §3. Each bound becomes a CI gate.

### After POSIX

Each of these is a ruling first. None is started before POSIX is met.

- **completion beyond file names** (R3: files, commands and variables,
  landed in sh16; nothing programmable);
- **history expansion** (`!!`, `!$`), which is not POSIX (R4);
- **`local`**: pelt has it and Debian's scripts use it. Keep it, with
  dash's meaning (R5);
- arithmetic beyond POSIX (`++`, `--`, `,`): follow dash (R6);
- a `set -o emacs` name for the default editing mode (R2);
- nothing from bash's or zsh's languages (`[[`, arrays, `function`)
  unless a ruling asks for it.

## What each piece needs from upstream

| piece | wolf-lang | PAX |
|---|---|---|
| S1, S2, S3 | nothing (W07 for exact `test -r/-w/-x`; mode bits and uid are close without it) | — |
| S4 `umask` | done: wolf 0.2.28's `os_umask` (sh13) | `umask(2)` on PAX (px27 lists it) |
| H3a editor | done: wolf 0.2.30's `os_term_size`, `os_term_chars`, `os_signal_wait_fd`, `FLOW`/`EXTENDED` (sh15); restoring after SIGKILL is out by rule | a console that answers `TIOCGWINSZ` (px19's framebuffer does) |
| H3b history | — | px27 (a writable tree) for `HISTFILE` |
| H3e job control | done: wolf 0.2.31's `os_wait_poll`, `os_signal_send_group`, `os_signal_send_all`, `os_set_pgid` (sh18, at 0.2.32) | process groups, sessions, `tcsetpgrp`, stopped processes (px48, done) |
| H3f subshells | W01, or nothing under R1(B) | `clone` without `CLONE_VM` if W01 is a real fork |
| `kill`, `$$`, `PPID` | done: wolf 0.2.29's `os_signal_send`, `os_signal_number`, `os_pid`, `os_ppid` (sh14) | `kill(2)` to any pid, `getppid`, and `rt_sigaction` asked what a signal's disposition is |
| `trap` for every signal | done: wolf 0.2.29's twenty meanings and `os_signal_ignored` (sh14) | the signals already delivered (px26); every one POSIX names, and a poll that changes the thread's mask (`rt_sigprocmask`) |
| the editor's wait | done: wolf 0.2.30's `os_signal_wait_fd` (sh15) | `poll`/`ppoll` on a terminal and a pipe, and `TIOCGWINSZ` |
| `ulimit` | W02 | `prlimit64` |
| `~login` | W04 | `/etc/passwd` in the image |
| non-UTF-8 bytes | W06 | — |
| speed | W08 (a cheaper spawn) | — |
