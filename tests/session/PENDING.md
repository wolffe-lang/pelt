# Pending session cases

Every case here has its transcript recorded from `dash -i +m` like any
other, is typed into pelt on every `tools/session` pass, and is reported
as `PEND-ok` or `PEND-fail`; it does not decide the exit status.
`tools/session` fails any case marked `pending=` in its `.meta` that is
not named below, so nothing is skipped silently. A case leaves this list
in the commit that makes it pass.

| primitive pelt waits on | where it comes from | cases |
|---|---|---|
| **child stdin** — a command pelt runs reading the keyboard | wolf-lang s215 (spawn with a descriptor map); today `[os.proc.spawn]` wires a child's descriptor 0 to the null device, so `cat` at the prompt ends at once and the next typed line reaches pelt instead | `child_stdin` |
| **chdir** — `cd` | wolf-lang s215 (`os_chdir`) | `cd_root` |
| **pipe** — `a \| b` | wolf-lang s215 (`os_pipe`, a descriptor map), pelt H2 | `pipe` |
| **redirection** — `>`, `<`, here-documents to a command | wolf-lang s215 (a descriptor map), pelt H2 | `redirect_file`, `heredoc` |
| **background jobs** — `&`, `wait`, later `jobs`, `fg`, `bg`, Ctrl-Z | a spawn that does not wait and `$!` (wolf-lang#141), pelt H2; job control (process groups, the terminal's foreground group) a later s lane, pelt H3 | `background` |
| **interrupt** — Ctrl-C | `[os.signal.set]` has no meaning for `SIGINT` (wolf-lang#622), so pelt cannot catch it: Ctrl-C at the prompt, or while a child runs, kills pelt with the child | `ctrl_c_prompt`, `ctrl_c_child` |

**Gaps with no session case**, because the harness cannot type them:

- **isatty** — POSIX makes a shell with no operands interactive only
  when standard input and standard error are terminals. wolf 0.2.24
  cannot ask (`os_isatty` is s215's, unreleased); `fs_fstat(0)` tells a
  regular file from everything else. So `pelt < file` runs the file as
  a script, as dash does, but `printf 'echo hi\n' | pelt` prompts on
  standard error and keeps going after an error, where dash does
  neither. Waits on `os_isatty` in a release (sh03).
- **line editing and history** — none (no termios surface; the
  terminal's own line discipline does the editing: backspace, Ctrl-U,
  Ctrl-W work because the terminal is in canonical mode).
