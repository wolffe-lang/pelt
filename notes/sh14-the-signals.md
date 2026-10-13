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

### 3.9 The result against the prediction

Measured on kasumi (linux x86-64; dash 0.5.13.4 for the corpus, the
census images' own dash for the scripts), at `812cafc` (the head of
the code; what follows it is this file, the README, the plan and the
census document), and in CI on linux x86-64, macOS arm64 and linux
aarch64 (run 38349110222 at `812cafc`). **native** is `tools/build
--native` (`wolf build`), **release** `tools/build --release` (`wolf
build --release`); "both tiers" means both.

| prediction | predicted | measured | held? |
|---|---|---|---|
| 3.1 the pin builds with no source change | both tiers, `--deny-warnings` | both tiers, no change (`logs/pin.status`, at `4c16941`) | held |
| 3.1 at the bare pin | corpus 837/0/98 (8 PEND-ok), sessions 197/0/20, every gate as at trunk, census unchanged | **837/0/98 (8)** on native, release and both under `taskset -c 0-3`; **197/0/20** on native, release and release under `taskset`; every other gate 0; census unaided **76** | held |
| 3.2 `$$`, `PPID`: five corpus cases and one session leave pending | 5 + 1 | **5 + 1**, on linux and on macOS (CI) | held |
| 3.3 `trap`: eight cases leave pending; `c_trap_ignore_pipe`, the two interruptible-wait cases and `pending/subshell_signal` stay | 8 leave, 4 stay | **8 leave, 4 stay**; `c_trap_ignore_pipe` moved to the fork row | held |
| 3.3 an unnamed number or a non-POSIX name refused; faults recorded only | as said | as said (`probe/pelt/p2b.pelt` against `p2b.dash`) | held |
| 3.4 `kill`: four cases and `wait/c_job_id` leave pending | 5 | **5** | held |
| 3.4 statuses as dash's | 0, 1, 2 | as dash on every probed form but the ones named in `tests/diff/PENDING.md` (a signal POSIX does not name; a job id's number after an earlier job ended); **not predicted:** dash stops at the first operand that fails, and tries a `-word` as a signal before it reads it as options (`-stop` is `SIGSTOP`, `-sTERM` is `-s TERM`); pelt does both | held, with two things learned |
| 3.5 the barrier goes; 0 misses | 2,000 rounds, 0 misses on four cpus and on one | the witness asks 5,000 times with a child as sender and 5,000 with the built-in: **0 misses** on native and release, on 16 cpus, four and one (`logs/head-sigw-*.log`, `logs/gauntlet-totals.txt`), and on linux and macOS in CI. Seen red: trunk on 0.2.28 with the barrier's call removed misses **3 to 12 of 5,000** on four cpus and sixteen (`logs/red-barrier.log`) | held |
| 3.5 `settle_hup` goes | — | gone; `tools/edit-witness`'s `hup` row still ends by the signal (status −1) with the modes restored, both tiers, also under `taskset -c 0-3` and `-c 0` | held |
| 3.5 the editor's timed read stays | — | stays | held |
| 3.6 corpus | (855 + new)/0/80 | **880/0/80** on both tiers and under `taskset -c 0-3` (25 new cases; 18 left pending) | held |
| 3.6 sessions | 198/0/19 plus new | **201/0/19** (three new cases) on both tiers and under `taskset` | held |
| 3.6 statements | 449 of 545 | **450 of 545 (83.3%)** | **off by one**: 2.12/5 ("signals for every name can be trapped") is met too. Its one failing case, `c_trap_ignore_pipe`, fails for want of a fork, so it moved to 2.9.2/9 (a producer written in the shell meets `SIGPIPE` or `EPIPE`), which was and stays pending; `signal/trap_ignore_pipe_fifo` shows `trap '' PIPE` in the shell's own process |
| 3.6 scripts, unaided | 76 | **75 printed at the head, 75 at trunk today, 76 at the bare pin**: the head's table and trunk's are the same verdict for verdict (`scripts/base-unaided.tsv`, `head-unaided.tsv`), and both are sh13's 76 but for `configure-sed`, whose one differing line is a coin (below) | held in substance (no script moved; the count is no lower than trunk's taken the same day), **missed as printed** (75, not 76) |
| 3.6 scripts, aided | 76 | **76** at trunk and at the head, verdict for verdict | held |
| 3.7 speed, head against the pin | no row above 2% (user instructions) | user instructions, head against the pin (`bench/instructions.txt`, three runs each, identical to five digits): release param −0.6%, fork −0.0%, pipeline −0.1%, configure-shaped +0.3%; native param +0.1%, fork +0.1%, pipeline −1.5%, configure-shaped +1.0%. Wall time under `taskset -c 0-3`, medians of 9: every row within 1.3% of the pin but native configure-shaped, +2.5% (0.393 s → 0.403 s) | held on instructions; one native wall-time row is over by half a point |
| 3.8 lupin | `unsupported` at `env_vars` | `lupin run --json src/pelt.lu`: `unsupported` at resolve, as predicted, but the name it gives is now `os_signal_default` ("this machine admits no `unsafe` and std has no `sigaction`"): with `std.signal` imported, the disposition builtins lupin refuses by ruling are met before `env_vars` (`lupin/pelt.txt`). So wolf-interp#240 is not the only thing between lupin and pelt | **held in kind, the name missed** |
| 3.8 the checked machine | an `unsupported` or a budget | `wolf conform-run --json --checked src/pelt.lu`: `unsupported`, "home-module method calls in checked execution", `phase_reached mem`; the same at trunk on 0.2.28 (`lupin/pelt.txt`) | held |

