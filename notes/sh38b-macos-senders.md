# sh38b — the hangup witness on macOS: who sent a signal

Base: pelt trunk `45c4de11` (the merge of #120; wolf 0.2.36, lupin 0.1.58, std `78b9d3cb`). Clean room: no
shell's or kernel's source. bash ran only as a black box; the kernels were asked with two small C programs that
signal only their own children, by pid.

## 0. The red, and the prediction

Trunk `45c4de11`'s push run 43348013450, job `gauntlet (macos-latest, true, native)`, step `tools/signal-witness`:
`hangup-witness: 22 of 39 rows hold, 17 fail, 7 skipped` (the seven are the `-close` rows, linux's by design). The
linux legs were green. #120's record was linux only, and its pull-request run had no macOS leg. The Mac here
(macOS 26.4.1, arm64) gives the same 17 at the same head (§3). They are of three kinds:

- 14 rows where a stopped job's CONT, and in `stopped` and `mixed` its TERM too, is named `kernel0` (sender 0,
  si_code 0) where linux names the shell: `stopped`, `mixed`, `disown-h-stopped`, `exit-stopped`,
  `exit-stopped-bg`, `eof-stopped`, and the eight `kill-*` rows that end a stopped job (`kill-stopped`, `-hup`,
  `-term`, `-s-term`, `kill-bg-stopped`, `-group`, `-pipe`, `-two`);
- 3 rows where a HUP linux names the kernel's is named the shell's: `disown-stopped`, `disown-all` (the stopped
  job taken out of the table) and `script` (a script's jobs);
- `eof-stopped`'s status, 146 where linux's is 148: 128 + SIGTSTP, which is 18 on macOS and 20 on linux.

**Prediction.** Either (a) macOS does not tell the witness who sent a signal the way linux does, and the rows must
hold there what macOS does tell; or (b) pelt on macOS does not send the CONT and TERM itself and something else
does, a pelt fault. If (a): a program that sends every signal itself sees the same `0` senders on macOS and its own
pid on linux, and bash on the same Mac shows the same senders as pelt. If (b): bash on the Mac names the shell
where pelt shows `kernel0`. Before measuring, (a) is the likelier: only a shell sends TERM to its stopped jobs as it
ends (the kernel never does), and pelt's `stopped` probes received a TERM named `kernel0`.

## 1. Which it is: (a), measured

**A sender that is known.** `notes/sh38b/sigattr.c` forks a child and sends it signals itself, by the child's pid:
to a running child and to a stopped one (stopped by itself or by the parent's SIGSTOP), back to back or 50 ms
apart, three takes. The child's handlers record si_code and si_pid.

- Linux (7.2.4, the Ubuntu 24.04 image): every one of 123 signals names the parent, si_code 0 (SI_USER).
- macOS 26.4.1: 81 of 123 name the parent and 42 name 0, every si_code is 0 (macOS's SI_USER is 0x10001, so 0
  is no code at all). The pattern is the same in every take: a signal sent alone names the parent; of signals
  pending together, one names it and the rest 0. A running child sent HUP, CONT and TERM back to back reads
  `CONT:0 TERM:0 HUP:parent`; 50 ms apart, all three name the parent. A stopped child sent HUP then CONT reads
  `CONT:0 HUP:parent`; sent USR1 then CONT, `USR1:0 CONT:parent`. The sender is one slot per process, not one
  per signal.

**A signal the kernel makes.** `notes/sh38b/orphan.c`: P starts C in a group of its own, C stops itself, and P
exits (or G kills P with SIGKILL). C's group is orphaned with a stopped member, so the kernel sends it SIGHUP and
SIGCONT (POSIX `_exit()`). Nobody calls kill(2) on C.

- Linux: `HUP:0/code=0x80 CONT:0/code=0x80` (SI_KERNEL), 6 of 6.
- macOS: `HUP:P(exited)/code=0x0 CONT:0/code=0x0`, 6 of 6, also when P died of SIGKILL and so sent nothing. A
  signal the kernel makes as a process exits names that process.

**bash 5.3.20 on the same Mac** (`tools/hangup-witness --measure bash`, `notes/sh38b/bash-5.3.20-macos.table`):
every one of the 17 rows reads as pelt's does, `kernel0` and `shell` in the same places, and bash sends CONT and
TERM to its stopped jobs (linux names bash for them, `notes/sh38/bash-5.2.21.table`). Without senders, bash's macOS
table equals `tests/hangup/expected` on 35 of the 39 rows the Mac runs, and the four that differ are the table's
four decisions (`trap`, `ignored`, `exit-stopped`, `exit-stopped-bg`), each as it differs on linux.

**pelt's own rows.** In `kill-stopped` the shell lives, the harness sends nothing, and the job's group is not
orphaned (its parent, the shell, is in the session), so nobody but pelt can continue the job; the probe received
CONT, named `kernel0`.

So it is (a). pelt sends what it sends on linux; macOS's siginfo does not say so.

**What macOS promises.** sigaction(2) on this Mac: "The code argument of the BSD-style handler and the si_code
member of the info argument to a SA_SIGINFO handler contain a numeric code explaining the cause of the signal,
usually one of the SI_... values from <sys/signal.h> or codes specific to a signal". `<sys/signal.h>` (the SDK's)
comments si_pid as "sending process" and promises it only for SIGCHLD: "If the signal is SIGCHLD, the si_pid field
will contain the child process ID". POSIX.1-2024 (XSH 2.4.3 and `<signal.h>`) sets si_pid and si_uid when si_code
is SI_USER or SI_QUEUE; macOS gives 0. Nothing in the documents promises the sender of a signal sent with kill(2),
and the measurement shows neither reading can be trusted there: 0 may be the shell (the slot went to another
signal), and the shell's pid may be the kernel's (a hangup made as the shell exited).

## 2. The change

- `tools/hangup-witness` asks the host first (`senders`): a child stops itself, and the witness's helper sends it
  SIGHUP and SIGTERM, which both wait while it is stopped, then SIGCONT, by its pid. Where each names the sender
  (linux), the rows hold every sender, the table's lines as written. Where not (macOS: `HUP from parent (si_code
  0), TERM from 0 (si_code 0), CONT from 0 (si_code 0)`), the rows hold each probe's signals by name, each once,
  how it ended (`dead:SIG`: the first signal that ended it), and how the shell ended, and not who sent them; a
  failing row prints what it saw with the senders too. On linux a host that does not name each sender fails the
  witness, so the linux rows never lose their senders.
- A status past 128 that names a signal is spelled `exit:128+SIG` (the number is the host's), and
  `tests/hangup/expected`'s `eof-stopped` reads `exit:128+TSTP`: on linux exactly the 148 it held.

Every other line of `tests/hangup/expected` is unchanged, and on linux each is held as before.

**What the macOS rows hold, and what they cannot.** They hold which signals each job received, which one ended
it, and the shell's end. In the `kill-*` rows that is enough to hold that pelt continues a stopped job: nobody
else does there, and a pelt that does not leaves the probe stopped with TERM pending (the plant, §3). They cannot
tell, in the hangup rows, a stopped job's CONT and HUP from pelt from the ones the kernel sends an orphaned
stopped group as the shell dies (`orphan.c`), nor, in `script` and `disown-*`, whether a HUP was the shell's or
the kernel's. Those senders are linux's rows to hold, where each is named.

## 3. Evidence index

The measurements, in `notes/sh38b/` (sha256):

- `sigattr.c` `4b36c126…`, its outputs `sigattr-macos.txt` `cab5c88e…` and `sigattr-linux.txt` `e1545736…`
  (the same source compiled on each: macOS 26.4.1 here; linux 7.2.4 in the Ubuntu 24.04 image).
- `orphan.c` `c55cfb9b…`, `orphan-macos.txt` `8658b355…`, `orphan-linux.txt` `b9d9f707…`.
- `bash-5.3.20-macos.table` `d4f4785b…`: bash on the Mac through the changed witness, with its `senders` line; a
  first take through trunk's witness was identical row for row (`eof-stopped`'s 146 then spelled as a number).
- `pelt-45c4de11-macos-red.txt` `1fe87d48…`: trunk's pelt and witness on the Mac, the hosted run's 17 FAIL rows,
  the same lines.

Before committing, the changed witness held every row on the Mac (39 of 39, 7 skipped) and on linux in the
Ubuntu 24.04 image (46 of 46, with `senders: each named (HUP from parent (si_code 0), TERM from parent (si_code
0), CONT from parent (si_code 0))`), against trunk's pelt. The gauntlet records at the head (the Mac's and
linux's) and the plant's are cited in the pull request's evidence index.

## Forbidden

- Read no shell's source and no kernel's: bash, dash and both kernels were asked from outside.
- Signal only pids this lane started, never a group; nothing in /tmp on any host.
- Weaken no linux row: the table's lines are held as written on linux, `eof-stopped` respelled, not changed.
- Touch nothing of pelt#123 (the prompt's back-off, another lane).

## Inputs verified

- The red: run 43348013450, job 131640341472's log, read once (17 FAIL lines, the summary line above).
- sigaction(2) and the SDK's `<sys/signal.h>` on the Mac (macOS 26.4.1, 25E253), quoted above.
- bash: Homebrew's 5.3.20 on the Mac (`GNU bash, version 5.3.20(1)-release (aarch64-apple-darwin25.6.0)`).
- Linux: the Ubuntu 24.04 image #120's records ran in, kernel 7.2.4.

## Done-when

- The Mac's witness holds every row at the head, and linux's holds every row with its senders.
- The plant, one hunk off the head, is red by name on the Mac.
- The hosted macOS leg of `tier full` is green at the head (the merge's to see; this lane does not wait on CI).
