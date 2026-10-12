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

### 3.7 The result against the prediction

Measured on kasumi (linux x86-64; dash 0.5.13.4 for the corpus, the
census images' own dash for the scripts). **The branch was rebased onto
trunk `87ffb21` (sh11, the line editor) while the census ran**; every
number below the pin row is at the rebased head `91c08b4` unless it
says otherwise.

| prediction | predicted | measured | held? |
|---|---|---|---|
| 3.1 the pin builds with no source change | both tiers, `--deny-warnings` | both tiers, no change (`logs/pin.status`, at `975056b`, before the rebase) | held |
| 3.1 at the pin: corpus, sessions, census | 825/0/103, 92/0/35, 66 unaided | **825/0/103** on both tiers and under `taskset`, **92/0/35**, census **66** with every verdict and exit status as at trunk (`scripts/pin-unaided.tsv`, static `b5c25c84…`) | held |
| 3.2 the four pending cases pass | 4 | **4** | held |
| 3.2 the corpus | (825 + 4 + new)/0/99 | **835/0/99** at the rebased head (trunk after sh11 is 826/0/103: 826 + 4 + 5 new = 835) on both tiers and under `taskset`; sessions (sh11's) **171/0/26**, as trunk | held |
| 3.3 the census, unaided | 76 (band 74–76) | **76 same, 3 differ, 1 unstable** (`scripts/final-unaided.tsv`, static `c16bd143…`): the ten named moved, nothing else | held |
| 3.3 the census, aided | 76 | **76** with the new instrument (umask run by pelt, `final-aided.tsv`) and **76** with sh07's (umask skipped, `final-aided-sh07.tsv`): the same 3 differ, pfetch unstable | held |
| 3.4 statements | 414 → 418 of 527 | **418 of 527 (79.3%)** before the rebase; after it, sh11's table has 544 statements and **431** are met (80.0%): sh11's 427 plus `umask/1`–`umask/4` | held |
| 3.5 speed, head against pin | no row above 2% | user instructions (load-independent, `bench/instructions.txt`): fork +0.3% / +0.3%, **param +1.6% release, +0.7% native**. Wall time, medians of 9: under `taskset -c 0-3` param **+2.2% release, +2.9% native**, configure-shaped −0.2% / +1.3%; unpinned param +3.1% / **+6.0%** (load 1.3–2.4) | **held on instructions, missed on wall time for param** (by under one point pinned): the cost is about 1,700 user instructions a loop turn on release, from the two `int` fields every copy of the state now carries; not trimmed |
| 3.5 speed, pin against trunk | no row above 5% | wall time, pinned: param −4.1% release / −0.7% native, configure-shaped −2.0% / −1.1%, fork and pipeline within 2% | held |
| 3.6 lupin | `env_vars` first; `os_umask` ends the program by name | as predicted (`lupin/runs.txt`) | held |

**Seen red.** The nine umask cases against the pin's pelt (no
`umask`): **8 fail, 1 passes** (`logs/final-umask-on-pin.log`). The one
is `umask/c_bad`: both its lines expect status 2, and pelt's old "not
supported yet" also answered 2, so that case cannot tell the two apart;
`umask/refused` (whose `-w` and `0027` columns need a real mask) is the
case that does. The table check was planted red once (an expectation
off by one: `wolf test` failed naming `mask_from(0027, =r)`,
`logs/plant-selftest.log`) and put back.

## 4. Evidence index

- **The prediction:** `3c6c58c` (was `f44788f` before the rebase),
  before the pin (`f22c33b`, was `975056b`) and the first `src/` change
  (`b4262eb`, was `ae0ff8e`).
- **The probes:** `notes/sh13-evidence/probe/` — the umask forms under
  dash and `bash --posix`; pelt at `91c08b4` answers all three files
  byte for byte as dash, exit statuses included, on both tiers
  (`pelt-at-head.txt`).
- **The census:** `notes/sh13-evidence/scripts/` — `base-*` (trunk
  `251f90a`, static `8a498b23…`, the same bytes sh07 measured),
  `pin-unaided.*` (`975056b`, `b5c25c84…`), `final-unaided.*`,
  `final-aided.*`, `final-aided-sh07.*` (`91c08b4`, `c16bd143…`); the
  binaries' digests in `*.bin`. Images `sh06-arch`, `sh06-debian`,
  `sh06-alpine` built from `tools/script-census`'s pinned Containerfiles
  into the lane's own store; every script checked against
  `tools/script-census.pins`.
- **The gauntlets:** `notes/sh13-evidence/logs/` — `base-*` (trunk),
  `pin-*` (the pin), `final-*` (the rebased head `91c08b4`: fmt, both
  builds, `wolf test`, the clause census, difftest on both tiers and
  under `taskset`, the planted difftest red, sessions on both tiers and
  under `taskset`, the planted session red, glob-rss, loop-rss,
  exec-witness, `oracle-record --check` 0 drifted, sh11's edit-witness
  on both tiers and `gen-width --check`: every exit status 0,
  `final.status`, `final-extra.status`).
- **Seen red:** `logs/final-umask-on-pin.log`, `logs/plant-selftest.log`.
- **lupin:** `notes/sh13-evidence/lupin/`.
- **The bench:** `notes/sh13-evidence/bench/` — trunk `87ffb21` on 0.2.27
  (`base`), the pin alone (`pin`), the head; medians, loads, the
  binaries' digests (`heads`), instruction counts.
- **CI:** PR wolffe-lang/pelt#23; run 38212019281 green before the
  rebase (it also showed 0.2.28 builds no tier on linux aarch64, so the
  workflow's comment moved, `91c08b4`); run 38216565366 green at
  `91c08b4`.

## 5. Done-when

- Branch `sh13`, PR #23 open and unmerged, CI green at the head;
  `wolf/tools/lane-audit.sh pelt sh13 23` run from the org directory,
  its exit status read directly.
- pelt issues this branch answers: **#21 (P17)** — the message naming
  wolf 0.2.24 is gone with the stub; `umask` is a built-in. Nothing
  closed by this lane.

## 6. Not verified

- linux aarch64 (no tier builds there at 0.2.28) and the census on
  macOS (CI's macOS job runs every umask case green; the scripts are
  linux-only).
- A pipeline whose program stage is started before an in-process stage
  that runs `umask`: the in-process stage's mask is the process's while
  it runs, so a program stage started alongside it could create files
  under it. No case covers that order; dash runs every stage in its own
  process.
- A symbolic `umask` on a host whose dash differs from 0.5.13.4 (the
  Debian and Alpine images carry 0.5.12; the census scripts agreed,
  the forms in the probe were not run there).
- The `unsupported` row's message: no machine pelt runs on answers it
  (lupin ends the program before, windows is not a target).
