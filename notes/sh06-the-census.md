# sh06 — the census (what pelt lacks, measured, and the plan that follows)

This file is the lane's record. §3 is committed before the first
measurement; §2 and §4 are filled in as the work lands. The plan the
census produces is `docs/PLAN.md`.

## 1. Forbidden, absolutely

No shell's source and no line-editing library's source is read or
searched for: facts come from POSIX.1-2024 (XCU chapter 2 and the
utility pages), man pages read as documentation, and black-box runs of
`dash`, `bash --posix`, and (interactive behaviour only) `bash` and
`zsh` as installed. No change under `src/`: tests marked pending, tools
and documents only. Third-party scripts run only inside throwaway
containers with nothing of the host mounted but a scratch directory
under `~/lanes/sh06/`, with no network once their inputs are fetched,
never as root on a host; none is committed unless its licence allows it
and the file says so. No `extern "c"` proposed. No `rm` outside
`~/lanes/sh06/` and this lane's clones; no `git add -A`; no merge; no
attribution trailers. Strict evidence; concurrency rows under
`taskset -c 0-3`. Scratch under `~/lanes/sh06/` (`TMPDIR` points there
for every tool run).

## 2. Inputs, verified

Filled in after §3 is committed (the corpus is not run before then).

## 3. Prediction (committed before the first measurement)

Written from reading only: the track's record, `tests/diff/PENDING.md`,
`tests/session/PENDING.md`, the names in `src/sh/builtin.lu`'s dispatch
table, and chapter 11 of the wolf specification at the 0.2.27 tag.
Nothing has been built or run by this lane yet.

### 3.1 The clause census

- The census will list **between 450 and 650** testable statements for
  XCU chapter 2 and the built-in utilities' pages.
- pelt at `b32bebc` meets **74%** of them (falsified below 65% or above
  83%). By part: sections 2.2–2.7 and 2.9–2.10 (quoting, tokens,
  expansions, redirection, commands, grammar) **above 90%**; 2.11
  (signals), 2.12 (the execution environment) and 2.14/2.15 (built-ins)
  between **60% and 80%**; the utility pages `fc`, `jobs`, `fg`, `bg`,
  `kill`, `alias`, `unalias`, `type`, `umask`, `ulimit`, `hash` **near
  0%**, because the dispatch table either has no row for them or
  answers "not supported yet"; `sh`'s own page (options, `-c`, `-s`,
  `ENV`, `-n`) around **70%**.
- The corpus as it stands covers **under half** of the listed
  statements by a passing case; the census will add **more than 150**
  new cases, and **between 60 and 120** of them land pending.
