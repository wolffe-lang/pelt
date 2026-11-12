# Contributing to pelt

pelt is a POSIX shell written in [wolf](https://github.com/wolffe-lang/wolf-lang):
`/bin/sh` on [PAX](https://github.com/wolffe-lang/pax) and an ordinary program on
Linux and macOS. It aims to be a drop-in `/bin/sh` for the behaviour scripts rely
on, and every behaviour is held to `dash` (the oracle of record) and checked
against `bash --posix`.

## The licence rule

**Never read, copy or translate the source of any shell**: bash, dash, zsh,
ksh, mksh, oksh, busybox (ash, hush), yash, toybox's sh, fish or any other.
Most are GPL or otherwise owned by others, and a wolf program translated from
one would be a derivative this project does not wholly own. Write pelt from:

- the POSIX.1-2024 Shell Command Language (XCU chapter 2) and the pages of its
  special and regular built-ins;
- the shells' manuals and man pages, as documentation of behaviour;
- black-box runs of `dash` and `bash --posix`, recorded as differential cases.

Do not copy any shell's error or `--help` text either: pelt's messages are its
own. That is why a differential case compares standard output and the exit
status exactly, and standard error by presence only.

## The toolchain

`wolf-toolchain.toml` pins the wolf compiler and the lupin interpreter by the
sha256 digest of their release archives, and wolf-std as a tree at a commit.
Build with the pinned toolchain only:

```sh
tools/fetch-toolchain    # stages all three into .wolf-bin/, refusing a digest mismatch
```

`tools/lib-toolchain.sh` refuses a toolchain whose `--version` drifts from the
pin. A pin moves in a commit of its own.

## Building and running the checks

```sh
tools/build                              # target/native/pelt and target/release/pelt
tools/check-fmt                          # the formatter's fixed point
tools/check-test                         # the unit tests (`wolf test`)
tools/self-check release                 # the same table checks on a compiled tier
tools/difftest --bin target/release      # the differential corpus against dash's recordings
tools/session --bin target/release       # typed sessions through a pseudo-terminal
tools/difftest-selftest target/release   # the harness can still see a difference
python3 ci/tiers-test.py                 # CI's planner against its rules
```

Every build denies warnings. The README's "How it is tested" table lists the
witnesses and measurement tools, one behaviour each.

## What a change must bring

- **A behaviour change comes with its case**: a differential case under
  `tests/diff/` or a typed session under `tests/session/`, its expectation
  recorded from the oracle (`tools/oracle-record`, `tools/session-record`, which
  refuse any dash but the one `tests/diff/ORACLE` names; `tools/oracle-image`
  and `tools/oracle-container` run that oracle in a container).
- **Seen red before green**: the case fails against pelt before the change and
  passes after it.
- A case that needs something pelt does not have yet is marked `pending=` and
  listed by name in `tests/diff/PENDING.md`; it still runs, but does not decide
  the result.
- A bug or a missing feature in wolf is filed upstream at
  [wolffe-lang/wolf-lang](https://github.com/wolffe-lang/wolf-lang) with a
  small program that shows it, never silently worked around.
- `docs/CHANGELOG.md` gets an entry. A larger piece of work leaves a record
  under `notes/`: what it predicted, what it measured, what it left undone.

## Commits

- Small and chunked: one file or one coherent change a commit, so the history
  tells how the work was done. Stage what you mean, never `git add -A`.
- A terse, imperative subject, with the issue in parentheses where there is
  one (`Take the prompt's user and host from the system when unset (pelt#115)`).
- No trailers: no co-author, sign-off or "generated with" lines.

## Pull requests

Open a pull request from a branch against `trunk`. An unlabelled pull request
runs only a cheap check, so your own run of the checks is the evidence: the
description names the head you ran the commands above on and their results,
and for a behaviour change the case that went red and then green. A change to
CI, `tools/` or the toolchain pin also needs the full CI set green at its head
before it merges: ask for the `full-matrix` label once the head is the one to
merge, not when the pull request opens.
