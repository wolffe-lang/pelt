# The script census: smallest constructs (sh06, item 2)

pelt = static build of `4437c81` (trunk `b32bebc` code, wolf 0.2.27 /
lupin 0.1.50), sha256 `906c2a7a7ba7ca49b840c0240d5f091e369ac9dc2a89c8c0885104b021cd6e6d`.
Each construct below was cut from a failing script by running pieces of
it, then rewritten from scratch as a case of this lane's own (the files
under `cases/`); every case was run under dash 0.5.13.4, `bash --posix`
5.3.20 and pelt on kasumi (`kasumi:~/lanes/sh06/sc/tri FILE`), and the
answers below are those runs. A script is counted under a construct when
the construct is part of what makes it differ (a script can count under
several); "first" is the construct it hits first.

## The verdict, in one line

**Unaided: 50 of 80 scripts run as under dash (62.5%); 30 differ; 0
hang; 0 crashes.** The **aided pass** (the same 80, each script and the
files it sources rewritten by `tools/script-census --aided` so that the
four most-counted gaps go around pelt: `test -x/-w/-r/-L/-h` run
`/usr/bin/test`, `umask` skipped, `trap … 13` spelled `PIPE`, autoconf's
three bracket-with-slash `case` arms spelled without the bracket):
**72 of 80 same (90%), 8 differ, 0 hang** — and the 8 are exactly
constructs 5–8: configure-hello/-sed/-gzip (6, `$*` in an assignment:
exit 0 now, wrong host checks in stdout and config.h), xzgrep, zgrep,
zdiff (5), update-ca-certificates (7), pfetch (8). So constructs 1–4
(three of them pelt's own work, umask waiting on s230's `os_umask`)
account for 22 of the 30 differing scripts, and 1–8 for all 30.

## Ranked by scripts broken

