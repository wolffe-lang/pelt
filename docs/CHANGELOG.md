# Changelog

pelt has no releases yet; the entries below are trunk's, newest first.
Before this file, what each lane changed is in `notes/` (one record a
lane) and in the README's status.

## Unreleased

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
