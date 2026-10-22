# Changelog

pelt has no releases yet; the entries below are trunk's, newest first.
Before this file, what each lane changed is in `notes/` (one record a
lane) and in the README's status.

## Unreleased

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
