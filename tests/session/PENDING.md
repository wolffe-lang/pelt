# Pending session cases

Every case here has its transcript recorded from `dash -i +m` like any
other, is typed into pelt on every `tools/session` pass, and is reported
as `PEND-ok` or `PEND-fail`; it does not decide the exit status.
`tools/session` fails any case marked `pending=` in its `.meta` that is
not named below, so nothing is skipped silently. A case leaves this list
in the commit that makes it pass.

<!-- census:begin -->
The census cases (sh06, `c_*`; `docs/CENSUS.md`), by what they wait on.
"P03", "W03" and the like are the issue texts in the sh06 report
(`notes/sh06-the-census.md`).

| waits on | what is missing | whose work | cases |
|---|---|---|---|
<!-- census:end -->

None is pending since sh26.

**Cleared by sh26 (the corners):** `c_ignoreeof` (`set -o ignoreeof`:
the end of file refused with dash's words, R-sh26-4) and `c_mail`
(`MAIL`, `MAILPATH`, `MAILCHECK`, R-sh26-5). New with them:
`mail_path`, `mail_interval` and `jc_assign_text` (pelt#56).

**Cleared by sh20 (wolf 0.2.34, the fork):** `c_jc_mixed_pipeline`: a
stage pelt runs itself is a process that joins the job's group with
`SUSPEND` at the default, so Ctrl-Z stops the whole pipeline as one job.
New with it: `jc_subshell_stop` (a foreground `( … )` is a job Ctrl-Z
stops and `fg` continues), `jc_background_subshell` (the prompt's line
goes on while `( … ) &` runs) and `subshell_jobs` (which subshells list
the shell's jobs, as dash's).

**Cleared by sh18 (wolf 0.2.32, job control):** `c_jc_background_group`,
`c_jc_background_job`, `c_jc_bg`, `c_jc_bg_ttin`, `c_jc_ctrl_z`,
`c_jc_done_message`, `c_jc_fg`, `c_jc_fg_number`, `c_jc_foreground_group`,
`c_jc_jobs_list`, `c_jc_jobs_states`: a pipeline of programs in a group of
its own, the terminal handed over and taken back, stops reported by
`os_wait_poll`, `jobs`, `fg`, `bg`, the notices. pelt is given `+m`
in every session dash is (`tools/lib_session.py`'s `argv_for`).

**Cleared by sh16 (the completion):** `c_ed_complete_command`,
`c_ed_complete_file` (Tab completes commands, files and variables,
ruling #69 R3).

**Cleared by sh15 (wolf 0.2.30):** `c_ed_ctrl_v`, `c_ed_tab_literal`,
`c_vi_insert_ctrl_v` (lnext: the editor turns `EXTENDED` off while a
line is edited, so macOS hands it Ctrl-V too).

**Cleared by sh14 (wolf 0.2.29):** `c_jc_shell_is_leader` (`$$` is
`os_pid` on every host).

**Cleared by sh12 (the history):** `c_ed_search` (Ctrl-R),
`c_hist_fc_edit`, `c_hist_fc_list`, `c_hist_fc_s`, `c_ps1_bang`,
`c_vi_v`; and the differential case `fc/c_noninteractive`.

**Cleared by sh11 (the line editor):** `c_ed_delete_char`,
`c_ed_home_end`, `c_ed_kill_to_end`, `c_ed_left_insert`, `c_ed_up_arrow`,
`c_ed_up_down_edit`, `c_ed_utf8_erase`, `c_ed_utf8_left`,
`c_ed_word_motion`, `c_long_line`, `c_vi_basic`, `c_vi_history`,
`c_vi_motion`.

**Cleared by sh05 (wolf 0.2.27):** `ctrl_c_prompt` and `ctrl_c_child`
(an interactive pelt listens for `SIGINT`, `[os.signal.disp]`, and
polls for it after the line is read and after the child is reaped).

**Cleared by sh03 (H2, wolf 0.2.26):** `child_stdin`, `cd_root`,
`pipe`, `redirect_file`, `heredoc`, `background`.

**Gaps with no session case**, because the harness cannot type them:

- **`set -b`'s notice while a line is typed** (2.11/11) — the harness
  types when the shell is quiet and cannot place a notice between two
  keys; and dash 0.5.13.4 writes it at the next prompt anyway (sh18,
  black-box p11), where POSIX and bash write it at once, as pelt does
  (`notes/sh18-evidence/probe/keys/p24`, `p25`).
- **the history file across shells** — a session is one shell, so
  `HISTFILE` written by one shell and read by the next, two shells
  sharing one file at once, and the file cut to `HISTSIZE` are asked
  from outside by `tools/hist-witness` (sh12), in CI on both tiers.
- **a command typed right after Ctrl-C at an empty prompt** — dash
  0.5.13.4 loses that line's newline (typed `^C`, `echo after`,
  `exit`, it runs `echo afterexit`); pelt runs each line as typed. Not
  recorded as a case: it is a quirk, not a behaviour scripts rely on.

**isatty** is covered by the differential corpus, not here: the
`stdin/` cases run the shell with the script on a pipe and no operand,
and `default_interactive` types into pelt with standard error a pipe;
in both, pelt (`os_isatty(0)` and `os_isatty(2)`) and dash decide the
shell is not interactive.
