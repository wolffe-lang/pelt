# sh14 — the signals (and the pin to 0.2.29)

Contract: `sprints/pelt/14-the-signals/sh14-the-signals.md` in the
planning repo (`a35b2fe`). This file is the lane's record: §1 to §3 are
committed before the first change under `src/`, `tools/`, `tests/` or
to the pin, and the evidence index (§4) is filled in as the work lands.

## 1. Forbidden

As the contract's §1. No shell's source is read or searched for (dash,
bash, zsh, busybox, mksh, any other), nor a libc's or a kernel's
(rulings #42–#45): POSIX.1-2024, man pages as documentation, and
black-box runs of dash 0.5.13.4 only. A signal's meaning is named
(`std.signal`'s functions); no literal signal bit and no host signal
number is written in pelt's source, and `os_signal_number` is the only
way to a host number. The terminal builtins of s234 (`os_term_size`,
`os_signal_wait_fd`, `os_term_chars`) are on wolf-lang trunk only, not
in 0.2.29, and are not reached for. No census regression: sessions,
statements and the real-script count are re-taken and are no lower.
The toolchain from the release archives by digest, each digest read
twice. No merge, no tag, no issue filed or closed (listed in the
report), no package installed, no other lane's CI run cancelled,
nothing under `~/.claude`; no attribution trailers. No build on
nomad-1: kasumi, under `~/lanes/sh14/` (one target directory per
tree, pruned), detached jobs by `setsid` with the pid recorded and
stopped by that pid only, never by name, pattern or group. A signal in
a test goes only to a process the test started. Scratch under
`~/lanes/sh14/` (`TMPDIR` points there), never `/tmp`. Strict evidence
(#571): `wolf build` exit 2 is a compile error; SigBlk and SigIgn are
read before a signal row is called red; signal and process tests also
run under `taskset -c 0-3`. If the harness refuses an action, the lane
stops and reports.

## 2. Inputs, verified (2026-10-13, re-derived before any change)

| input | contract says | measured | drift |
|---|---|---|---|
| pelt trunk | `1315587` or later | `origin/trunk` = `13155878ce37…`; branch `sh14` cut from it; no open PR | none |
| wolf 0.2.29 | tag `v0.2.29` at `6ffe7c60` | tag → `6ffe7c6056eeb8c661b37e38d99b91166e8c1add`; release 411040788, not a draft, 4 assets; `wolf 0.2.29 (wolfgang, pin 6ffe7c6)`, "paired with lupin 0.1.52 (reference interpreter), pin 294d626" | none |
| lupin 0.1.52 | tag `v0.1.52` at `025428b` | tag → `025428b725a35bfbc53745d4166817ff3053c0fd`; release 410845419, not a draft, 5 assets; `lupin 0.1.52 (wolf-interp, reference interpreter at pin 294d626)` | none |
| the digests | by digest, each read twice | read twice from the release API, both reads equal, and equal to `sprints/release/r34-evidence.md`; the three wolf and three lupin archives pelt pins fetched on kasumi and `sha256sum -c` run twice, 12 of 12 OK (`notes/sh14-evidence/logs/fetch6.log`) | none |
| the bundled std | the bundled std in 0.2.29 does not have `signal.send`, `signal.number`, `signal.ignored`, `env.pid`, `env.ppid` | the linux x86-64 archive's `std/STD-REV` is `d7c2968cbba1…`; its `std.signal` names nine meanings | none |
| wolf-std trunk | `9e5bd6b` has them | `origin/trunk` = `9e5bd6b16beeab1708a95c75d43b9926dd95f31e` (sc60, pinned to 0.2.29 / 0.1.52): `std.signal` names the twenty listenable meanings and the eight send-only as functions, with `send`, `number`, `ignored`; `std.env` has `pid`, `ppid` | none |
| whether pelt consumes wolf-std | "if so" | it does: `[std]` in `wolf-toolchain.toml` stages a tree at a commit (PAX builds pelt from that rev), and `Map.keys`/`Map.has` resolve into it; no module is imported by name today | — |
| the spec | `[os.signal.set]`, `[os.signal.set.stable]`, `[os.signal.number]`, the process clauses, at `v0.2.29` | read at the tag (`spec/11-os.md` §1, `[os.proc.self]`): twenty listenable meanings, eight send-only, one shape rule, `os_signal_ignored`, a poll that does not trail a delivery, `os_pid`, `os_ppid`, `os_signal_send` (one pid above 0; groups are job control's), `os_signal_number`. The stability clause's parenthetical ("the prelude declares no constant for any meaning") holds: the names a program has are `std.signal`'s | none |
| the five builtins, measured | — | `notes/sh14-evidence/wolf/sig/`: one program on the published archives. **checked** (`wolf conform-run --json --checked`), **native** (`--native`) and **release** (`--release`) answer the same: the 28 numbers (linux: `USR1=10 … SYS=31`), `number(0)` `invalid`, `send(0, …)` `invalid`, a pid no process has `not_found`, pid 1 `denied`, and a send of each of 17 listenable meanings to the program's own pid seen by the very next poll in 3,400 of 3,400. **lupin** (`lupin run --json`) answers `unsupported` at resolve, by name, on `os_signal_ignored` | — |
| the checked machine and `<<` | wolf-lang#736 | open; pelt writes no shift | — |
| lupin and pelt | wolf-interp#240 | open | — |
| the corpus at trunk | (index) 835/0/99 at sh13 | **837/0/98**, 8 of the pending passing (PEND-ok), on native, release and both under `taskset -c 0-3` (kasumi `~/lanes/sh14/logs/base-diff-*.log`): sh12 and sh08 landed since | reported |
| the sessions | (index) 171/0/26 at sh13 | **197/0/20**, 4 PEND-ok (native; release and `taskset` in the baseline commit) | reported |
| the clause table | (index) 431 of 544 | **439 met of 545** (81.3%), 99 pending, 2 gaps, 5 untestable | reported |
| the script census | (index) 76 of 80 | re-taken in the baseline commit (the images are rebuilt from the pinned Containerfiles: sh13's store is gone) | — |
| pelt#10–#21 | which of them this closes | open: #10–#18, #20; closed: #19, #21. None is about `kill`, `$$`, `PPID` or a signal's meaning: sh06's census rows for those were routed to wolf-lang#141, #679, #681 (all closed by s232) and live in `tests/diff/PENDING.md`. #18 (P12, `jobs` in a script) and #17 (P10, `trap -p`, `$(trap)`) touch this lane's area and are not its items | reported |
| sh07's "trap by number recorded" (P15) | — | `trap_name` takes 0–6, 8, 9, 11, 13–15 by number from a table of literals and records them; only `HUP INT QUIT TERM USR2` are caught | — |
| sh11's signal handling | — | the editor listens for `HUP` while a line is edited and polls `HUP` and `INT` between reads that time out every 0.1 s; after a hangup it raises `HUP` at its default and sleeps up to 0.5 s for the death (`settle_hup`) | — |
| wolf-lang#680 | — | open: no child wait a signal can cut short | — |
| what dash does | black-box | `notes/sh14-evidence/probe/p1`–`p7` (`.sh` and `.dash`): `kill -l` and its operand, every `kill` form and status, `trap` names and numbers, each signal trapped, ignored and at its default, the order of pending traps, `$$` and `PPID`, a signal ignored at start, job ids | — |

## 3. Prediction (committed before the first change)

Written from the spec at the tag, the probes above and the pending
lists; nothing of pelt has been built at 0.2.29.

### 3.1 The pin (its own commit)

wolf 0.2.29 / lupin 0.1.52 by the six digests; std at wolf-std
`9e5bd6b`, **not** the commit the archive bundles (`d7c2968`), because
that is the first std whose `std.signal` names every meaning, and the
rule is that pelt writes no bit. pelt builds on both tiers with
`--deny-warnings` and no source change (no declaration of the five new
prelude names; r34 grepped pelt for them). Every binary's bytes move.
At the bare pin: corpus **837/0/98** with the same 8 PEND-ok, sessions
**197/0/20**, every other gate as at trunk, the script census
unchanged. The barrier is still in the source there and still works
(its meaning, `BG_READ`, is listenable).

### 3.2 `$$` and `$PPID`

`$$` is `os_pid()`; `PPID` is a variable set once at start from
`os_ppid()` (as dash: assignable, not exported, not taken from the
environment). Subshells keep both (they run in-process). Leaving
pending: `pending/pid`, `pending/exec_pid`, `param/c_pid_is_real`,
`param/c_pid_subshell` (they pass on linux today through `/proc`; the
claim is that they pass on macOS in CI too), `env/c_ppid`, and the
session `c_jc_shell_is_leader`.

### 3.3 `trap`

A condition is any of the twenty meanings wolf can hear, by POSIX name
(any case, no `SIG` prefix, as dash) or by the host's number
(`os_signal_number`); the eight wolf can only send (`KILL`, `STOP`, the
six faults) are recorded and listed and never caught, which is what
dash does with `KILL` and `STOP` and differs for the faults. A number
or name wolf has no meaning for (linux's 16, `IO`, `PWR`, the
real-time signals) is refused where dash takes it. `trap` prints in the
order of the signals' numbers, as dash. Pending traps run in the order
of their numbers. A signal ignored when the shell started is recorded
and listed and stays ignored, trapped or reset, in an interactive
shell too (dash, probed). A subshell resets caught traps and keeps
ignored ones; a program started or `exec`ed starts with caught signals
at their default and ignored ones ignored.

Leaving pending: `pending/trap_usr1`, `pending/trap_ignore_usr1`,
`signal/c_trap_abrt_number`, `signal/c_trap_alrm`,
`signal/c_trap_pipe`, `signal/c_trap_usr1_self`,
`signal/c_trap_winch_cont`, `signal/c_ignored_on_entry`.
**Staying pending:** `signal/c_trap_ignore_pipe` (its writer is a brace
group in a pipeline, which pelt runs to its end before the reader
starts: no fork, not a missing meaning; it moves to the fork row),
`pending/wait_interrupted` and `signal/c_wait_interrupted_term`
(wolf-lang#680), `pending/subshell_signal` (fork).

### 3.4 `kill`

A regular built-in: `kill pid…`, `-s name`, `-s number`, `-name`,
`-number`, `-0`, `--`, `-l`, `-l number`, `-l status`; statuses as
dash's (0; 1 when a process could not be signalled; 2 for a usage
error, an unknown signal or an operand that is not a number). Job ids
(`%1`, `%%`, `%+`, `%-`) name pelt's own `&` jobs, each one process;
`kill` and `wait` take them. A pid of 0 or below (a process group) is
refused by name as waiting on job control (`os_signal_send` takes one
pid above 0). `kill -l` prints the 28 names wolf has, by number.
Leaving pending: `kill/c_bad`, `kill/c_job_id`, `kill/c_list`,
`kill/c_send`, `wait/c_job_id`.

### 3.5 The barrier and the timed polls

`settle` (raise `BG_READ` on itself and wait for it after every reap)
goes, with its state field and its listen: `[os.signal.poll]`'s
guarantee is that a signal delivered or pending before the poll is on
the queue. The test that says so: every trap case in the corpus under
`taskset -c 0-3` (sh05 found the race there: seven cases failed on
four cpus without the barrier), plus a new witness that sends a signal
to a shell while its child runs and asks for the trap 2,000 times,
**0 misses** on both tiers pinned to four cpus and to one. `settle_hup`
(sleeping up to half a second after raising `HUP` at its default) goes:
`os_signal_raise` now delivers before it returns. **Staying:** the
editor's read that times out every 0.1 s to poll for `HUP` and `INT`;
only a read a signal can interrupt retires it (s234's
`os_signal_wait_fd`, not in 0.2.29).

### 3.6 The numbers

| | at trunk | predicted at the head |
|---|---|---|
| corpus | 837/0/98 | **(855 + new)/0/80**: the 18 cases named above leave pending; falsified if fewer than 16 or more than 19 leave |
| sessions | 197/0/20 | **198/0/19** (`c_jc_shell_is_leader`), plus any new case |
| statements met | 439 of 545 | **449 of 545** (82.4%): 2.5.2/12, 2.5.2/13, 2.5.3/8, 2.11/1, trap/13, wait/6, kill/1, kill/2, kill/4, kill/5. 2.12/5 stays pending on `c_trap_ignore_pipe` alone |
| real scripts as under dash, unaided | 76 of 80 (sh13) | **76**: the three that differ need a process per pipeline stage and pfetch is unstable; no script in the set stops at `kill`, `$$`, `PPID` or an uncaught signal |
| real scripts, aided | 76 | **76** |

### 3.7 Speed and size (`tools/bench`)

The state gains one `int` (the set ignored at start) and loses one
`bool` (the barrier's flag). Head against the bare pin, user
instructions: no row moves by more than 2%. A shell with no trap set
makes no signal call it did not make before; one with a trap set makes
one poll after a command where it made up to five and, after a reap, no
raise and wait.

### 3.8 The machines

pelt is built and measured on **native** (`wolf build`) and **release**
(`wolf build --release`). The **checked** machine (`wolf conform-run
--json --checked src/pelt.lu`) and **lupin** are asked once each and
their answers recorded; predicted: lupin still `unsupported` at
`env_vars` (wolf-interp#240), and now would stop at `os_signal_ignored`
besides; the checked machine does not run pelt to a prompt (an
`unsupported` or a budget, to be named from the record).
