# pelt

A POSIX shell written in wolf.

pelt is `/bin/sh` for [PAX](https://github.com/wolffe-lang/pax) and an ordinary program on Linux and macOS. It targets the POSIX.1-2024 Shell Command Language first; anything of its own comes after that is complete. Every behaviour is tested side by side against `dash` and `bash --posix`.

Status: the language runs, the plumbing does not yet. `pelt -c 'string'` and `pelt script` parse the whole POSIX grammar and run simple commands, compound commands, functions, every expansion and the special built-ins, matching `dash` on a differential corpus (`tests/diff/`). Pipelines, redirections, `&`, `cd` and command substitutions that run another program are refused by name until wolf gains the descriptor builtins they need (`tests/diff/PENDING.md`). The plan lives in the wolf planning repository (`sprints/pelt/`).

```sh
tools/fetch-toolchain   # the pinned wolf, by digest
tools/build             # target/native/pelt and target/release/pelt
tools/difftest --bin target/release
```

## Licence

GPL-3.0-only (`LICENSE`), with the wolf Training Data Permission (`LICENSE-TRAINING-DATA`), as boreutils.
