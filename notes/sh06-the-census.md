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

## 2. Inputs, verified (2026-10-11, after `4437c81`)

| input | contract says | measured | drift |
|---|---|---|---|
| pelt trunk | `b32bebc`, wolf 0.2.27 / lupin 0.1.50, corpus 443/0/7, sessions 85/0/0 | `origin/trunk` = `b32bebc23fa6f7b6…`; built both tiers on kasumi from the pinned archives; corpus **443/0/7** on both tiers (`logs/diff-release-base.log`), sessions **85/0/0** (`logs/sess-release-base.log`); the seven pending: `pending/exec_pid`, `pending/pid` (PEND-ok on linux), `pending/subshell_signal`, `pending/trap_ignore_usr1`, `pending/trap_usr1`, `pending/wait_interrupted`, `tilde/user`; pelt#6 open (`set -v`) | none |
| the archives | 0.2.27 / 0.1.50 by digest | release 409367590: wolf linux x86-64 `5e17eebed7ffbb3e…`, macOS arm64 `ea461a7668d98604…`; release 409303515: lupin linux x86-64 `e2867a3515d4691f…`, macOS arm64 `2cbd192d2f4fa8b9…` (the release API's digests); `tools/fetch-toolchain` accepted them on kasumi; `wolf --version` line 1 `wolf 0.2.27 (wolfgang, pin 0ddda6b)` | none |
| the oracle | dash 0.5.13.4 on kasumi | `dash 0.5.13.4-1.1` (sha256 `c6221703b6197ce2…`), `bash 5.3.20-2` (`a8ce2b3c38c81853…`): `tests/diff/ORACLE`'s | none |
| waits upstream | #141, #679, #680, #681, #682, #691, #633 | all seven OPEN (`gh issue view`); also #423 and #614 OPEN | none |
| PAX | pax `5afb903`: threads, signals, Ctrl-C to "every process"; no groups, sessions, `tcsetpgrp`, stopped processes; px27 a writable tree | pax trunk is now **`1af462d`**: px27's notes are on trunk (the writable tree has landed since the contract was written); px24, px28, px29, px30 open | px27 landed |
| wolf's terminal surface | `os_term_mode` and the rest of spec chapter 11 | `spec/11-os.md` at `v0.2.27`, §8: `os_pgid`, `os_term_foreground`, `os_term_set_foreground`, `os_term_mode`, `os_term_set_mode` (canonical, echo, signals, `VMIN`, `VTIME`); nothing for the window size, no `SIGWINCH` meaning, no read woken by a signal; measured by four witnesses (§4) | as named |
| POSIX | POSIX.1-2024, cite clauses | fetched from `pubs.opengroup.org/onlinepubs/9799919799/` (XCU chapter 2 and 23 utility pages) on 2026-10-11 | none |
| how the corpus was built | which clauses by design, which by accident | 283 of the 532 statements had a passing case before this lane (sh01–sh05 built the corpus by area: grammar, expansions, redirection, special built-ins); nothing covered aliases, `$'…'`, `umask`, `ulimit`, `type`, `hash`, `fc`, `jobs`, `fg`, `bg`, job control or `test`'s file primaries beyond `-e -f -d -s` | — |

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

## 3.8 The result against the prediction

| predicted | measured | verdict |
|---|---|---|
| 450–650 statements | 532 (+18 not counted) | held |
| 74% met (65–83%) | **75.9%** (400 of 527 testable) | held |
| 2.2–2.7, 2.9–2.10 above 90% | 2.6 99%, 2.7 100%, 2.9 91%, 2.10 100%, but **2.2 56%** (`$'…'`) and **2.3 44%** (aliases) | falsified for 2.2 and 2.3 |
| 2.11–2.15 between 60% and 80% | 2.12 60%, 2.13 73%; **2.11 20%**, **2.15 87%** | falsified for 2.11, 2.15 |
| the utility pages for `fc`, `jobs`, `fg`, `bg`, `kill`, `alias`, `unalias`, `type`, `umask`, `ulimit`, `hash` near 0% | 0% for `alias`, `type`, `umask`, `ulimit`, `fc`, `jobs`, `fg`, `bg`; `kill` and `hash` 50% | mostly held |
| `sh`'s page about 70% | 67% | held |
| under half covered before the census | 283 of 532, 53% | falsified (slightly over half) |
| more than 150 new cases, 60–120 pending | 471 new (110 pending) and 42 sessions (35 pending) | held |
| dash and bash disagree on 15–40 new cases | **96** (mostly message and listing formats); POSIX took bash's side in 24 | falsified |
| the five largest gaps: fork, missing built-ins, signals with no meaning, `$$`/`wait`, expansion corners | by scripts: **`test`'s file primaries (14)** — not predicted at all; `umask` (9); `trap 13` (7); a bracket with `/` (4); fork-shaped (3); `$*` in an assignment (3) | the largest gap was missed |
| 25–40 scripts, 35% same (15–60%) | 80 scripts, **62.5%** same | falsified (more pass) |
| no autoconf configure completes identically | none of the three autoconf configures did; zlib's hand-written one did | held |
| install-sh passes; config.guess passes or fails on a pipeline shape | both fail on `umask` | falsified |
| git's test library fails on `local` | it fails on `test -x` | right verdict, wrong cause |
| at least two hangs | **none** | falsified |
| startup within 3× of dash | pelt is as fast or faster (1.35 ms against 2.32, loaded; 0.34 against 0.36, native, quiet) | held |
| under 6 MB and flat after 10,000 typed commands | **33 MB and growing** (pipelines, `&&`, groups and substitutions keep 3–10 KB each) | falsified |
| fork-heavy 0.8–1.5× | 1.54× | falsified (just above) |
| pipeline-heavy 1.5–4× | 1.69× | held |
| expansion loop 5–20×, the worst, the time in allocation | **3.9×** release, 10.2× native; the worst; ~29% in the runtime's allocation, the rest pelt's interpreter | the ratio falsified on release, held on native; the cause held |
| configure-shaped 2–6× | **1.5×** | falsified |
| the order: the fork ruling first | the plan starts with pelt's own script walls (they break 4× the scripts fork does), then memory, then the small built-ins; the fork ruling sits with job control | changed by the measurement |

## 4. Evidence index

- **The prediction:** `4437c81`, pushed before any build or run.
- **The clause table:** `tests/census/clauses.tsv` (532 statements, 18
  more not counted), counted by `tools/clause-census` (a CI step on
  every host); per statement in `docs/CENSUS.md` §5. Source:
  `notes/sh06-evidence/*.census`, turned into cases by `gen.py`,
  pending tags by `pend.py`, sessions by `sess.py`.
- **The corpus and sessions at the head, on kasumi:**
  `logs/g1-*` and the final `g2` run: corpus **804/0/117** on both
  tiers and under `taskset -c 0-3`; `tools/oracle-record --check` 0
  drifted (the first `--check`, `logs/g1-oracle-check.log`, found one
  case recorded under load, `signal/c_wait_interrupted_term`, fixed in
  `a6af687`); sessions **92/0/35** on both tiers and under `taskset`
  (`logs/g1-sess-*`).
- **CI:** run 38162244145 red on two host-dependent cases (ubuntu's
  `/bin/sh` is dash: `simple/c_enoexec_binary`; macOS's `kill -s 15`:
  `kill/c_send`), fixed in `6e59043`; run 38163737691 green on all
  three jobs at `6e59043`.
- **The script set:** `notes/sh06-evidence/scripts/scripts.tsv` (80 rows:
  package, version, sha256, licence, exits, verdict) and
  `scripts-aided.tsv`; `constructs.md` (the three shells' answers);
  pins `tools/script-census.pins`; the static pelt `906c2a7a7ba7ca49…`
  built from `4437c81`; images `sh06-arch` `f24bfd32dfb4`,
  `sh06-debian` `419c2b42b659`, `sh06-alpine` `434f3bd249e0` on
  kasumi's lane-private store; logs `scripts/final-*.log`.
- **The sessions:** `tests/session/c_*` (42), recorded from `dash -i +m`,
  `dash -i -m` and `bash --posix -i`; `tools/interactive-census` →
  `logs/icensus-*.log`.
- **Memory:** `loopmem.sh` → `logs/loopmem-release.log`; `leak.py` →
  `logs/leak-release.log`, `logs/leak2-*.log` (dash flat, 0 B a line).
- **Speed:** `tools/bench/` → `scripts/speed.md`, `scripts/speed-*.txt`.
- **Witnesses for what wolf lacks:** `witness/term_keys`, `winch`,
  `stop_report`, `read_vs_signal` (driver `witness/drive.py`, output
  `witness/drive.log`), `witness/argv_bytes` (`argv_bytes.log`); built
  with the pinned wolf 0.2.27 on kasumi, linux 7.2.8.

## 5. Done-when

- Branch `sh06`, PR wolffe-lang/pelt#8, open and unmerged.
- No change under `src/`.
- `wolf/tools/lane-audit.sh pelt sh06 8` run from the org directory;
  its exit status is in the PR's last comment.
