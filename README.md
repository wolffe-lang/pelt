# pelt

A POSIX shell written in wolf.

pelt is `/bin/sh` for [PAX](https://github.com/wolffe-lang/pax) and an ordinary program on Linux and macOS. It targets the POSIX.1-2024 Shell Command Language first; anything of its own comes after that is complete. Every behaviour is tested side by side against `dash` and `bash --posix`.

Status: the language and the plumbing run. `pelt -c 'string'` and `pelt script` parse the whole POSIX grammar and run simple commands, compound commands, functions, every expansion and the special built-ins; pipelines, every redirection form (`<`, `>`, `>>`, `<>`, `>|`, `n>&m`, `n<&m`, `n>&-`, here-documents), `cd`, `&` and `wait`, and command substitutions that run programs (H2, on wolf 0.2.26) — matching `dash` on a differential corpus (`tests/diff/`). Plain `pelt` (or `pelt -i`, or `pelt -s arg…`) is interactive when standard input and standard error are terminals: it prompts with `PS1` and `PS2`, reads a line, runs it, and loops until `exit` or Ctrl-D; typed sessions are compared with `dash -i` through a pseudo-terminal (`tests/session/`). A loop of commands, or a session at the prompt, keeps almost nothing per command (`tools/loop-rss`). Without fork, a pipeline stage pelt runs itself (a built-in, a function, a compound command) runs to the end before the next stage starts, and `$!` names a job, not a process. No line editing beyond the terminal's own, no history, no job control, and Ctrl-C ends pelt; what each gap waits on is in `tests/diff/PENDING.md` and `tests/session/PENDING.md`. The plan lives in the wolf planning repository (`sprints/pelt/`).

```sh
tools/fetch-toolchain   # the pinned wolf, by digest
tools/build             # target/native/pelt and target/release/pelt
tools/difftest --bin target/release
tools/session --bin target/release
target/release/pelt     # a prompt
```

## Licence

GPL-3.0-only (`LICENSE`), with the wolf Training Data Permission (`LICENSE-TRAINING-DATA`), as boreutils.