| # | construct | case | scripts | first wall in | clause |
|---|---|---|---|---|---|
| 1 | `test -x/-w/-r` answer from the mode bits, not from access(2) as this process; `-L`/`-h` never true; `-ef` never true | `builtin/test_access` | **14** | ltmain.sh, git-test-lib, git-t0000-basic, deb-openssh-server.postinst, deb-ca-certificates.postinst, deb-libc6.postinst, deb-libc6.preinst, deb-tzdata.postinst (via debconf's `confmodule`), deb-base-files.postinst (`-L`), init-rsync, init-ssh, init-procps (via `/lib/init/init-d-script`, inferred from the aided pass), service, which.debianutils | XCU `test` |
| 2 | `umask` not implemented (status 2, "not supported yet") | `builtin/umask_set` | **9** | install-sh, config.guess, mkinstalldirs, deb-openssh-client.postinst, deb-tzdata.postinst, lesspipe, and configure-hello/-sed/-gzip through `build-aux/config.guess` | XCU `umask` (a regular built-in pelt answers for itself) |
| 3 | `trap ACTION 13` (a number with no wolf meaning) refused, status 1, "no such condition" | `signal/trap_by_number` | **7** | config.guess, test-driver, ylwrap, tap-driver.sh, configure ×3 (`trap … 1 2 13 15` and `for ac_signal in 1 2 13 15`) | XCU 2.15 `trap` (XSI numbers); wolf-lang#679, #423 |
| 4 | a bracket expression containing `/` never matches in `case` or `${x#…}` | `glob/bracket_slash_case` | **4** | configure-hello, -sed, -gzip (first wall: `[\\/$]* \| ?:[\\/]*` for `--bindir`, "expected an absolute directory name"), ylwrap (`*[\\/]*` → `./fakeyacc: not found`, 127) | XCU 2.14.1 (2.14.3's slash rule is pathname expansion only) |
| 5 | in `$( exec 4>&1; { … >&4; } \| cmd >&3 )` the stage's write to fd 4 is lost | `redir/cmdsub_fd_pipeline` | **3** | xzgrep, zgrep, zdiff (the decompressor's status comes back empty: `test: : an integer is required`) | XCU 2.7.5, 2.12 |
| 6 | unquoted `$*` in an assignment / `case` word joins with nothing, not IFS's first char | `param/star_assign_ifs` | **3** | configure-hello, -sed, -gzip (`host_os=$*` under `IFS=-` → `linuxgnu`; `*-gnu*` and `linux*-gnu*` host checks take their default arms: "guessing no" ×2 and two extra checks in hello/sed, "time() works… guessing yes" in gzip) — reached only once 1–4 are aided | XCU 2.5.2 |
| 7 | bytes ≥ 0x80 become `?` in arguments to programs, file names, `read`, here-documents | `quote/high_bytes` | **1** | update-ca-certificates (a certificate named `…F\xc5\x91tan\xc3\xbas\xc3\xadtv\xc3\xa1ny.crt` is "not found" and left out of the bundle) | XCU 2.2 (only NUL excluded) |
| 8 | `.` of a file that is not regular (`/dev/null`, a FIFO, `/dev/stdin`) is "not found", ending the shell with 2 | `builtin/dot_special_file` | **1** | pfetch (`. "${PF_SOURCE:-/dev/null}"`) | XCU 2.15 dot |

No script hung (timeouts 120 s; configure 600–900 s), and none showed a
pelt crash, trap message or signal death.

## The answers, per case (dash / bash --posix / pelt)

`|` separates output lines; `[exit N]` the status.

**builtin/test_access** — as user mfwolffe on kasumi, non-root:
- dash: `plain r=y w=y x=n L=n-|prog r=y w=y x=y L=n-|secret r=n w=n x=n L=n-|ro r=y w=n x=n L=n-|dir r=y w=y x=y L=n-|link r=y w=y x=n L=y|/usr/bin/env r=y w=n x=y L=n-|/nonexistent r=n w=n x=n L=n-|ef: same file|ef: different files|env is a program|[exit 0]`
- bash: identical to dash.
- pelt: `plain r=y w=y x=n L=n-|prog r=y w=y x=n L=n-|secret r=y w=y x=n L=n-|ro r=y w=y x=n L=n-|dir r=y w=y x=y L=n-|link r=y w=y x=n L=n-|/usr/bin/env r=y w=y x=n L=n-|/nonexistent r=n w=n x=n L=n-|ef: different files|[exit 0]`
  — `-x` false for every executable regular file (a directory is
  searchable), `-w`/`-r` true for any existing file, `-L`/`-h` false for
  a link, `-ef` false for two names of one file. The oracle row is
  user-dependent (root reads a mode-000 file): record it as a user.
  Also seen, not in a script: `test -k` is "unknown operator" (status
  2); dash answers 1.

**builtin/umask_set**:
- dash: `0027|u=rwx,g=rx,o=|drwxr-x---|-rw-r-----|-rw-------|-rw-r-----|0027|u=rwx,g=rx,o=r|[exit 0]`; bash identical.
- pelt: `drwxr-xr-x|-rw-r--r--|-rw-r--r--|[exit 2]` and on stderr
  `umask: not supported yet (no umask builtin in wolf 0.2.24)` (the
  message names a wolf version two releases old). s230's `os_umask` is
  merged on wolf-interp and held on wolf-lang for its rebase (wave-53):
  this waits on the release after 0.2.27.

**signal/trap_by_number**:
- dash: `set: 0|ignore: 0|trap -- '' ALRM|trap -- 'echo caught' HUP|trap -- 'echo caught' INT|trap -- 'echo caught' PIPE|trap -- 'echo caught' TERM|reset: 0|bye|[exit 0]`; bash identical.
- pelt: `set: 1|ignore: 0|trap -- '' ALRM|trap -- 'echo caught' HUP|trap -- 'echo caught' INT|trap -- 'echo caught' TERM|reset: 1|bye|[exit 0]`, stderr `trap: 13: no such condition` (twice).
  Note pelt accepts `trap '' 14` and `trap … PIPE` by name, and HUP/INT/
  TERM by number, but not 13 by number: an inconsistency inside pelt,
  separable from wolf-lang#679 (recording the action is pelt's; catching
  it is #679's). Every script in the set that writes `13` only needs
  the action recorded and the signal never comes, so recording alone
  would clear all 7.

**glob/bracket_slash_case**:
- dash: `/abs: absolute|rel: plain|./rel: has a separator|a\b: has a separator|$var/x: absolute|c:/dos: absolute|bracket matches slash|negated bracket matches slash|local/bin usr/local bin usr|[exit 0]`; bash identical.
- pelt: `/abs: plain|rel: plain|./rel: plain|a\b: plain|$var/x: plain|c:/dos: plain|no match|negated bracket matches slash|usr/local/bin usr/local/bin usr/local/bin usr/local/bin|[exit 0]`
  — a negated bracket (`[!x]`) does match `/`; a positive one holding
  `/` never matches, in `case` and in all four `${x#…}` forms. Likely
  sh04's "a word is a glob pattern only with a closed bracket
  expression" or the pathname rule applied outside pathname expansion
  (inferred; pelt's source not read for this).

**redir/cmdsub_fd_pipeline**:
- dash: `status=[1]|status=[seven]|data|status=[eight]|[exit 0]`; bash identical.
- pelt: stdout `1|status=[]|seven|status=[]|data|status=[eight]|[exit 0]`
  — the write to 4 from a pipeline stage lands on the shell's own
  standard output instead of the substitution; from the last stage of
  `{ cat; echo eight >&4; } >&3` it works. Inferred tie to pelt's
  in-process pipeline stages (no fork; tests/diff/PENDING.md).

**param/star_assign_ifs**:
- dash: `[x86_64] [pc] [linux-gnu]|[a:b:c] [a:b:c]|case word joined|[exit 0]`; bash identical.
- pelt: `[x86_64] [pc] [linuxgnu]|[a:b:c] [abc]|case word not joined|[exit 0]`.

**quote/high_bytes** (the `od -c` dumps):
- dash: `303 251|c a f 303 251|F 305 221 t|F 305 221 t|x 303 251 y \n|n 303 251 \n|n 303 251|a 377 b|2|[exit 0]`; bash identical.
- pelt: `? ?|c a f ? ?|F ? ? t|F ? ? t|x ? ? y \n|n ? ? \n|n ? ?|a ? b|2|[exit 0]`
  — the same with LC_ALL=C, C.UTF-8, en_US.UTF-8 and unset; valid UTF-8
  is mangled too, so it is not an invalid-UTF-8 fallback alone. pelt's
  own `printf '%s'` of the value keeps the bytes and the byte length
  (`${#e}` is 2) is right: the loss is where a pelt string becomes
  bytes for the host (an argument vector, a path, a here-document
  body, `read`'s input). Inferred: wolf `str` boundaries at
  `os_spawn_fds`/`os_exec` argv, `fs_*` paths, or pelt's own
  conversion; a witness at the wolf level is owed (see the report).

**builtin/dot_special_file**:
- dash: `dev null: 0|from the fifo|fifo: 0|[exit 0]`; bash identical.
- pelt: `[exit 2]`, stderr `.: /dev/null: not found`.

## Per script

`scripts.tsv` has the full table (id, group, package, version, sha256,
licence, dash exits, pelt exits, verdict, notes). The 30 that differ,
with the construct(s) (first first):

| script | constructs |
|---|---|
| configure-hello, configure-sed, configure-gzip | 4, 3, 2 (config.guess), 6 |
| install-sh | 2 |
| config.guess | 3, 2 |
| mkinstalldirs | 2 (stderr only; the directory is made) |
| test-driver, tap-driver.sh | 3 (stderr only) |
| ylwrap | 3, 4 |
| ltmain.sh | 1 (`func_executable_p`: "no acceptable sed could be found") |
| git-test-lib, git-t0000-basic | 1 (`bin-wrappers/git is not executable`; "Bail out! You need to build test-tool") |
| deb-openssh-server.postinst, deb-ca-certificates.postinst, deb-libc6.postinst, deb-libc6.preinst | 1 (debconf's `confmodule`: `[ -x /usr/share/debconf/frontend ] && [ ! -h … ]` false, so it `exec`s the absent cdebconf: 127) |
| deb-tzdata.postinst | 2, 1 |
| deb-openssh-client.postinst | 2 |
| deb-base-files.postinst | 1 (`-L`: `rmdir: failed to remove '/var/run': Not a directory`, and the wrong links made) |
| init-rsync, init-ssh | 1 (`test -x $DAEMON \|\| exit 0`: the script exits 0 silently) |
| init-procps | 1 (inferred: cleared in the aided pass once `/lib/init/init-d-script` was rewritten) |
| service | 1 |
| which.debianutils | 1 (finds nothing) |
| update-ca-certificates | 7 |
| pfetch | 8 |
| xzgrep, zgrep, zdiff | 5 |
| lesspipe | 2 (stderr only) |

## The set, and what was not run

- 80 scripts: 4 configure (hello 2.12.2, sed 4.9, gzip 1.14, zlib
  1.3.1), 13 automake 1.18.1 / libtool 2.5.4 helpers, 2 git 2.56.0 test
  rows, 17 Debian 13 maintainer rows (dpkg-maintscript-helper among
  them), 7 Debian init rows, 16 Alpine 3.22 rows (11 package scripts, 5
  alpine-conf tools), 21 small `#!/bin/sh` utilities.
- **git's test library**: `t/test-lib.sh` has no shebang (it is sourced
  by `#!/bin/sh` test files) and `shellcheck -s sh` reports 90 findings
  on it, but it runs under dash (our 4-test file passes and
  `t0000-basic` passes under dash 0.5.13.4) — so it counts as "runs as
  sh". git was built in the image with `NO_RUST=1 NO_PERL=1 NO_PYTHON=1
  NO_TCLTK=1 NO_OPENSSL=1 NO_CURL=1 NO_EXPAT=1 NO_GETTEXT=1` (no cargo
  in the image). Under the aided pass `git-test-lib` passes under pelt.
- **shellcheck**: `shellcheck -s sh` 0.10.0 (Debian image) was run over
  every `#!/bin/sh` file in the Debian image. The utility rows include
  the 10 clean ones that do something without a network or a terminal
  (gunzip, zcat, zcmp, zforce, uncompress, ssh-copy-id, ssh-argv0,
  select-editor, sensible-editor, sensible-pager): **all 10 same** in
  the final run (zcat was `unstable` — dash disagreeing with itself —
  in one earlier run). Also in the set, deliberately, everyday
  `/bin/sh` tools shellcheck does not pass (which, savelog, add-shell,
  gettext.sh, xzgrep, xzdiff, zgrep, zdiff, lesspipe, xdg-mime) and
  pfetch 0.6.0 (not shellcheck-clean either: exit 1 under 0.10.0).
  Of the 17 Debian maintainer rows, 8 are shellcheck-clean (cron, rsync and openssh-client postinst, openssh-server prerm, procps, util-linux postinst, base-passwd and adduser preinst): 7 same, openssh-client.postinst differs (umask).
- Alpine's busybox and dash package scripts are `#!/bin/busybox sh` and
  `#!/usr/bin/dash`; they are in the set but run as `sh SCRIPT`, which
  is how the census runs everything (counted, said here).
- **Oracle drift**: the containers' dash is not the corpus's 0.5.13.4:
  Arch rows (configure, helpers, git) use dash **0.5.13.4-1** (same
  release as the oracle); Debian rows use **0.5.12-12**; Alpine rows
  **0.5.12-r3** (Debian and Alpine have no 0.5.13). Every construct
  above was re-checked against kasumi's 0.5.13.4 (the `tri` runs).
