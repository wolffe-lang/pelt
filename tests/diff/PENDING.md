# Pending differential cases

Every case here has its expectation recorded from dash like any other,
RUNS on every `tools/difftest` pass, and is reported as `PEND-ok` or
`PEND-fail`; it does not decide the exit status. `tools/difftest` fails
any case marked `pending=` in its `.meta` that is not named below, so
nothing is skipped silently. A case leaves this list in the commit that
makes it pass.

| primitive pelt waits on | where it comes from | cases |
|---|---|---|
| **user database** — `~login` | no `getpwnam` surface in wolf 0.2.27; not filed until a lane needs it beyond this case | `tilde/user` |

<!-- census:begin -->
## The census cases (sh06)

Cases named `c_*` were written by the clause census (`docs/CENSUS.md`,
`tests/census/clauses.tsv`). The ones pelt does not answer as POSIX.1-2024
requires are pending here, by what they wait on. "P01"… and "W01"… are
the issue texts in the sh06 report (`notes/sh06-the-census.md`).

| waits on | what is missing | whose work | cases |
|---|---|---|---|
| **host-dir-size** | nothing pelt lacks: the case's `-s` row asks whether an empty directory has a size, and the oracle was recorded on kasumi's btrfs, where it has none; on ext4 (the linux runners) and APFS (macOS) an empty directory has a size, so dash there answers `-s` true for it as pelt does (sh07). PEND-ok on btrfs | the oracle's host | `test/c_files` |
| **command-special** | `command .`/`command set`/`command exec` with an error still ends the shell (XCU 2.8.1 note 1) | pelt (P09) | `builtin/c_special_error_command` |
| **builtin-dashdash** | `export -- name` and `printf -- format`: `--` is taken as an operand | pelt (P09) | `builtin/c_export_invalid`, `printf/c_usage` |
| **exit-in-exit-trap** | `exit` with no operand inside an EXIT trap action uses the action's last status, not the status from before the trap | pelt (P09) | `builtin/c_exit_in_trap_status` |
| **readonly-p-unset** | `readonly -p` omits a readonly variable that has no value | pelt (P09) | `builtin/c_readonly_p` |
| **pwd-from-env** | `PWD` is not taken from the environment at start, so a shell started in a directory reached through a symbolic link reports the physical path (XCU 2.5.3) | pelt (P09) | `cd/c_pwd_from_env` |
| **printf-float** | `printf` `%e %f %g` (optional in POSIX; dash has them and configure scripts use `%f`) | pelt (P09); wolf has float formatting | `printf/c_floats` |
| **printf-numbered** | `printf '%2$s'` (new in POSIX.1-2024; neither oracle has it) | not counted in the census | `printf/c_numbered` |
| **trap-p** | `trap -p` (new in POSIX.1-2024) | pelt (P10) | `signal/c_trap_p` |
| **ps4-expansion** | `PS4` is written as is, not parameter-expanded (XCU 2.5.3) | pelt (P10) | `option/c_ps4` |
| **xtrace-assignment** | `set -x` does not trace a command that is only assignments | pelt (P10) | `option/c_xtrace_forms` |
| **verbose** | `set -v` writes nothing | pelt#6 | `option/c_verbose`, `option/c_verbose_stderr` |
| **arith-increment** | `$((++x))`: dash reads two unary pluses, pelt refuses it (`++` is optional in POSIX) | pelt, a ruling (R4); not counted in the census | `arith/c_incr_optional` |
| **special-name-function** | a function named after a special built-in is accepted (dash refuses; unspecified by POSIX) | not counted in the census | `simple/c_special_not_shadowed` |
| **ulimit** | `ulimit` | wolf-lang: no `getrlimit`/`setrlimit` surface (W02) | `ulimit/c_bad`, `ulimit/c_enforced`, `ulimit/c_file_size`, `ulimit/c_resources` |
| **uid** | `test -O`, `test -G` | wolf-lang#633 | `test/c_owner` |
| **enoexec** | a file with no `#!` that cannot be a script (a NUL before the first newline): pelt hands it to the host's `/bin/sh` and answers whatever that shell answers (127 under dash, 126 under bash), where POSIX says 126 | wolf-lang#682 | `simple/c_enoexec_binary` |
| **non-utf8-bytes** | a byte that is not UTF-8 (`a\377b` from a command substitution) cannot be a program's argument, since a wolf `str` is UTF-8: it reaches the program as `?`. Valid UTF-8 passes unchanged everywhere since sh07 (`quote/utf8_bytes`); this case's other lines pass | wolf-lang W06 (byte strings) | `quote/c_s_high_bytes` |
| **user database** | `~login` | wolf-lang: no `getpwnam` surface (W04) | `tilde/c_user_root` |
<!-- census:end -->

