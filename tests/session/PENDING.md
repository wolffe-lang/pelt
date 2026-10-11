# Pending session cases

Every case here has its transcript recorded from `dash -i +m` like any
other, is typed into pelt on every `tools/session` pass, and is reported
as `PEND-ok` or `PEND-fail`; it does not decide the exit status.
`tools/session` fails any case marked `pending=` in its `.meta` that is
not named below, so nothing is skipped silently. A case leaves this list
in the commit that makes it pass.

No case is pending.

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