**Not predicted.**

- **A shell started with `SIGCHLD` ignored answered 1 for every
  command** (trunk too): the host takes the children's statuses and
  `os_wait_status` answers `io`. dash puts `SIGCHLD` back to its
  default when it starts, and so does pelt now (`sig_start`); and `trap
  '' CHLD` is recorded without ignoring the signal, as dash
  (`probe/p9`, `probe/chld.py`; `tools/signal-witness`'s `chld` row,
  seen red first).
- **With `SIGPIPE` ignored, a built-in's failed write was silent**
  (status 0). It is the command's error now (status 1), on the fast
  path too; a failed write for any other reason (a full disk) is still
  not reported by the ordinary path, which buffers.
- **dash serves every waiting trap before a `break` in one of them
  takes effect**, and runs a second signal's action inside the first's
  when it comes there (`signal/trap_break_keeps_pending`,
  `signal/trap_nested`); pelt did neither before.
- **`configure-sed` is a coin**: its third line prints a filesystem
  timestamp resolution it measures by how fast the shell runs between
  two file writes (`checking the filesystem timestamp resolution... 0.2` under dash, `0.1` under pelt in 3 of 23 census runs: trunk 1 of 8, the bare pin 1 of 7, the head 1 of 8; `scripts/sed-repeat.txt`. The same check run alone 300 times a shell (`scripts/ts.sh`, `ts-run.txt`) sees the second file newer at the first look in 34 and 35 of 300 runs under dash and in 62 and 71 (trunk), 70 (pin), 51 and 73 (head) under pelt: a shell that is slower between the two writes crosses the filesystem's clock tick more often, dash crosses it too, and the three pelts cannot be told apart. `tools/script-census` calls a script unstable only when dash disagrees with dash in the same run, which a one-in-nine coin rarely shows).
- The corpus harness reset eight signals to their defaults; with every
  signal trappable and the ignored-at-start rule in, it resets all of
  them (the oracle re-checked: 0 drifted).

**Seen red.** (1) `tools/signal-witness` on trunk with the barrier's
call removed, wolf 0.2.28: 3 to 12 misses of 5,000
(`logs/red-barrier.log`). (2) The `ignored` rows on the build before
the rule (`logs/ignored-red.txt`). (3) The `chld` row on the build
before `sig_start` (`logs/chld-red.txt`). (4) In CI, branch
`sh14-plant` (`0b108ec`: the set ignored at start unread, `kill -s`
unused), run 38349137192: the witness's `ignored` and `ignored-i` rows
fail on both tiers on linux (the shell dies of signal 10) and macOS
(signal 30), and eight corpus cases fail on each host
(`kill/c_send`, `forms`, `job_ids`, `self`, `status_names`, `targets`,
`signal/c_ignored_on_entry`, `ignored_at_start`): 872/8/80
(`logs/plant-38349137192.txt`).

## 4. Evidence index

- **The prediction:** `75c08f3`, before the pin (`4c16941`) and the
  first `src/` change (`bcec4eb`).
- **The probes:** `notes/sh14-evidence/probe/` — `p1`–`p9` under dash
  (`.dash`) and under pelt at the head (`pelt/`), `chld.py`.
- **The five builtins on four machines:** `notes/sh14-evidence/wolf/sig/`.
- **pelt on the checked machine and lupin:** `notes/sh14-evidence/lupin/pelt.txt`.
- **The gauntlets:** `notes/sh14-evidence/logs/` — `base.status`
  (trunk `1315587`, wolf 0.2.28), `pin.status` (`4c16941`),
  `head.status` (`812cafc`): fmt, both builds, `wolf test`, the clause
  census, the width table, difftest on both tiers and both under
  `taskset -c 0-3`, the planted difftest red, sessions on both tiers
  and under `taskset`, the planted session red, glob-rss, loop-rss,
  shape-rss, exec-witness, edit-witness, hist-witness on both tiers,
  signal-witness on both tiers and both under `taskset` (head),
  `oracle-record --check` (0 drifted), the static build; every exit
  status 0. The totals are in `gauntlet-totals.txt`; the head's
  session transcripts checked against the oracle
  (`head-session-record-check.log`).
- **The census:** `notes/sh14-evidence/scripts/` — `base-*`, `pin-unaided.*`,
  `head-*` (`.tsv`, `.log`, `.bin`), `sed-repeat.txt`.
- **The bench:** `notes/sh14-evidence/bench/`.
- **The system calls:** `notes/sh14-evidence/sysc/` (pin and head).
- **Seen red:** `logs/red-barrier.log`, `logs/ignored-red.txt`,
  `logs/chld-red.txt`, `logs/plant-38349137192.txt`.
- **CI:** PR wolffe-lang/pelt#26; run 38349110222 green at `812cafc`
  on three hosts (linux x86-64 and macOS arm64: corpus 880/0/80,
  sessions 201/0/19, the witnesses; linux aarch64: both tiers still
  refused by name); the plant, run 38349137192, red as said above.

## 5. Done-when

- Branch `sh14`, PR #26 open and unmerged, CI green at the head;
  `wolf/tools/lane-audit.sh pelt sh14 26` run from the org directory,
  its exit status read directly.
- pelt issues: none of #10–#20 is closed by this branch (§2). The
  census rows it clears were routed to wolf-lang issues that s232
  closed (#141, #679, #681, #691, #423).

## 6. What waits on what

**On job control** (wolf-lang#680 and the lane after it: a child wait
a signal can cut short, a stopped child's report, a signal to a
process group):
- `wait` cut short by a trapped signal (`pending/wait_interrupted`,
  `signal/c_wait_interrupted_term`);
- `kill 0`, `kill -- -N` (refused by name, status 1);
- `jobs`, `fg`, `bg`, Ctrl-Z, job numbers that are given back when a
  job ends, `%name` (pelt#18 is `jobs` in a script).

**On the terminal builtins** (s234, wolf-lang trunk, not in 0.2.29):
- the editor's read that times out every tenth of a second to poll for
  `SIGHUP` and `SIGINT` (`os_signal_wait_fd`);
- a redraw on `SIGWINCH` and the window's size (`os_term_size`); pelt
  can TRAP `WINCH` since this lane, the editor does not use it;
- the terminal's own special characters (`os_term_chars`).

**On a fork** (ruling #69 R1): a signal to "the subshell"
(`pending/subshell_signal`), a subshell's own trap for a signal sent
to `$$`, `signal/c_trap_ignore_pipe`.

**For PAX** (`notes/sh14-evidence/sysc/`: `tools/syscall-census` on
the static build, the pin and the head over the head's corpus, 46
distinct calls each). New at the head: `getppid` (once a shell) and
`kill` (the built-in; `os_signal_send`). Gone: `tgkill` and `gettid`
(the barrier's raise). Many more `rt_sigaction` (5,893 → 18,698 over
the corpus): one at every start (`SIGCHLD` to its default) and twenty
that only ASK (a null new action: the set ignored at start) the first
time a shell runs a subshell, sets a trap or starts an asynchronous
list. A kernel that answers `rt_sigaction` with no new action wrongly
would make pelt think signals are, or are not, ignored at start.

## 7. Wolf findings (not filed; texts for the orchestrator)

1. **A program started with `SIGCHLD` ignored cannot learn how any
   child ended**, and nothing says so at the call: `os_wait_status`
   answers `io` for every child (`[os.signal.disp]` states it for a
   program that ignores `CHILD` itself; the inherited case is the same
   and is not the program's doing). pelt's witness:
   `tools/signal-witness`'s `chld` row; before `sig_start` every `$?`
   was 1. A runtime that reset `SIGCHLD` at its first spawn, or a
   sentence in `[os.proc.status]`, would have saved the search.
2. **`[os.signal.disp]` still says "a bit outside the nine meanings is
   `io`"** at v0.2.29, beside `[os.signal.set]`'s twenty: a stale
   count.
3. **No meaning for a signal POSIX does not name**, so `kill -s IO`,
   `kill -PWR`, `kill -34` and `trap … 16` cannot be written in wolf
   (ruling #70 R1 took exactly POSIX's set). dash takes them. Not a
   defect; the edge of the ruling, met by a shell.
4. **`os_signal_send` reaches one process** (R6): a shell's `kill 0`
   and `kill -- -pgid` wait on the job-control lane.
5. **The checked machine refuses pelt** with "home-module method calls
   in checked execution" (the `Map` methods that resolve into
   `std.map`), at 0.2.28 and 0.2.29 alike: pelt has never run there.
6. **While a wolf program starts a child, its signal mask is full**
   (`SigBlk: fffffffffffbfeff` read from `/proc` by the child of a
   pelt pinned to one cpu). It is the spawn's own window and closes
   again; noted because a witness that reads a parent's mask from a
   child sees it.

## 8. Not verified, and inferred

- **macOS** by CI only (no build on nomad-1): the corpus, the sessions
  and the witnesses are green there; the probes `p1`–`p9` were not run
  there, and the census scripts are linux-only.
- **linux aarch64**: no tier builds (asserted in CI).
- **The checked machine and lupin run no pelt**; the five builtins
  were measured on all four machines by one small program, not
  through pelt.
- **`kill/job_ids` takes bash as its oracle** (the corpus's rule for
  where POSIX and dash part): dash 0.5.13.4 answers "no such process"
  to every `kill %n` in a script. pelt signals the job, as XCU `kill`
  says and bash does.
- **Inferred, not measured:** that dash tries a `-word` as a signal
  first is read from four forms (`-stop`, `-segv`, `-sys`, `-sTERM`);
  that dash stops at the first failing operand, from two.
- **The order of two actions that both leave** (`break` in one,
  `return` in another, waiting together): pelt keeps the later; dash
  was not asked.
- **A trap for `TSTP`, `TTIN`, `TTOU`** is caught when a child sends
  the signal (`signal/trap_every`); what the terminal's own Ctrl-Z
  does to a pelt with such a trap was not typed.
- **`kill` of a pid that is one of the shell's own reaped children**
  answers "no such process" without asking the host (the id may be
  another process's by then); a host that reuses ids faster than a
  script loops was not constructed.
- The `unsupported` rows of `os_ppid`, `os_signal_number` and
  `os_signal_send` (windows): no machine pelt runs on answers them.
