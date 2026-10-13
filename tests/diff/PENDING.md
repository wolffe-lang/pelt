# Pending differential cases

Every case here has its expectation recorded from dash like any other,
RUNS on every `tools/difftest` pass, and is reported as `PEND-ok` or
`PEND-fail`; it does not decide the exit status. `tools/difftest` fails
any case marked `pending=` in its `.meta` that is not named below, so
nothing is skipped silently. A case leaves this list in the commit that
makes it pass.

| primitive pelt waits on | where it comes from | cases |
|---|---|---|
| **an interruptible wait** — `wait` cut short by a trapped signal | `os_wait_status` blocks until the child ends and nothing waits for "a child or a signal" (`[os.term.note]` leaves stop reporting and the rest to the next job-control lane): the action runs after the jobs end and `wait` answers 0, where dash runs it at once and answers 128+N (wolf-lang#680) | `pending/wait_interrupted` |
| **fork** — a process for a subshell | none planned: pelt runs `( … )` in-process, so a signal sent to "the subshell" (`$PPID` of its child) reaches the shell itself, whose trap then runs where dash's subshell would have died | `pending/subshell_signal` |
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
| **sh-option-parsing** | `sh -ec 'cmd'` (option letters joined with `c`), `--`, and `-s -` | pelt (P02) | `sh/c_combined_options`, `sh/c_dash_s` |
| **alias** | `alias`, `unalias`, alias substitution (XCU 2.3.1), and `command -v` of an alias or of a file that is not executable | pelt (P03) | `alias/c_after_reserved`, `alias/c_alias_missing`, `alias/c_alias_names`, `alias/c_alias_print`, `alias/c_basic`, `alias/c_no_self_recursion`, `alias/c_not_inherited`, `alias/c_parse_time`, `alias/c_position`, `alias/c_quoted_not`, `alias/c_subshell`, `alias/c_takes_effect_next`, `alias/c_trailing_blank`, `alias/c_unalias`, `alias/c_value_tokens`, `command/c_v` |
| **type** | `type` | pelt (P04) | `type/c_type`, `type/c_type_path` |
| **hash** | `hash` | pelt (P04) | `hash/c_hash` |
| **command-p** | `command -p` | pelt (P04) | `command/c_p` |
| **dollar-single-quote** | `$'…'` (XCU 2.2.4, new in POSIX.1-2024) | pelt (P05) | `quote/c_ds_control`, `quote/c_ds_embedded`, `quote/c_ds_escapes`, `quote/c_ds_hex`, `quote/c_ds_octal`, `quote/c_ds_plain`, `quote/c_ds_quoted` |
| **pipefail** | `set -o pipefail` is accepted and does nothing (XCU 2.9.2) | pelt (P06) | `option/c_pipefail_option`, `pipe/c_pipefail` |
| **read-trailing-delimiter** | `IFS=: read a b c` on `a:b:c:` leaves the trailing delimiter in the last variable | pelt (P08) | `read/c_fields` |
| **readonly-read-getopts** | `read` and `getopts` into a readonly variable, and `read` into an invalid name, answer 0 | pelt (P08) | `builtin/c_readonly_everywhere`, `read/c_bad_target` |
| **read-d** | `read -d delim` (new in POSIX.1-2024) | pelt (P08) | `read/c_delim` |
| **read-no-var** | `read` with no variable (unspecified by POSIX; dash refuses, pelt reads) | pelt, with P08; not counted in the census | `read/c_no_var` |
| **command-special** | `command .`/`command set`/`command exec` with an error still ends the shell (XCU 2.8.1 note 1) | pelt (P09) | `builtin/c_special_error_command` |
| **builtin-dashdash** | `export -- name` and `printf -- format`: `--` is taken as an operand | pelt (P09) | `builtin/c_export_invalid`, `printf/c_usage` |
| **exit-in-exit-trap** | `exit` with no operand inside an EXIT trap action uses the action's last status, not the status from before the trap | pelt (P09) | `builtin/c_exit_in_trap_status` |
| **readonly-p-unset** | `readonly -p` omits a readonly variable that has no value | pelt (P09) | `builtin/c_readonly_p` |
| **pwd-bad-option** | `pwd -x` answers 0 | pelt (P09) | `pwd/c_pwd_bad` |
| **cd-e** | `cd -P -e` (new in POSIX.1-2024) | pelt (P09) | `cd/c_dash_e` |
| **pwd-from-env** | `PWD` is not taken from the environment at start, so a shell started in a directory reached through a symbolic link reports the physical path (XCU 2.5.3) | pelt (P09) | `cd/c_pwd_from_env` |
| **printf-partial-number** | `printf %d 12x` prints 0 where the leading digits are the value | pelt (P09) | `printf/c_bad_operand` |
| **printf-float** | `printf` `%e %f %g` (optional in POSIX; dash has them and configure scripts use `%f`) | pelt (P09); wolf has float formatting | `printf/c_floats` |
| **printf-numbered** | `printf '%2$s'` (new in POSIX.1-2024; neither oracle has it) | not counted in the census | `printf/c_numbered` |
| **trap-p** | `trap -p` (new in POSIX.1-2024) | pelt (P10) | `signal/c_trap_p` |
| **trap-in-cmdsub** | `$(trap)` shows nothing where it must show the invoking shell's traps | pelt (P10) | `signal/c_trap_cmdsub_shows_parent` |
| **ps4-expansion** | `PS4` is written as is, not parameter-expanded (XCU 2.5.3) | pelt (P10) | `option/c_ps4` |
| **xtrace-assignment** | `set -x` does not trace a command that is only assignments | pelt (P10) | `option/c_xtrace_forms` |
| **verbose** | `set -v` writes nothing | pelt#6 | `option/c_verbose`, `option/c_verbose_stderr` |
| **notify-flag** | `set -o notify` does not put `b` in `$-` | pelt (P10) | `option/c_long_names` |
| **arith-increment** | `$((++x))`: dash reads two unary pluses, pelt refuses it (`++` is optional in POSIX) | pelt, a ruling (R4); not counted in the census | `arith/c_incr_optional` |
| **special-name-function** | a function named after a special built-in is accepted (dash refuses; unspecified by POSIX) | not counted in the census | `simple/c_special_not_shadowed` |
| **fork** | a compound command or function after `&`, and every pipeline stage pelt runs itself, runs to its end before the shell goes on: no concurrency, no SIGPIPE to a shell-written producer, a subshell is not a process (XCU 2.9.2, 2.9.3.1, 2.13); `(echo … >fifo &)` opens the FIFO for writing inside the shell, which waits for a reader that comes only after it, so `builtin/c_s_dot_special_file` times out (its `. /dev/null` line passes since sh07, and `builtin/dot_fifo_program` reads a FIFO a program writes); and `signal/c_trap_ignore_pipe` (since sh14 `trap '' PIPE` is honoured, `signal/trap_ignore_pipe_fifo`; this case's writer is a brace group in a pipeline, which runs to its end before the reader starts, so its write meets a pipe that still has a reader) | wolf-lang: a fork (sh06 issue W01), or pelt re-executing itself per subshell (ruling R1) | `builtin/c_s_dot_special_file`, `env/c_subshell_concurrent`, `pipe/c_concurrent_stages`, `pipe/c_shell_producer_ends`, `redir/c_s_cmdsub_fd_pipeline`, `signal/c_subshell_trap_reset`, `wait/c_subshell`, `signal/c_trap_ignore_pipe` |
| **ulimit** | `ulimit` | wolf-lang: no `getrlimit`/`setrlimit` surface (W02) | `ulimit/c_bad`, `ulimit/c_enforced`, `ulimit/c_file_size`, `ulimit/c_resources` |
| **kill** | `kill` as a built-in: `kill -l`, exit statuses, a signal to the shell's own pid | wolf-lang#141 (a signal to any pid), then pelt | `kill/c_bad`, `kill/c_job_id`, `kill/c_list`, `kill/c_send` |
| **job-ids** | `wait %1`, `kill %1` | pelt once `kill` is a built-in (wolf-lang#141) | `wait/c_job_id` |
| **jobs** | `jobs`, `jobs -p` | pelt (P12); job states need wolf-lang W03 | `jobsctl/c_jobs_script` |
| **job-control** | `set -m`: a process group per job | wolf-lang: stop reporting, `SIGCONT`, a signal to a group, an interruptible wait (W03, wolf-lang#680) | `jobsctl/c_fg_bg_no_monitor`, `jobsctl/c_monitor_script_pgid` |
| **uid** | `test -O`, `test -G` | wolf-lang#633 | `test/c_owner` |
| **enoexec** | a file with no `#!` that cannot be a script (a NUL before the first newline): pelt hands it to the host's `/bin/sh` and answers whatever that shell answers (127 under dash, 126 under bash), where POSIX says 126 | wolf-lang#682 | `simple/c_enoexec_binary` |
| **non-utf8-bytes** | a byte that is not UTF-8 (`a\377b` from a command substitution) cannot be a program's argument, since a wolf `str` is UTF-8: it reaches the program as `?`. Valid UTF-8 passes unchanged everywhere since sh07 (`quote/utf8_bytes`); this case's other lines pass | wolf-lang W06 (byte strings) | `quote/c_s_high_bytes` |
| **interruptible wait** | `wait` cut short by a trapped signal | wolf-lang#680 | `signal/c_wait_interrupted_term` |
| **user database** | `~login` | wolf-lang: no `getpwnam` surface (W04) | `tilde/c_user_root` |
<!-- census:end -->

**No case, named:**

- With no fork, a pipeline stage pelt runs itself runs to the end
  before the next starts, so an endless in-process producer
  (`while :; do echo y; done | head -1`) does not end as it does under
  dash; and `exec cmd` inside a subshell starts `cmd` as a child of
  pelt rather than replacing a subshell process.
- `kill` is not a built-in (wolf can signal only a child it holds a
  handle for, wolf-lang#141), so `kill` is the host's program: it has
  no job ids (`%1`).

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
