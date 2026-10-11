# pelt

A POSIX shell written in wolf.

pelt is `/bin/sh` for [PAX](https://github.com/wolffe-lang/pax) and an ordinary program on Linux and macOS. It targets the POSIX.1-2024 Shell Command Language first; anything of its own comes after that is complete. Every behaviour is tested side by side against `dash` and `bash --posix`.

Status: the language and the plumbing run. `pelt -c 'string'` and `pelt script` parse the whole POSIX grammar and run simple commands, compound commands, functions, every expansion and the special built-ins; pipelines, every redirection form (`<`, `>`, `>>`, `<>`, `>|`, `n>&m`, `n<&m`, `n>&-`, here-documents), `cd`, `&` and `wait`, and command substitutions that run programs — matching `dash` on a differential corpus (`tests/diff/`). On wolf 0.2.27: `exec cmd` replaces the shell (the same process, measured by `tools/exec-witness`); a child's environment is exactly the exported variables, so `unset` reaches it; `trap` catches, ignores and resets `HUP`, `INT`, `QUIT`, `TERM` and `USR2`; a child a signal ended answers 128+N; and `$!` is a process id. Plain `pelt` (or `pelt -i`, or `pelt -s arg…`) is interactive when standard input and standard error are terminals: it prompts with `PS1` and `PS2`, reads a line, runs it, and loops until `exit` or Ctrl-D; Ctrl-C ends the program it is waiting for, or the loop it is running, and the prompt comes back. Typed sessions are compared with `dash -i` through a pseudo-terminal (`tests/session/`). A loop of commands, or a session at the prompt, keeps almost nothing per command (`tools/loop-rss`). Of 80 real scripts (`tools/script-census`: configure, automake and libtool helpers, git's test library, Debian and Alpine package and init scripts, small utilities), 66 run exactly as under dash, one more differs only where dash differs from itself, and every one of the other 13 stops at `umask` or at a pipeline stage that needs a process of its own.

What it does not do yet, each named with what it waits on in `tests/diff/PENDING.md` and `tests/session/PENDING.md`: without fork, a pipeline stage pelt runs itself (a built-in, a function, a compound command) runs to the end before the next stage starts, and a subshell has no process of its own; no `umask` (wolf's next release); `trap` records but cannot catch a signal wolf has no meaning for (`USR1`, `ALRM`, `PIPE`); a byte that is not UTF-8 cannot reach a program; `test -r/-w/-x` read the mode bits for the shell's own ids rather than asking `access(2)`, so a read-only or `noexec` mount and ACLs are not seen; `wait` is not cut short by a trapped signal; `$$` is the process id on linux only. No line editing beyond the terminal's own, no history, no job control. What pelt lacks is measured in [`docs/CENSUS.md`](docs/CENSUS.md) (POSIX clause by clause, 80 real scripts, the prompt, speed), and what comes next is [`docs/PLAN.md`](docs/PLAN.md).

```sh
tools/fetch-toolchain   # the pinned wolf, by digest
tools/build             # target/native/pelt and target/release/pelt
tools/difftest --bin target/release
tools/session --bin target/release
tools/exec-witness target/release/pelt
tools/clause-census     # the POSIX clause table, counted
target/release/pelt     # a prompt
```

## Licence

GPL-3.0-only (`LICENSE`), with the wolf Training Data Permission (`LICENSE-TRAINING-DATA`), as boreutils.
