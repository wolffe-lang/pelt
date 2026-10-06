# pelt — agent guidance

A POSIX shell in pure wolf. Drop-in as `/bin/sh` on the behaviour scripts rely on, differential-tested against `dash` and `bash --posix`.

## The licence rule (read before writing a line)

**Never read, copy or translate the source of any shell:** bash, dash, zsh, ksh/mksh/oksh, busybox (ash, hush), yash, toybox's sh, fish, or any other. Most are GPL or otherwise owned by others; a wolf program translated from one would be a derivative this project does not wholly own. Write pelt from:

- the POSIX.1-2024 Shell Command Language (XCU chapter 2) and the utility pages of its special and regular built-ins;
- the shells' manuals and man pages, as documentation of behaviour;
- black-box runs of `dash` and `bash --posix`, recorded as differential cases.

Do not copy any shell's error or `--help` text: write pelt's own. Differential cases compare stdout and exit status; stderr is compared by presence only.

## Read before writing a line of wolf

1. `AN_AGENTS_GUIDE_TO_WRITING_GOOD_WOLF.md` in the planning repo (`wolffe-lang/wolf`, trunk).
2. Your sprint contract under the planning repo's `sprints/pelt/`. Contracts are binding.
