# sh13 — the umask (and the pin to 0.2.28)

Contract: `sprints/pelt/13-the-umask/sh13-the-umask.md` in the planning
repo. This file is the lane's record: §1 to §3 are committed before the
first change under `src/` or to the pin, and the evidence index (§4) is
filled in as the work lands.

## 1. Forbidden

As the contract's §1: no shell's source is read or searched for
(ruling #43): POSIX.1-2024 (pubs.opengroup.org), man pages as
documentation, black-box runs of dash 0.5.13.4 and `bash --posix`
only. No `extern "c"`. Third-party scripts only through
`tools/script-census` in `--network none` containers with nothing of
the host mounted but a scratch directory under `~/lanes/sh13/`. The
line editor is sh11's (running beside this lane): not touched here;
whichever lands second rebases. No merge, no tag, no issue filed or
closed, no package installed, no other lane's CI run cancelled,
nothing under `~/.claude`; no attribution trailers. The toolchain from
the release archives by digest. Detached kasumi jobs by `setsid` with
the pid recorded and killed by that pid only; scratch under
`~/lanes/sh13/` (`TMPDIR` points there), never `/tmp`; no build on
nomad-1. Strict evidence (#571).

## 2. Inputs, verified (2026-10-12, re-derived before any change)

| input | contract says | measured | drift |
|---|---|---|---|
| pelt trunk | `251f90a` (sh07) | `origin/trunk` = `251f90a`; branch `sh13` cut from it | none |
| the toolchain | 0.2.28 ships `os_umask` | trunk pins wolf 0.2.27 / lupin 0.1.50 / std `87ba162`. wolf-lang release 410118732 (`v0.2.28`, tag → `f71ece8e`), wolf-interp release 409991647 (`v0.1.51`, tag → `f72e78d`); the CHANGELOG at the tag names the bundled std `98e1b7b` and the pelt step: "the toolchain digests; a `umask` built-in can be served by `os_umask`" | none |
| `os_umask` | set-and-answer only; a read is two calls; lupin refuses it by name | CHANGELOG 0.2.28: `os_umask(mask) -> int ! {invalid, unsupported}` "sets the process's file mode creation mask and answers the one it replaced"; "the mask is the process's: every task's, and every child's"; charges `env`; windows `unsupported` by name; "lupin 0.1.51 mirrors seven and refuses `os_umask` … by name (ruling #67 R10)" | none |
| the corpus at trunk | (sh07) 825/0/103 | **825/0/103** on both tiers and under `taskset -c 0-3` (`logs/base-diff-*.log`) | none |
| the sessions | (sh07) 92/0/35 | **92/0/35** on both tiers and under `taskset` (`base-sess-*.log`) | none |
| the clause table | (sh07) 414 of 527 | **414 met of 527 testable (78.6%)**, 111 pending (`base-clause.log`) | none |
| the umask cases pending | `tests/diff/PENDING.md` | four: `umask/c_bad`, `umask/c_s_umask_set`, `umask/c_symbolic`, `umask/c_umask` (statements `umask/1`–`umask/4`) | none |
| the static pelt of trunk | — | sha256 `8a498b238992c0cf…`, the same bytes sh07 measured at `9e4e78e` (`final-unaided.log`) | none |
| the script census, unaided | sh07's: 66/80 | **66 same, 13 differ, 1 unstable** (`base-unaided.tsv`): verdicts and exit statuses identical to sh07's `final-unaided.tsv` | none |
| the script census, aided | sh07's: 76/80 | **76 same, 3 differ, 1 unstable** (`base-aided.tsv`): verdicts and exit statuses identical to sh07's `after-aided.tsv` (xzgrep, zgrep, zdiff differ; pfetch unstable) | none |
| pelt under lupin, today | — | `lupin run pelt.lu` (0.1.50) answers `unsupported: env_vars does not resolve` and exits 4 before it reads a line; `lupin run sh_test.lu` is `unsupported` at `fs_open_mode("/dev/null")` (lupin serves files only inside its own tree) | — |

## 3. Prediction (committed before the first change under `src/`)

Written from the CHANGELOG, the four pending cases, sh07's census
tables and black-box runs of dash and `bash --posix` on the umask forms in
(`notes/sh13-evidence/probe/`); nothing has been built at 0.2.28.

### 3.1 The pin (its own commit)

wolf 0.2.28 / lupin 0.1.51 / std `98e1b7b` (what the archive bundles).
pelt builds on both tiers with `--deny-warnings` and no source change:
no declaration of the eight new prelude names (W0304), and none of the
four new E1010 shapes (the CHANGELOG's s227/s229 censuses built pelt
byte-identical). Every binary's bytes move (`libwolf_rt.a` changed).
At the pin, before `umask`: corpus **825/0/103**, sessions **92/0/35**,
every gate as at trunk; the census unchanged (66 unaided).

### 3.2 `umask`

`umask [-S] [mask]` as XCU says and dash answers: four octal digits
(`0022`); `-S` as `u=rwx,g=rx,o=rx`; an octal operand (low nine bits)
or a symbolic mode (who `ugoa`, ops `+-=`, perms `rwxXs` and the copy
letters `ugo`, comma-separated clauses); status 2 for a bad option or
a bad mode, the shell going on. The mask is the process's
(`os_umask`), so children and `exec` inherit it with nothing handed
over; an in-process subshell (`( … )`, `$( … )`, a pipeline stage, an
`&` list) puts it back when it ends. Until the first `umask`, no call
is made.

**Cases.** The four pending cases pass and leave `PENDING.md`. New
cases recorded from dash, each passing: symbolic forms (`X`, the copy
letters, chained operators, a trailing comma, the empty operand, `s`),
the refused forms and their statuses (`t`, `,`, a lone `who`, `8`,
`-x`), the options (`-S` with an operand prints nothing, `--`, a second
operand ignored), the subshells (`( )`, `$( )`, a pipeline stage, `&`,
a function that does persist), and a program and `exec` inheriting the
mask. **Corpus: (825 + 4 + new)/0/99** on both tiers; sessions
**92/0/35**.

### 3.3 The script census

| pass | before | predicted after | which move |
|---|---:|---:|---|
| unaided | 66 | **76** | the ten sh07 named as stopping at `umask`: configure-hello, configure-sed, configure-gzip, install-sh, config.guess, mkinstalldirs, deb-openssh-client.postinst, deb-tzdata.postinst, init-ssh, lesspipe |
| aided | 76 | **76** | none; the aided pass no longer routes around `umask` (its rewrite is dropped once pelt has the built-in), so its ten scripts now run pelt's own `umask` and stay `same` |

Falsified below 74 or above 76 unaided. Left after: xzgrep, zgrep,
zdiff (a process per pipeline stage, gap 7) and pfetch (`unstable`:
dash differs from itself).

### 3.4 Statements

**414 → 418 of 527 (79.3%)**: `umask/1`–`umask/4` become met; nothing
else moves.

### 3.5 Speed (`tools/bench`)

Three binaries per tier: trunk on 0.2.27, trunk's source on 0.2.28
(the pin alone) and the head. **The head against the pin: no row moves
by more than 2%** (a snapshot gains one `int`, a restore one
comparison, no call until `umask` runs). The pin against trunk: no row
by more than 5%.

### 3.6 Under lupin

pelt still does not run under lupin 0.1.51: `unsupported` at
`env_vars`, exit 4, before the first command, as at 0.1.50, so lupin's
refusal of `os_umask` is never reached by pelt. A four-line probe that
calls `os_umask` under lupin 0.1.51 ends the program as `unsupported`
by name (exit 4), not with the `unsupported` row; under native and
release it answers the old mask. pelt's own handling of the row (a
message, status 2) is for a machine that answers the row (windows,
which pelt does not target).
