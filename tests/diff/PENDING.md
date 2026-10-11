# Pending differential cases

Every case here has its expectation recorded from dash like any other,
RUNS on every `tools/difftest` pass, and is reported as `PEND-ok` or
`PEND-fail`; it does not decide the exit status. `tools/difftest` fails
any case marked `pending=` in its `.meta` that is not named below, so
nothing is skipped silently. A case leaves this list in the commit that
makes it pass.

| primitive pelt waits on | where it comes from | cases |
|---|---|---|
| **getpid** — `$$` on every host | wolf-lang#141 (pelt reads `/proc/self/stat` on linux; macOS has no `/proc`). `pending/exec_pid` compares `$$` before and after `exec`; the pid itself is measured on every host by `tools/exec-witness` | `pending/pid`, `pending/exec_pid` |
| **a meaning for every signal** — catching or ignoring `USR1`, `ALRM`, `PIPE` and the rest | wolf 0.2.27's signal surface is by meaning (`[os.signal.set]`): `HUP`, `INT`, `QUIT`, `TERM`, `USR2`, the job-control stops and `CHLD`, and no other. `trap` records and prints any condition, but one with no meaning keeps its default: the shell dies where dash runs the action (wolf-lang#679, and #423 for `PIPE`) | `pending/trap_usr1`, `pending/trap_ignore_usr1` |
| **an interruptible wait** — `wait` cut short by a trapped signal | `os_wait_status` blocks until the child ends and nothing waits for "a child or a signal" (`[os.term.note]` leaves stop reporting and the rest to the next job-control lane): the action runs after the jobs end and `wait` answers 0, where dash runs it at once and answers 128+N (wolf-lang#680) | `pending/wait_interrupted` |
| **fork** — a process for a subshell | none planned: pelt runs `( … )` in-process, so a signal sent to "the subshell" (`$PPID` of its child) reaches the shell itself, whose trap then runs where dash's subshell would have died | `pending/subshell_signal` |
| **user database** — `~login` | no `getpwnam` surface in wolf 0.2.27; not filed until a lane needs it beyond this case | `tilde/user` |

**No case, named:**

- A signal that was ignored when a non-interactive shell started cannot
  be trapped or reset (XCU `trap`). wolf 0.2.27 cannot ask what a
  signal's disposition is, so pelt traps it anyway (wolf-lang#681); the
  corpus harness starts every case with the defaults, so no case can
  show it.
- With no fork, a pipeline stage pelt runs itself runs to the end
  before the next starts, so an endless in-process producer
  (`while :; do echo y; done | head -1`) does not end as it does under
  dash; and `exec cmd` inside a subshell starts `cmd` as a child of
  pelt rather than replacing a subshell process.
- `kill` is not a built-in (wolf can signal only a child it holds a
  handle for, wolf-lang#141), so `kill` is the host's program: it has
  no job ids (`%1`).

**Cleared by sh05 (wolf 0.2.27):** `pending/unset_env` (now
`env/unset_var`: `env_unset`) and `pending/signal_status` (now
`signal/child_term`: `os_wait_status`). `$!` is a process id
(`os_proc_pid`), so `kill $!` reaches the job.

**Cleared by sh03 (H2, wolf 0.2.26):** the fifteen cases that waited on
s215's descriptor builtins — `pipe/pipeline_status`, `control/pipeline`,
`redir/redirect_out`, `redir/redirect_err`, `redir/heredoc`,
`builtin/dot`, `builtin/times`, `func/unset_f`, `tilde/middle`,
`cmdsub/external`, `control/async_list`, `jobs/background`,
`builtin/cd`, `cd/cd_subshell`, `simple/child_stdin` (the ones that
were under `pending/` moved to their subjects' areas).
