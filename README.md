# pelt

A POSIX shell written in [wolf](https://github.com/wolffe-lang/wolf-lang).
pelt is `/bin/sh` on [PAX](https://github.com/wolffe-lang/pax) and an
ordinary program on Linux and macOS.

It targets the POSIX.1-2024 Shell Command Language first; anything of
its own comes after that is complete. Every behaviour is recorded from
`dash` (the oracle of record) and checked against `bash --posix`, and no
shell's source is ever read: pelt is clean-room, black-box only.

## Status at a glance

| measure | where it stands |
|---|---|
| POSIX.1-2024 XCU chapter 2 and the built-ins' pages, testable statements met | 505 of 547 (`tools/clause-census`; the table and the misses in [`docs/CENSUS.md`](docs/CENSUS.md)) |
| differential corpus against dash, both tiers | 968 cases, 0 failing, 38 pending on a named primitive (`tests/diff/`) |
| typed sessions against `dash -i` through a pseudo-terminal | 283 sessions, 0 failing, 3 pending (`tests/session/`) |
| real `sh` scripts that run as under dash | 76 of 80 (`tools/script-census`: configure, automake and libtool helpers, git's test library, Debian and Alpine package and init scripts) |
| memory per command at a prompt or in a loop | almost nothing (`tools/loop-rss`, `tools/shape-rss`) |
| toolchain | the wolf and lupin pinned by digest in `wolf-toolchain.toml` |

The two documents behind the numbers: [`docs/CENSUS.md`](docs/CENSUS.md)
measures what pelt lacks (POSIX clause by clause, real scripts, the
prompt, speed) and [`docs/PLAN.md`](docs/PLAN.md) says what comes next
and what each piece needs from wolf or PAX. Trunk's changes are in
[`docs/CHANGELOG.md`](docs/CHANGELOG.md).

## Try it

On PAX, pelt is already the shell: boot the image and you are at its
prompt. Elsewhere, build it from source with the pinned compiler
(there are no binary releases yet):

```sh
tools/fetch-toolchain      # the pinned wolf and lupin, fetched by digest
tools/build                # target/native/pelt and target/release/pelt
target/release/pelt        # a prompt
target/release/pelt -c 'for f in *; do echo "$f"; done'
target/release/pelt script.sh
```

`tools/build --static` links the release tier with `cc -static`, the
shape PAX runs as pid 1. Every build denies warnings.

## What works

**The language.** `pelt -c 'string'`, `pelt script` and the prompt
parse the whole POSIX grammar: simple and compound commands, functions,
every expansion (parameters, arithmetic, command substitution, word
splitting, pathname expansion, quoting, `$'…'`), aliases, and the
special built-ins. `sh -ec 'string'` and its kin read their options as
dash does.

**Redirections and pipelines.** `<`, `>`, `>>`, `<>`, `>|`, `n>&m`,
`n<&m`, `n>&-` and here-documents; pipelines, with `set -o pipefail`
for the rightmost failure; `&`, `wait`, `$!`, and command substitutions
that run programs.

**Built-ins.** `cd`, `pwd`, `echo`, `printf`, `test`, `read` (`-d`),
`getopts`, `umask` (octal and symbolic, `-S`), `trap`, `kill` (`-s`,
`-signal`, `-0`, `-l`, job ids, a process group), `type`, `command`
(`-v`, `-V`, `-p`), `hash` (a utility once found is remembered until
`PATH` changes), `alias`/`unalias`, `fc`, `jobs`, `fg`, `bg`, `exec`
(which replaces the shell in the same process), and the rest of the
special built-ins.

**Signals and processes.** `trap` catches, ignores and resets every
signal POSIX lets a program catch, by name or by the host's number, and
leaves alone a signal the shell was started ignoring; a child a signal
ended answers 128+N; `$$`, `PPID` and `$!` are real process ids on every
host; a child's environment is exactly the exported variables. A
subshell `( … )`, a command substitution, a list after `&` and every
pipeline stage pelt runs itself (a function, a compound command, a
built-in) are processes of their own (wolf 0.2.34's `os_fork`), as
dash's are: the stages of a pipeline run together, a producer ends when
its reader leaves, the child starts with caught traps back at the
default, and a subshell's own redirections are its process's. A script
reaps the jobs it never waits for as the next one starts, so a loop of
`cmd &` does not fill the process table.

**The prompt.** Interactive when standard input and standard error are
terminals (`pelt`, `pelt -i`, `pelt -s`): `PS1` and `PS2`, Ctrl-C ends
the program it is waiting for or the loop it is running and the prompt
comes back, Ctrl-D ends the shell. The line editor has emacs keys and
`set -o vi`, takes the window's width from the terminal and redraws on a
resize, honours the erase, kill, interrupt, end-of-file, word-erase and
literal-next characters `stty` set, and lets Ctrl-S, Ctrl-Q, Ctrl-V and
Ctrl-O through. Tab completes a command name (built-ins, reserved words,
functions, programs on `PATH`), a file name (relative, absolute or under
`~`, quoted so the shell reads it back as itself) or a variable's name
after `$` or `${`; a second Tab lists the candidates in columns sized to
the window. History: `fc`, a shared `HISTFILE` kept to `HISTSIZE`,
Ctrl-R, vi's `v`, and `!` in `PS1`. An idle prompt costs nothing: it
waits for a key or a signal without waking.

**Job control.** `set -m` (on by default at an interactive prompt, also
in a script): each pipeline of programs runs in its own process group
and is handed the terminal, Ctrl-Z stops it, `jobs` (`-l`, `-p`), `fg`
and `bg` take every job id (`%n`, `%+`, `%-`, `%string`, `%?string`), a
job's ending or stopping is told before the next prompt (at once with
`set -b`), `wait` is cut short by a trapped signal, and `exit` with
stopped jobs warns once. A pipeline with a stage pelt runs itself, and
a foreground `( … )`, are jobs like any other: Ctrl-Z stops the whole of
it and `fg` continues it.

**Two hooks for a modern prompt.** An interactive pelt calls a function
named `command_not_found_handle` (bash's name) when a command's name is
found nowhere, in the shell's own environment and with the command's
words, so a `cd` there moves the shell: this is what `lope init pelt`
uses for no-prefix directory jumping. With `set -o autocd` (off by
default; `pelt -o autocd` too) a command that names a directory, with a
slash (`home/pax`, `/home/pax/`) or found nowhere (`..`, `child`), runs
as `cd -- NAME`, the way bash's `shopt -s autocd` and zsh's `AUTO_CD`
do; a function, built-in or program of that name still wins, and a
script ignores the option, as do a subshell, a command substitution and
a pipeline stage (bash's line). Where pelt parts from bash on the details,
`docs/CHANGELOG.md` says so.

**Startup.** pelt is POSIX here too: an interactive shell runs the file
named by `ENV` before its first prompt (there is no `~/.peltrc`), so

```sh
export ENV="$HOME/.peltrc"          # in the shell that starts pelt
echo 'set -o autocd' >> ~/.peltrc   # and, with lope: eval "$(lope init pelt)"
```

## What it does not do yet

Each gap is named with the primitive it waits on in
[`tests/diff/PENDING.md`](tests/diff/PENDING.md) and
[`tests/session/PENDING.md`](tests/session/PENDING.md), and every
pending case still runs on every pass and is reported, never skipped.

- Where wolf's `os_fork` does not fork (the checked machine of `wolf
  test` and `wolf conform-run --checked`, which answers `unsupported`),
  a subshell, a list after `&` and a pipeline stage pelt runs itself
  still run inside the shell: they are no jobs there, and a stage runs
  to its end before the next starts.
- `trap` and `kill` know the signals POSIX names and no other (not
  Linux's `IO`, `PWR` or the real-time ones).
- A byte that is not UTF-8 cannot reach a program.
- `test -r`, `-w` and `-x` read the mode bits for the shell's own ids
  rather than asking `access(2)`, so a read-only or `noexec` mount and
  ACLs are not seen.
- Three of the 80 census scripts (xzgrep, zgrep, zdiff) need a process
  for a pipeline stage.

## How it is tested

Nothing here is believed without a recording. Every tool below is in
the tree so the measurement can be taken again.

| tool | what it checks |
|---|---|
| `tools/difftest --bin target/release` | the differential corpus, every case's output, status and files against the expectation recorded from dash |
| `tools/session --bin target/release` | typed sessions through a pseudo-terminal, byte for byte against `dash -i` |
| `tools/oracle-record`, `tools/session-record` | record a new case's expectation from the oracle |
| `tools/exec-witness`, `tools/signal-witness`, `tools/hist-witness`, `tools/edit-witness` | one behaviour each, measured on the live process (the same pid after `exec`, a signal's disposition, the history file, the editor) |
| `tools/reap-witness` | a test case that times out leaves nothing running |
| `tools/script-census` | the 80 real scripts, run as under dash |
| `tools/clause-census` | the POSIX statement table, counted |
| `tools/syscall-census`, `tools/loop-rss`, `tools/shape-rss`, `tools/session-rss`, `tools/glob-rss` | what a command costs in calls and memory |
| `tools/check-fmt`, `tools/check-test`, `wolf test` | the formatter's fixed point, the unit tests |

CI runs the same tools in tiers: a pull request runs what its paths can
affect (`ci/tiers.py` decides), the merge runs everything, and a nightly
re-runs the lot and opens an issue when red. Each lane of work leaves a
record under `notes/` with its prediction, its measurements and what it
left undone.

## Layout

```
src/pelt.lu        the program (over the module src/sh/)
src/sh/            parse, expand, exec, redir, builtin, jobs, signal, kill,
                   edit, complete, hist, interact, arith, pattern, umask, …
tests/diff/        the differential corpus (.lu cases, .meta expectations)
tests/session/     the typed sessions (.tr transcripts, .meta)
tests/reap/        the reaper's cases
tests/census/      the 80 real scripts
tools/             the build and every measurement tool above
docs/              CENSUS.md, PLAN.md, CHANGELOG.md
notes/             one record per lane of work
ci/                the tier planner and its tests
wolf-toolchain.toml  the pinned compiler and interpreter, by digest
```

## Contributing

- dash is the oracle and bash the second opinion, both as black boxes.
  Never read any shell's source; pelt's licence depends on it.
- A behaviour change comes with its case, recorded from the oracle and
  seen red before green.
- Build with the pinned toolchain only; the pin moves in its own commit.
- `docs/CHANGELOG.md` gets an entry; a lane of work gets a note.

## Licence

GPL-3.0-only (`LICENSE`), with the wolf Training Data Permission
(`LICENSE-TRAINING-DATA`), as boreutils.
