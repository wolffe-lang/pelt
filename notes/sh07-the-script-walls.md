# sh07 — the script walls (what stops real scripts under pelt)

Contract: `sprints/pelt/07-the-script-walls/sh07-the-script-walls.md`
in the planning repo. This file is the lane's record: §2 and §3 are
committed before the first change under `src/`, and the evidence index
(§4) is filled in as the work lands.

## 1. Forbidden, absolutely

As the contract's §1: no shell's source is read or searched for
(ruling #43): POSIX.1-2024 (pubs.opengroup.org), man pages as
documentation, black-box runs of dash 0.5.13.4 and `bash --posix`
only. No `extern "c"`; a missing primitive is a wolf-lang finding with
a witness. No case weakened, no oracle re-recorded to make pelt pass:
a pending case moves to the corpus only when pelt matches the recorded
oracle. Third-party scripts only through `tools/script-census` in
`--network none` containers with nothing of the host mounted but a
scratch directory under `~/lanes/sh07/`; nothing third-party
committed. No `rm` outside `~/lanes/sh07/` and this lane's clones; no
`git add -A`; nothing under `~/.claude`; no merge; no attribution
trailers. Strict evidence (#571); spawning rows also under
`taskset -c 0-3`. Detached kasumi jobs by `setsid` and a recorded pid;
no build on nomad-1; no package installs. At most two CI runs at once.
Scratch lives under `~/lanes/sh07/` (`TMPDIR` points there for every
tool run), never in `/tmp`.

## 2. Inputs, verified (2026-10-11, re-derived from origin before any change)

| input | contract says | measured | drift |
|---|---|---|---|
| pelt trunk | `84a02dc` | `origin/trunk` = `84a02dc` ("notes/sh06: the final corpus run and oracle check"); branch `sh07` cut from it | none |
| the toolchain | (the pin) | `wolf-toolchain.toml`: wolf 0.2.27 `0ddda6b`, lupin 0.1.50 `32b970d`, std `87ba162`; `tools/fetch-toolchain` accepted the archives on kasumi; no newer wolf release exists (`gh release list`: v0.2.27 is the latest, 2026-10-11T04:12Z) | none |
| the corpus | 804/0/117 | **804/0/117** on both tiers on kasumi (`kasumi:~/lanes/sh07/logs/base-diff-{native,release}.log`, `difftest: total 804 0 117 (9)`) | none |
| the sessions | 92/0/35 | **92/0/35** (release tier, `base-sess-release.log`) | none |
| the clause table | 400 of 527 | `tools/clause-census`: **532 statements, 400 met of 527 testable (75.9%)**, 125 pending, 2 gap, 5 untestable, 18 not counted (`base-clause.log`) | none |
| sh06's issue texts | P01, P07, P11, P14, P15, P16 in `docs/PLAN.md` | the texts are in `notes/sh06-the-census.md` §6 (P01–P16) and their cases in `tests/diff/PENDING.md`'s census table; `docs/PLAN.md` carries the gap table, not the P-numbers | the P-texts live in the sh06 note, not PLAN.md |
| the script census | 50/80 unaided | re-run below (§4) before any change | — |
| **the contract's target** | **72 of 80 unaided, from gaps 1, 4, 5, 6, the UTF-8 half of 8, P15, P16** | sh06's 72 was the **aided** pass, and that pass also routed around **`umask`** (gap 2, nine scripts), which is not in this contract and cannot be done at wolf 0.2.27 (no `os_umask`; s230's lands in the release after 0.2.27, and none has been cut). sh06's own table: the nine `umask` scripts (install-sh, config.guess, mkinstalldirs, deb-openssh-client.postinst, deb-tzdata.postinst, lesspipe, configure-hello/-sed/-gzip through `config.guess`) and the three fork-shaped ones (xzgrep, zgrep, zdiff: gap 7) are walls this contract does not touch. **80 − 9 − 3 = 68 is the ceiling for this lane** | the target is 4 above what the listed items can reach; reported, not absorbed |

## 3. Prediction (committed before the first change under `src/`)

Written from sh06's census tables (`notes/sh06-evidence/scripts/`
`constructs.md`, `scripts.tsv`), the pending cases and reading pelt's
own source; nothing has been changed or run under the new code.

### 3.1 The script census, unaided, after each item in order

| after | scripts the item frees | unaided |
|---|---|---|
| (now) | — | **50** |
| 1 `test` file primaries (P01) | ltmain.sh, git-test-lib, git-t0000-basic, deb-openssh-server.postinst, deb-ca-certificates.postinst, deb-libc6.postinst, deb-libc6.preinst, deb-base-files.postinst, init-rsync, init-ssh, init-procps, service, which.debianutils (deb-tzdata.postinst still stops at `umask`) | **63** |
| 2 patterns (P11) | none alone: ylwrap still needs item 5, the configures need `umask` | 63 |
| 3 assignments (P07) | none alone: the configures need `umask` (through `config.guess`) | 63 |
| 4 UTF-8 bytes (P14, half) | update-ca-certificates | **64** |
| 5 `trap … 13` (P15) | test-driver, tap-driver.sh, ylwrap (with item 2) | **67** |
| 6 `.` of `/dev/null` (P16) | pfetch | **68** |

**Final: 68 of 80**, falsified below 66 or above 68. The twelve left:
nine on `umask` (wolf's next release), three on fork (gap 7, W01).

### 3.2 The cases

Moved from pending to passing (15): `test/c_s_test_access`,
`test/c_files`, `test/c_permissions`, `test/c_file_types`,
`test/c_file_compare` (item 1); `glob/c_s_bracket_slash_case`,
`glob/c_no_file_rules_in_case`, `quote/c_dq_default_word`,
`simple/c_path_order` (item 2); `simple/c_assign_current`,
`param/c_s_star_assign_ifs`, `param/c_star_assign`,
`command/c_declaration`, `simple/c_declaration_utility` (item 3);
`signal/c_s_trap_by_number` (item 5).

Stay pending, under a truer name:
- `quote/c_s_high_bytes`: its `a\377b` line is a byte that is not
  UTF-8, which a wolf `str` cannot carry (W06). A new case holding
  only its UTF-8 lines passes.
- `builtin/c_s_dot_special_file`: once `.` reads `/dev/null`, its FIFO
  line has the writer as an in-process background subshell
  (`(echo … >pipe &)`), and pelt opening the FIFO for writing waits
  for a reader that never comes: it times out, and waits on fork (gap
  7). A new case whose writer is a program passes.
- `test/c_owner` (`-O`, `-G`) stays on wolf-lang#633 off linux (not in
  the contract's list).

Corpus after: **(804 + 15 + the new cases) / 0 / 102**, both tiers;
sessions unchanged at 92/0/35.

### 3.3 Statements met

**400 → 415 of 527** (78.7%): `test/8`, `test/9`, `test/10`,
`test/14`, `test/1b`, `trap/17`, `2.14.1/8`, `2.14.3/8`, `2.5.2/5`,
`2.5.2/16`, `2.9.1.1/2`, `command/7`, `2.9.1.2/1`, `2.9.1.4/3`,
`2.2.3/5` become met. `2.2/1` (bytes) and `dot/8` stay pending, each
behind the old case that now waits on W06 or fork.

### 3.4 `test -r/-w/-x` without `access(2)`

pelt reads the mode bits and owner with `fs_stat` (wolf 0.2.27) and
its own effective uid, gid and groups from `/proc/self/status` on
linux; off linux it asks `id` once, and only when the answer depends on
who is asking. Predicted to match dash for every file in the cases, as
a user and as root (root: `-r`/`-w` true for any file, `-x` when any
execute bit is set or it is a directory). Where it cannot match
`access(2)`: a read-only or `noexec` mount, ACLs, and capabilities
short of root (W07).

### 3.5 Speed (`tools/bench`, release tier, against dash)

**No row moves by more than 5%.** `fork` runs `/bin/true` by path
(no search); `pipeline` and `param` touch nothing changed;
`configure-shaped`'s `command -v` search was one `stat`-like call per
directory and stays one (`fs_stat` in place of `fs_is_file`).

### 3.6 The result against the prediction

Measured on kasumi (linux x86-64, dash 0.5.13.4 for the corpus; the
census images' own dash for the scripts), at the end of each item
(`notes/sh07-evidence/scripts/step*.tsv`, the 18 scripts that changed
re-run with a static pelt built at that commit) and at the head.

| after | predicted | measured | what differs from the prediction |
|---|---:|---:|---|
| (trunk `84a02dc`) | 50 | **50** | — (`base-unaided.tsv`: verdicts and digests identical to sh06's) |
| 1 `test` (`f3f0d15`) | 63 | **61** | `ltmain.sh --help` also needed item 2; `init-ssh` passes `test -x` and then stops at `umask` (sh06's aided pass skipped `umask`, so nobody had seen that wall) |
| 2 patterns (`df1a62e`) | 63 | **62** | `ltmain.sh` |
| 3 assignments (`d5bd035`) | 63 | **62** | — |
| 4 UTF-8 (`c130113`) | 64 | **63** | update-ca-certificates, as predicted |
| 5 `trap … 13` (`b0d0814`) | 67 | **66** | test-driver, tap-driver.sh, ylwrap, as predicted |
| 6 `.` (`644b48b`) | 68 | **66 + 1 unstable** | pfetch now runs to the end and matches dash's runs 0 and 1; its run 2 prints the memory in use, which moved between dash's own two runs (`unstable`: counted neither way; the same on a second try, `after-aided-and-pfetch.log`) |

**66 of 80 unaided, the bottom of the predicted band (66–68): held.**
The contract's 72 was not reachable, as §2 said; with `umask` routed
around (`--aided`), 76 of 80 run as under dash (`after-aided.tsv`). The
13 still differing, each with the construct it stops at (the first
`pelt:` line of its runs, `after-unaided.log`, and the aided pass):

| scripts | construct | waits on |
|---|---|---|
| configure-hello, configure-sed, configure-gzip (through `build-aux/config.guess`), install-sh, config.guess, mkinstalldirs, deb-openssh-client.postinst, deb-tzdata.postinst, init-ssh, lesspipe | `umask` is "not supported yet" (`umask/c_s_umask_set`) | wolf's release after 0.2.27 (s230's `os_umask`), then pelt (PLAN S4) |
| xzgrep, zgrep, zdiff | a pipeline stage's write to descriptor 4 inside `$( … )` is lost (`redir/c_s_cmdsub_fd_pipeline`): the decompressor's status comes back empty | a process per pipeline stage (gap 7, W01 / ruling R1) |

**The cases.** 14 moved from pending to passing, not 15: `test/c_files`
stays pending, now on the oracle's host. Its `-s` row asks whether an
empty directory has a size; the oracle was recorded on kasumi's btrfs,
where it has none, and on the CI hosts' ext4 and APFS it has one, so
dash there answers `-s` true as pelt does (the access witness's
`dirsize` runs show dash itself answering both ways: true on a tmpfs,
false on btrfs; CI run 38168369021, ubuntu: `PEND-fail test/c_files`,
every other test case `ok`). 7 new cases from dash, all passing:
`simple/assign_order_program`, `param/at_star_nosplit`,
`simple/declaration_forms`, `test/primaries_more`, `quote/utf8_bytes`,
`signal/trap_numbers_common`, `builtin/dot_fifo_program`. The corpus is
**825/0/103** on both tiers and under `taskset -c 0-3` (predicted
(804 + 15 + new)/0/102: one fewer moved, for `c_files`); sessions
92/0/35; `tools/oracle-record --check` 0 drifted. Run against trunk's
pelt (`84a02dc`, release tier), **all 21 moved and new cases fail**
(`difftest: total 0 21 0`, `notes/sh07-evidence/logs/`
`h3-cases-on-trunk-pelt.log`): each is a gate that has been seen red on
the code it guards against.

**Statements: 400 → 414 of 527 (78.6%)**, predicted 415: `test/8`
stays pending behind `test/c_files`. 2.14 Pattern matching is now 100%,
the `test` page 87%.

**`test -r/-w/-x` without `access(2)`** (`notes/sh07-evidence/access/`,
`witness-644b48b.log`): 13 files and directories, as root and as uid
1000, in the census's Arch image (dash 0.5.13.4), every row the same as
dash's but one: as root, `-w` of a file on a **read-only mount** is
true under pelt (the mode bits allow it) and false under dash (access(2)
answers `EROFS`). That is W07, as predicted; ACLs, `noexec` mounts and
capabilities short of root were not measured. The identity comes from
`/proc/self/status` on linux and from `id -u`/`id -G` on macOS (CI's
macOS job runs every access case green), asked only when the mode bits
give different answers to different askers.

**Speed** (`notes/sh07-evidence/bench/`, head `9e4e78e` against trunk
`84a02dc`, both tiers built on kasumi, load 2.4–3.2). Wall time,
medians of 9 (unpinned / under `taskset -c 0-3`), release tier: fork
+0.4% / −1.7%, pipeline +1.9% / +2.8%, param +0.2% / +4.6%,
configure-shaped +0.4% / +2.2%; native: fork +0.2% / +1.0%, pipeline
+1.6% / −0.9%, param +4.2% / +3.4%, configure-shaped +4.6% / +2.8%.
User instructions (`perf stat -e instructions:u`, load-independent,
`instructions.txt`): release fork +0.3%, pipeline +1.1%, param +2.2%,
configure-shaped +1.8%; native +1.2%, +2.2%, +2.5%, +2.5%. **No row
moves by more than 5%: held**, but only after two trims the first
measurement asked for: at `644b48b` param cost +4.2% instructions on
release, and at `f2202d8` param native measured +6.8% wall under
load (the instruction count said +3.8%). `8ef1de3` takes the in-order
bookkeeping off a lone assignment, `f2202d8` keeps the groups as a
`str` so the fast path's copy of the state allocates nothing, and
`9e4e78e` carries "no field splitting here" as a flag on the word
instead of a field of the shell written and restored per expansion.

## 4. Evidence index

- **The prediction:** `ef03131`, pushed before the first change under
  `src/` (`72038d8`).
- **The census, before:** `notes/sh07-evidence/scripts/base-unaided.tsv`
  and `.log` (static pelt of trunk, sha256 `906c2a7a7ba7ca49…`, the
  same binary sh06 measured): 50 same, 30 differ.
- **The census, after each item:** `step1-f3f0d15.tsv` …
  `step5-b0d0814.tsv` and `steps.out` (each static pelt's digest).
- **The census, at the head:** `after-unaided.tsv`/`.log` (static pelt
  of `644b48b`, sha256 `adc24d9b18642061…`: 66 same, 13 differ, 1
  unstable), `after-aided.tsv` (76 same, 3 differ, 1 unstable),
  `final-unaided.tsv`/`.log` (static pelt of the final source head
  `9e4e78e`, sha256 `8a498b238992c0cf…`: 66 same, 13 differ, 1
  unstable, the same verdicts as at `644b48b`). Images: `sh06-arch`, `sh06-debian`, `sh06-alpine`,
  built from `tools/script-census`'s pinned Containerfiles into
  kasumi's lane-private store; every script's sha256 checked against
  `tools/script-census.pins` (identical before and after).
- **The corpus and sessions at the head:** `notes/sh07-evidence/logs/`
  `h3-*` (gauntlet at `9e4e78e`: fmt, both builds, `wolf test`, the
  clause census, difftest on both tiers and under `taskset`, sessions
  on both tiers and under `taskset`, glob-rss, loop-rss, exec-witness,
  oracle-record `--check`; every exit status 0, `h3.status`); `base-*` the same at trunk before any change.
- **The access witness:** `notes/sh07-evidence/access/` (`witness.sh`,
  `access.sh`, `dirsize.sh`, `witness-644b48b.log`).
- **The bench:** `notes/sh07-evidence/bench/` (`speed-unpinned.txt`,
  `speed-pinned.txt`, the loads, `instructions.txt`, the binaries'
  digests in `heads`).
- **The gates seen red:** the 21 moved and new cases against trunk's
  pelt, `logs/h3-cases-on-trunk-pelt.log` (0 pass, 21 fail).
- **CI:** PR wolffe-lang/pelt#9; run 38168369021 (at `f3f0d15`:
  ubuntu `PEND-fail test/c_files`, the host-dir-size evidence), run
  38176525398 green on all three jobs at `9e4e78e`.

## 5. Done-when

- Branch `sh07`, PR #9 open and unmerged, CI green at the head.
- `wolf/tools/lane-audit.sh pelt sh07 9`, run from the org directory,
  its exit status read directly (the report says it).
- pelt issues this branch fixes (sh06's numbering; none is filed yet,
  so nothing is closed): **P01** (`test/c_files` stays pending on the
  oracle's host only; `-O`/`-G` stay on wolf-lang#633), **P07**,
  **P11**, **P15** (recorded and listed; catching SIGPIPE stays
  wolf-lang#679), and the UTF-8 half of **P14** and the `/dev/null` and
  program-written-FIFO half of **P16**; P14's non-UTF-8 half waits on
  W06 and P16's shell-written FIFO on fork (gap 7).
- Ruling #69 (R1 B, R5 keep `local`, R6 arithmetic as dash, R7 A),
  made while this lane ran, changes nothing here: `local` is kept and
  treated as a declaration utility, as dash does.
