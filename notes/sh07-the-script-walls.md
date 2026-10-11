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