**No case, named:**

- `kill 0`, `kill -- -N` (a process group) and `kill -1`: since sh18
  sent through `os_signal_send_group` and `os_signal_send_all`. No case
  here, under the oracle or pelt: `kill 0` and `kill -1` would signal
  the harness's own group or every process the user may signal; a
  group a session made is signalled in the session corpus instead
  (`c_jc_kill_group`).
- `kill` and `trap` for a signal POSIX does not name (linux's `IO`,
  `PWR`, `STKFLT`, 16, the real-time signals, by name or number): wolf
  has a meaning for the signals POSIX names and no other, so pelt
  refuses these (status 2 from `kill`, 1 from `trap`) where dash takes
  them. `kill -l` lists the 28 names wolf has.
- A job id (sh18): a job's number is the lowest one free, as dash's;
  `%name` and `%?text` match the job's command text, which with job
  control off is empty, as dash's (black-box: s02), so they name no job
  in a script.

**Cleared by sh20 (wolf 0.2.34), the fork:** `builtin/c_s_dot_special_file`,
`env/c_subshell_concurrent`, `pending/subshell_signal` (now
`signal/subshell_signal`), `pipe/c_concurrent_stages`,
`pipe/c_shell_producer_ends`, `redir/c_s_cmdsub_fd_pipeline`,
`signal/c_subshell_trap_reset`, `signal/c_trap_ignore_pipe`,
`wait/c_subshell`: a subshell, a command substitution, a list after `&`
and a pipeline stage pelt runs itself are processes (`os_fork`,
`src/sh/fork.lu`), each with its traps back at the default and its own
descriptors and (empty) job table. And `signal/c_trap_cmdsub_shows_parent`:
a substitution that is one `trap` command alone keeps the shell's traps
(XCU `trap`, as dash's). The two named here with no case have one now:
the endless producer (`pipe/endless_producer`) and `exec` in a subshell
(`exec/exec_replaces_subshell`). On a host that does not fork (the
checked machine: `unsupported`, ruling #95 R4 C) every one of these
shapes still runs in process, to its end.

**Cleared by sh18 (wolf 0.2.32), job control:** `jobsctl/c_jobs_script`
(`jobs`, `-p`), `jobsctl/c_fg_bg_no_monitor`, `jobsctl/c_monitor_script_pgid`
(`set -m`: a group per job), `option/c_long_names` (`b` in `$-`), and the
two interruptible waits, `pending/wait_interrupted` (now
`signal/wait_interrupted`) and `signal/c_wait_interrupted_term`: `wait`
polls the children (`os_wait_poll`) and parks in `os_signal_wait` on
`CHILD` and the trapped signals, so a trapped signal cuts it short with
`128 + N`. `c_wait_interrupted_term`'s sender is `( … ) &`, which until
sh20 pelt ran in process to its end before `wait`, so the answer was
dash's by another order; since sh20 it is a process and the order is
dash's too.

**Cleared by sh14 (wolf 0.2.29), `kill`:** `kill/c_bad`,
`kill/c_job_id`, `kill/c_list`, `kill/c_send` and `wait/c_job_id`.
`kill` is a built-in on `os_signal_send` and `os_signal_number`, and
`kill` and `wait` take a job id.

**Cleared by sh14 (wolf 0.2.29), ignored at start:**
`signal/c_ignored_on_entry`. pelt reads the set of signals it was
started ignoring (`os_signal_ignored`) and neither traps nor resets
them; `tools/signal-witness` asks it from outside (the corpus harness
starts every case with the defaults).

**Cleared by sh14 (wolf 0.2.29), the signals:** `pending/trap_usr1`
and `pending/trap_ignore_usr1` (now under `signal/`),
`signal/c_trap_abrt_number`, `signal/c_trap_alrm`, `signal/c_trap_pipe`,
`signal/c_trap_usr1_self`, `signal/c_trap_winch_cont`: wolf has a
meaning for every signal POSIX names (`[os.signal.set]`, s232), and
`trap` catches, ignores and resets the twenty a program may hear.

**Cleared by sh14 (wolf 0.2.29):** `pending/pid` (now `param/pid`),
`pending/exec_pid` (now `exec/exec_pid`), `param/c_pid_is_real`,
`param/c_pid_subshell` and `env/c_ppid`: `$$` is `os_pid` and `PPID` is
`os_ppid` on every host, where `$$` was read from `/proc` on linux
alone.

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
