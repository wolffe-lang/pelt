# Changelog

pelt has no releases yet; the entries below are trunk's, newest first.
Before this file, what each lane changed is in `notes/` (one record a
lane) and in the README's status.

## Unreleased

- `jobs` reuses its listing and releases listing scratch after each call;
  an empty literal query no longer copies an expansion string each time
  (pelt#45). Redirected brace groups, `if` and `while` commands apply
  their redirections directly from the syntax tree instead of keeping a
  temporary list per turn (pelt#54).
- In a `set -m` script, an ended single-process background job gives its
  process entry back while retaining its status and notice; jobs started
  repeatedly from one syntax node share its rendered command text.
  Foreground pipelines retain their per-process status readers (pelt#46).
- Complete commands in sourced interactive input tell and release ended
  jobs before the next complete command, as dash does. A `wait` does not
  itself release a job within the same complete command (pelt#55).
- A simple command's signal-end notice follows its redirected standard
  error. An optimized one-command subshell's notice remains outside its
  redirections and output capture, as a forked subshell's does (pelt#53).
- An invalid `trap` option ends a non-interactive shell with status 2;
  refused built-in writes report an error and status 1 even when the
  refusal is not EPIPE (pelt#28; the script-census timing coin remains).

- **The fork** (wolf 0.2.34 / lupin 0.1.55, the eighth pin; ruling #90,
  pelt#34). On a host whose `os_fork` forks, a subshell `( … )`, a
  command substitution, every list after `&` (a built-in's too) and
  every pipeline stage pelt runs itself are processes, as dash's are:
  the stages of a pipeline run together and an endless producer ends
  when its reader leaves; `( … ) &` and `{ …; } &` run beside the shell
  with a live `$!`; with job control a pipeline with such a stage, and a
  foreground `( … )`, are jobs Ctrl-Z stops and `fg` continues. The
  child sets caught traps back to the default and keeps ignored ones,
  empties the job table, closes what is not its own and ends by
  `os_exit`; a program that is its last command takes its place. A
  `( cmd )` or `$( cmd )` of one simple command the fast path finishes
  still runs in the shell. A subshell's own redirections, and those of
  braces that hold it alone, are its process's: the shell's word that a
  signal ended it, a trap's action run meanwhile and Ctrl-Z's notice go
  to the shell's own descriptors, and a failed one is the subshell's
  status, which `set -e` acts on. `$(trap)` alone lists the shell's
  traps (pelt#17). `$$` is the shell's pid in every subshell. The
  checked machine (`os_fork` answers `unsupported`, ruling #95) runs
  every shape in process as before.
  The three census scripts that read a decompressor's status through a
  pipeline stage, `xzgrep`, `zgrep` and `zdiff`, run as under dash (a
  Linux host's own copies; `tools/script-census` is not run again yet).
- `wait` for a job a poll reaped earlier answers its status without the
  signal's notice, as dash (pelt#47).
- `set -o autocd` is not taken inside a subshell, a command substitution
  or a pipeline stage, as bash 5.3 and zsh 5.9 refuse there (R-sh23-4,
  taken in sh20); `eval` and a function body still take it.
- `set -o autocd`, off by default (ruling #113, pelt#49). In an
  interactive shell a command whose name names a directory, with a slash
  (`home/pax`, `/home/pax/`) or found nowhere by command search (`..`,
  `child`), runs as `cd -- NAME`, with `cd`'s status and message; the
  command's other words are `cd`'s further operands, and a function named
  `cd` is called when one is defined. A function, built-in or program of
  that name still runs; a file or a missing path keeps its answer (126,
  127); a name that is no directory still reaches
  `command_not_found_handle`. `set -o` and `set +o` list it; `pelt -o
  autocd` starts with it on. A shell that is not interactive ignores it,
  as bash ignores `shopt -s autocd` there. Unlike bash, pelt does not
  write `cd -- NAME` before it changes directory, its `cd` takes the
  first of several operands where bash's refuses them (`DIR a b` goes
  to `DIR`), and `command DIR` still cannot be run (126) where bash and
  zsh change directory.

## History, by wolf release (moved from the README on 2026-10-22)

The README used to carry pelt's whole record as one paragraph per wolf
release. It is kept here unchanged, oldest first, so nothing is lost;
entries above this section are the record from now on.

the language and the plumbing run. `pelt -c 'string'` and `pelt script` parse the whole POSIX grammar and run simple commands, compound commands, functions, every expansion and the special built-ins; pipelines, every redirection form (`<`, `>`, `>>`, `<>`, `>|`, `n>&m`, `n<&m`, `n>&-`, here-documents), `cd`, `&` and `wait`, and command substitutions that run programs — matching `dash` on a differential corpus (`tests/diff/`). On wolf 0.2.27: `exec cmd` replaces the shell (the same process, measured by `tools/exec-witness`); a child's environment is exactly the exported variables, so `unset` reaches it; `trap` catches, ignores and resets a signal (five of them at that pin); a child a signal ended answers 128+N; and `$!` is a process id. Plain `pelt` (or `pelt -i`, or `pelt -s arg…`) is interactive when standard input and standard error are terminals: it prompts with `PS1` and `PS2`, reads a line, runs it, and loops until `exit` or Ctrl-D; Ctrl-C ends the program it is waiting for, or the loop it is running, and the prompt comes back. Typed sessions are compared with `dash -i` through a pseudo-terminal (`tests/session/`). A loop of commands, or a session at the prompt, keeps almost nothing per command (`tools/loop-rss`). Of 80 real scripts (`tools/script-census`: configure, automake and libtool helpers, git's test library, Debian and Alpine package and init scripts, small utilities), 76 run exactly as under dash, one more differs only where dash differs from itself, and the other 3 (xzgrep, zgrep, zdiff) need a process for a pipeline stage. On wolf 0.2.28, `umask` sets the process's file mode creation mask (octal or symbolic, `-S`), which every program pelt starts inherits, and a subshell's `umask` ends with the subshell. On wolf 0.2.29, `trap` catches, ignores and resets every signal POSIX lets a program catch, by name or by the host's number, and leaves alone a signal the shell was started ignoring; `$$` and `PPID` are the process's ids on every host; and `kill` is built in (`-s`, `-signal`, `-0`, `-l`, job ids). On wolf 0.2.30, the line editor takes the window's width from the terminal and draws the line again when the window is resized, waits for a key or a signal without waking (an idle prompt costs nothing), honours the erase, kill, interrupt, end-of-file, word-erase and literal-next characters `stty` set, and lets Ctrl-S, Ctrl-Q, Ctrl-V and Ctrl-O reach it. Tab completes a command name (built-ins, reserved words, functions, programs on `PATH`), a file name (relative, absolute or under `~`, quoted so the shell reads it back as itself) or a variable's name (after `$` and `${`); several names complete to what they share, and a second Tab lists them in columns sized to the window. Ctrl-V then Tab types a tab. Aliases are substituted as the shell reads (`alias`, `unalias`, a value ending in a blank, no recursion), `$'…'` quotes with its escapes, `set -o pipefail` gives a pipeline its rightmost failure, `type` and `command -v`/`-V` say what a name is, a utility once found on `PATH` is remembered until `PATH` changes (`hash`), `command -p` searches a standard `PATH`, `read -d` reads to a delimiter, and `sh -ec 'string'` and its kin read their options as dash does. On wolf 0.2.32, an interactive pelt has job control (`set -m`, also in a script): each pipeline of programs runs in a process group of its own and is handed the terminal, Ctrl-Z stops it, `jobs` (`-l`, `-p`), `fg` and `bg` take every job id (`%n`, `%+`, `%-`, `%string`, `%?string`), a job's ending or stopping is told before the next prompt (at once with `set -b`), `kill` reaches a job's group, `kill 0` and `kill -- -N`, `wait` is cut short by a trapped signal, and `exit` with stopped jobs warns once. A subshell, `{ …; } &` and a pipeline stage pelt runs itself are not processes yet, so they are not jobs. An interactive pelt calls a function named `command_not_found_handle` (bash's name) when a command's name is found nowhere: with the command's words as its operands and its redirections around it, in the shell's own environment, so a `cd` there moves the shell (the jump `lope init pelt` defines), and never from inside itself; its status is the command's, and a 127 is said as pelt's usual not-found (pelt#42). A script never calls it. With `set -o autocd` (off by default; `pelt -o autocd` too, and `set +o autocd` turns it off), an interactive pelt runs a command whose name names a directory, with a slash (`home/pax`, `/home/pax/`) or found nowhere (`..`, `child`, `"my dir"`), as `cd -- NAME`: `cd`'s status and message, the command's other words `cd`'s further operands, a function named `cd` called when there is one; a function, built-in or program of that name still runs, a file or a missing path keeps its answer, a name that is no directory still goes to `command_not_found_handle`, and a script ignores the option (pelt#49). A script reaps the jobs it never waits for as the next one starts, so a loop of `cmd &` does not fill the host's process table, and each such job keeps two numbers of the shell's memory; `read` with a redirection, `eval`, `cd`, `command` and `umask` keep almost nothing per command (`tools/shape-rss`, pelt#39). With `set -m` in a script, a job's ending is told after the complete command it ended in, as dash tells it (pelt#41). A test harness whose case times out ends every process the case started, under `tools/syscall-census` too (`tools/reap-witness`, pelt#27).

What it does not do yet, each named with what it waits on in `tests/diff/PENDING.md` and `tests/session/PENDING.md`: without fork, a pipeline stage pelt runs itself (a built-in, a function, a compound command) runs to the end before the next stage starts, and a subshell has no process of its own; `trap` and `kill` know the signals POSIX names and no other (not linux's `IO`, `PWR` or the real-time ones), and `kill` cannot signal a process group; a byte that is not UTF-8 cannot reach a program; `test -r/-w/-x` read the mode bits for the shell's own ids rather than asking `access(2)`, so a read-only or `noexec` mount and ACLs are not seen; `wait` is not cut short by a trapped signal. The line editor (emacs keys, `set -o vi`) and the history (`fc`, a shared `HISTFILE` kept to `HISTSIZE`, Ctrl-R, vi `v`, `!` in `PS1`) are there; no job control. What pelt lacks is measured in [`docs/CENSUS.md`](docs/CENSUS.md) (POSIX clause by clause, 80 real scripts, the prompt, speed), and what comes next is [`docs/PLAN.md`](docs/PLAN.md).