- dash and `bash --posix` will disagree on **between 15 and 40** of the
  new cases; POSIX's words will side with bash more often than dash
  (dash's `echo` and `read` without `-r` aside).

### 3.2 The five largest gaps, by scripts broken (predicted order)

1. **No fork**: a subshell and an in-process pipeline stage are not
   processes — `cmd | while read …` against an endless or large
   producer, `( exec … )`, `( cd …; … ) &` with a later `wait`,
   variable and option isolation under signals. Predicted to explain
   the largest count of failing real scripts.
2. **Missing regular built-ins that scripts call unconditionally**:
   `type`, `alias`/`unalias`, `umask`, `kill` with job ids, `hash`,
   `ulimit`. `umask 022` at the top of an installer and `type foo
   >/dev/null` as a probe are the common shapes.
3. **Signals with no wolf meaning** (`trap … PIPE ALRM USR1`, signal
   numbers above the nine meanings) and `trap` inheritance rules
   (wolf-lang#679, #681).
4. **`$$` and process identity off linux; `wait` semantics** (`wait`
   not interruptible, `wait -n` absent, wolf-lang#141, #680).
5. **Field and pattern corners in real scripts**: `IFS` edge cases,
   `case` patterns with bracket classes and locale classes, `${x#…}`
   with quoted patterns, here-document corners, `set -e` exemptions,
   `set -u` with `$@`. Each small, together a long tail.

Interactive gaps (line editing, history, job control) break no script
and so rank below these by that measure; by "would a person log in to
it" they rank first.

### 3.3 The script census

- Of the fixed set (predicted **25 to 40** scripts), **35%** run to the
  same output and exit status as under dash (falsified below 15% or
  above 60%).
- **No autoconf `configure` script completes identically.** The first
  failure in each is in the first 300 lines of executed shell, and at
  least two of them fail on the same construct.
- Small `shellcheck`-clean utilities pass at **above 60%**; Debian and
  Alpine maintainer scripts at **about 50%**; `install-sh` passes;
  `config.guess` passes or fails only on a subshell/pipeline shape;
  `ltmain`-style helpers fail.
- git's shell test helper library is **not** POSIX `sh` as shipped (it
  uses `local` and a few other extensions) and runs under dash only
  because dash carries them; it fails under pelt.
- The three most-counted smallest constructs: an in-process
  pipeline/subshell shape, an unsupported built-in, and an expansion or
  `set -e` corner.
- pelt will **hang or time out** on at least two scripts (a pipeline
  whose producer never ends without a reader's exit).

### 3.4 The interactive census

- Passing today: `PS1`/`PS2` expansion, `ENV`, Ctrl-C at the prompt and
  over a child, `exit`/Ctrl-D, the terminal's own canonical editing.
- Every one of these is a named gap: any key beyond the line
  discipline's (arrows, Home/End, Ctrl-A/E/K/R), history in any form
  (`fc`, `HISTFILE`, `HISTSIZE`), completion, `jobs`/`fg`/`bg`/Ctrl-Z/
  `set -m`, aliases, `PS4` under `set -x` at the prompt (expected to
  pass), a resized window (no window-size call in chapter 11, no
  `SIGWINCH` meaning).
- **wolf can already do a usable single-line editor**: raw mode
  (`os_term_set_mode` with `CANONICAL` and `ECHO` off, `VMIN`/`VTIME`),
  byte reads on descriptor 0 and writes of escape sequences. What is
  missing for a good one, each to be shown by a witness: the window
  size (`TIOCGWINSZ`), a `SIGWINCH` meaning, a read that waits for
  "input or a signal", a character-width table (`wcwidth`), and a way
  to restore the mode when the shell is killed.
- Startup: pelt within **3×** of dash (both under 5 ms on kasumi).
  Memory after 10,000 typed commands: **under 6 MB** and flat (sh03's
  gate), against dash's ~2.6 MB.
- Job control is **not startable today on Linux** without wolf-lang
  work (stop reporting, `SIGCONT`, a signal to a group, an
  interruptible wait: #680 and the `[os.term.note]` list), and not on
  PAX without process groups and sessions.

### 3.5 Speed

- Fork-heavy loop (1,000 external commands): pelt within **0.8× to
  1.5×** of dash (spawn dominates both).
- Pipeline-heavy loop: pelt **1.5× to 4×** slower.
- Parameter-expansion loop (no external command): pelt **5× to 20×**
  slower; this is the worst one, and the time is in allocation and
  string copying per command (`copy region` per command, `Map` lookups
  for variables), not in system calls.
- A `configure`-shaped script (many `test`, `case`, `echo`, short
  substitutions): pelt **2× to 6×** slower, dominated by command
  substitutions that capture output from in-process built-ins.

### 3.6 Whose work each gap is

- **pelt's own, no upstream need:** `type`, `alias`/`unalias`, `hash`,
  the remaining expansion and `set` corners, `set -v` (pelt#6), `fc`
  and history files, line editing in raw mode (first cut), `PS1` forms,
  completion of file names, speed.
- **Waits on wolf-lang:** `umask` (s230's `os_umask`, held for a
  release), `kill` as a built-in and `$$` everywhere (#141), `trap` for
  every signal (#679, #423), an interruptible and non-blocking wait
  (#680), ignored-at-start (#681), `ENOEXEC` (#682), the poll race
  (#691), job control (stop reporting, `SIGCONT`, group signals: no
  issue yet — to be drafted here), `~user` (no user database: to be
  drafted), `ulimit` (no `getrlimit`/`setrlimit`: to be drafted),
  window size and `SIGWINCH` (to be drafted), uid (#633, for `PS1`'s
  `#`/`$` choice and `test -O`), **fork or its equivalent** for
  subshells and pipeline stages (to be drafted; the largest).
- **Waits on PAX:** process groups, sessions, `tcsetpgrp`, stopped
  processes (job control on PAX); a writable tree (px27: history file,
  here-document temp files, `>` anywhere).

### 3.7 The order the plan will take

1. The fork question first, as a ruling: a real `fork` surface in
   wolf, or pelt re-executing itself for subshells and in-process
   pipeline stages. Everything in 3.2(1) hangs on it.
2. The script-breaking built-ins pelt can write alone (`type`, `alias`,
   `hash`, then `umask`/`kill`/`ulimit` as their primitives arrive).
3. The long tail from the clause census, by area, with the corpus.
4. Line editing (raw mode, emacs keys) and history together — the
   first thing a person notices.
5. Signals completed (#679–#681, #691) and then job control on Linux.
6. Job control on PAX, after PAX has groups and sessions.
7. "Drop-in `/bin/sh`" proved by the script census run as a CI gate,
   and by pelt as `/bin/sh` in a container that builds real software.
8. After POSIX: completion, history expansion, `local` and the other
   extensions scripts assume — each a ruling.

## 4. Evidence index

Filled in as the work lands.
