# Pending session cases

Every case here has its transcript recorded from `dash -i +m` like any
other, is typed into pelt on every `tools/session` pass, and is reported
as `PEND-ok` or `PEND-fail`; it does not decide the exit status.
`tools/session` fails any case marked `pending=` in its `.meta` that is
not named below, so nothing is skipped silently. A case leaves this list
in the commit that makes it pass.

| primitive pelt waits on | where it comes from | cases |
|---|---|---|
| **interrupt** — Ctrl-C | `[os.signal.set]` has no meaning for `SIGINT` (wolf-lang#622), so pelt cannot catch it: Ctrl-C at the prompt, or while a child runs, kills pelt with the child | `ctrl_c_prompt`, `ctrl_c_child` |

**Cleared by sh03 (H2, wolf 0.2.26):** `child_stdin`, `cd_root`,
`pipe`, `redirect_file`, `heredoc`, `background`.

**Gaps with no session case**, because the harness cannot type them:

- **job control** — `jobs`, `fg`, `bg`, Ctrl-Z: process groups and the
  terminal's foreground group are a later s lane (pelt H3). `&` and
  `wait` work (`background`, `background_status`).
- **line editing and history** — none (no termios surface; the
  terminal's own line discipline does the editing: backspace, Ctrl-U,
  Ctrl-W work because the terminal is in canonical mode).

**isatty** is covered by the differential corpus, not here: the
`stdin/` cases run the shell with the script on a pipe and no operand,
and `default_interactive` types into pelt with standard error a pipe;
in both, pelt (`os_isatty(0)` and `os_isatty(2)`) and dash decide the
shell is not interactive.
