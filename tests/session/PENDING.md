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
| **alias** | `alias` and alias substitution | pelt (P03) | `c_alias_interactive` |
| **line editor** | no line editor: the terminal's own line discipline does the editing, so an arrow key, Home/End, Ctrl-A/E/K/D/R, Tab, Alt-B are typed into the command as bytes, a line stops at the terminal's 4,095 bytes, and a multi-byte character is erased a byte at a time. Recorded from `bash --posix -i` (dash has no editor of its own in this build's default mode); only standard output and the exit are compared, since each editor draws its own line | pelt (sh07, sh08); wolf-lang W05 (window size, `SIGWINCH`) for a resized window; rulings R2, R3 | `c_ed_complete_command`, `c_ed_complete_file`, `c_ed_delete_char`, `c_ed_home_end`, `c_ed_kill_to_end`, `c_ed_left_insert`, `c_ed_search`, `c_ed_up_arrow`, `c_ed_up_down_edit`, `c_ed_utf8_erase`, `c_ed_utf8_left`, `c_ed_word_motion`, `c_long_line` |
| **history** | no command history: `fc`, the history number in `PS1`'s `!` | pelt (sh08) | `c_hist_fc_edit`, `c_hist_fc_list`, `c_hist_fc_s`, `c_ps1_bang` |
| **vi mode** | `set -o vi` is accepted and does nothing (XCU `sh`, Command Line Editing) | pelt (sh09), after the editor | `c_vi_basic`, `c_vi_history`, `c_vi_motion` |
| **ignoreeof** | `set -o ignoreeof` is accepted and Ctrl-D still ends the shell | pelt (P10) | `c_ignoreeof` |
| **mail** | `MAIL`, `MAILCHECK`, `MAILPATH`: no notice before the prompt | pelt (P10); the file's time is `fs_stat` | `c_mail` |
| **job control** | no job control: `set -m` is accepted and does nothing — no process group per job, no terminal handoff, Ctrl-Z stops nothing the shell can report, no `jobs`, `fg`, `bg`, no job numbers or completion notices. Recorded from `dash -i -m` | wolf-lang W03 (stop reporting, `SIGCONT`, a signal to a group) and #680 (a wait that a signal or a second child can end), #141 (`kill` built in); then pelt (sh12, sh13) | `c_jc_background_group`, `c_jc_background_job`, `c_jc_bg`, `c_jc_bg_ttin`, `c_jc_ctrl_z`, `c_jc_done_message`, `c_jc_fg`, `c_jc_fg_number`, `c_jc_foreground_group`, `c_jc_jobs_list`, `c_jc_jobs_states` |
| **getpid** | `$$` off linux (passes on linux) | wolf-lang#141 | `c_jc_shell_is_leader` |
<!-- census:end -->

**Cleared by sh05 (wolf 0.2.27):** `ctrl_c_prompt` and `ctrl_c_child`
(an interactive pelt listens for `SIGINT`, `[os.signal.disp]`, and
polls for it after the line is read and after the child is reaped).

**Cleared by sh03 (H2, wolf 0.2.26):** `child_stdin`, `cd_root`,
`pipe`, `redirect_file`, `heredoc`, `background`.

**Gaps with no session case**, because the harness cannot type them:

- **job control** — `jobs`, `fg`, `bg`, Ctrl-Z: wolf 0.2.27 has the
  process group, the terminal's foreground group and `SUSPEND`, and
  not yet a stopped child's report, `SIGCONT` or a signal to a group
  (`[os.term.note]`), so the sessions stay `dash -i +m` (pelt H3). `&`
  and `wait` work (`background`, `background_status`).
- **line editing and history** — none yet (`os_term_set_mode` arrived
  in wolf 0.2.27 and is not used; the terminal's own line discipline
  does the editing: backspace, Ctrl-U, Ctrl-W work because the
  terminal is in canonical mode).
- **a command typed right after Ctrl-C at an empty prompt** — dash
  0.5.13.4 loses that line's newline (typed `^C`, `echo after`,
  `exit`, it runs `echo afterexit`); pelt runs each line as typed. Not
  recorded as a case: it is a quirk, not a behaviour scripts rely on.

**isatty** is covered by the differential corpus, not here: the
`stdin/` cases run the shell with the script on a pipe and no operand,
and `default_interactive` types into pelt with standard error a pipe;
in both, pelt (`os_isatty(0)` and `os_isatty(2)`) and dash decide the
shell is not interactive.
