# sh26 — the census after the fork, and the corners (pelt#6, #16, #17, #28, #56, #61, #63, #65)

Contract: `sprints/pelt/26-the-corners/sh26-the-corners.md` in the
planning repo (Opus 5.5, crawl 54, 2026-10-24). This file is the lane's
record: §1 to §3 are committed before the first change under `src/`,
`tools/` or `tests/`; the rest is filled in as the work lands. The raw
evidence is under `notes/sh26-evidence/`.

## 1. Forbidden

As the contract and `sprints/RULES.md` §1–§10 say. No shell's source is
read or searched for (dash, bash, busybox, mksh or any other), nor a
libc's or a kernel's (ruling #43). Behaviour comes from POSIX.1-2024 XCU
chapter 2 and the utility pages, dash's and bash's manuals as
documentation, and black-box runs of dash 0.5.13.4 and `bash --posix`
5.3.20 inside this lane's container. A disagreement with dash is a STOP
with the diff, never an expectation edited to fit; a case dash answers
inconsistently is `R-sh26-N`; R-sh20-1 is decided (copy dash's `jobs`
text); ruling #123 governs a data-loss case should one appear. The pin
stays wolf 0.2.35 / lupin 0.1.56 / std `2386522e`; no behaviour change
outside the items; no performance change (pelt#57 is measured only).
Builds, the corpus, the sessions, the censuses and every measurement run
on kasumi on CPUs 0–3 only, under `flock ~/lanes/kasumi-cores-0-3.lock`
and `taskset -c 0-3`, inside this lane's own rootless container
(`notes/sh26-evidence/ctr.sh`), `ulimit -c 0`; nothing is built or run on
nomad. No merge, tag, label, issue filed or closed; no attribution
trailers; nothing under `~/.claude` or the planning repo; kill by
recorded pid only. If the harness refuses an action, the lane stops and
reports.

## 2. Inputs, verified (2026-10-24, before any change)

| input | contract says | measured | drift |
|---|---|---|---|
| pelt trunk | `70eec14` (r40p, the 0.2.35 pin) | `origin/trunk` = `70eec1437d04859504cae3d1382c7b51292cf2eb` ("Pin wolf 0.2.35"); branch `sh26` cut from it in `~/lanes/sh26/pelt` on nomad (editing only) and a clone at the same commit in `~/lanes/sh26/pelt` on kasumi | none |
| the pin | wolf 0.2.35 / lupin 0.1.56 / std `2386522e` | `wolf-toolchain.toml`: wolf 0.2.35 `cf0c13d3` (the tag's commit, read in the org checkout), lupin 0.1.56 `28547b43`, std `2386522e`; the release API (wolf-lang release 421613621, wolf-interp 421458363) gives linux x86-64 `4cc4045b…dad1a` and `ad703550…22cc`, the pinned digests; `tools/fetch-toolchain` on kasumi re-hashed both OK and staged std `2386522e`; `wolf --version` line 1 `wolf 0.2.35 (wolfgang, pin cf0c13d)` | none |
| the oracles | dash 0.5.13.4, bash 5.3; "the pinned `ubuntu:24.04` container" in the Inputs line | kasumi's `/usr/bin/dash` sha256 `c6221703b619…e855` (pacman `dash 0.5.13.4-1.1`), `/usr/bin/bash` `a8ce2b3c38c8…95f5` (`bash 5.3.20-2`): `tests/diff/ORACLE`'s two, run read-only from the host's `/usr` inside `docker.io/library/archlinux:base-devel` (image id `3ed18d5c7b24…297f`, digest `sha256:8185e444…0fa785`) | the contract's Inputs line names an `ubuntu:24.04` container; Ubuntu 24.04 ships no dash 0.5.13. The oracle of record is `tests/diff/ORACLE`'s, as the brief says (the Arch black-box container) |
| the four numbers | 519 of 548; 998 / 0 / 25; 290 sessions; 76 of 80 before the fork | README and CENSUS §5 say the same; re-measured in item 1 (§4) | — |
| the script census | xzgrep, zgrep, zdiff waited on a process per stage | sh20's `logs/zgrep/zgrep.txt`: the post-fork pelt answers the three's six shapes as dash does, the pre-fork pin did not | — |
| pelt#28 | three leftovers | sh24 (pelt#58) fixed `trap -x` (fatal in a script) and the non-EPIPE built-in write; the issue's comment says the coin remains. Items 4's texts and statuses are still to be measured against dash | two of three already done: item 4 measures and pins them |
| pelt#16 | the corners | sh25 (pelt#62) did `pwd -x`, `cd -P -e` and `printf %d 12x`; the rest open | three already done: measured again only |
| pelt#17 | the corners | sh20 did `$(trap)`, sh18 `-o notify` (`option/c_long_names`); the rest open | two already done |
| `os_spawn_fds` / `os_exec` | — | spec `11-os.md` at `cf0c13d`: `os_spawn_fds(exe: str, args: List[str], map)`, `os_exec(str, List[str], List[str], List[int])`; std `2386522e`'s `std.process` keeps `argv: List[str]`; no builtin takes an argv or an environment as `List[byte]` | — |
| kasumi | 63 GB free | 63 GB free on `/home`, load 1.2 at the start, cores 0–3 lock free; sh28 in its own container on 12–15 | — |

## 3. Prediction (committed before the first change)

1. **The script census at the pin, before any change: 79 of 80 run as
   under dash.** xzgrep, zgrep and zdiff move from `differs` to `same`
   (sh20's fork gives each stage its process; sh20's probe already
   answers them as dash). The eightieth is `pfetch`, `unstable` (dash
   disagrees with dash on its memory-in-use line). `configure-sed` is
   `same` in most passes and `differs` in about one in eight on its
   timestamp-resolution line (sh14's coin), so a single pass prints 79
   or 78. No script hangs, none crashes pelt; the aided pass gives the
   same verdicts. With the coin mechanism (item 1): `configure-sed`
   counted apart as a coin, so 78 same, 1 coin, 1 unstable, and no pass
   prints a different count.
2. **The coin's flip rates** (sh14's `ts.sh`, the check alone, 300 runs a
   shell, in the container on CPUs 0–3): dash sees the second file newer
   at the first look in 9–15% of runs (sh14: 34–35 of 300), pelt in
   15–28% (sh14: 51–73), at the pin and at the head alike: the window
   between the two writes holds no fork, so sh20 does not move it. The
   300-run measurement takes under five minutes a shell, so it is not
   detached.
3. **The corners: of the fourteen #16/#17 name, dash answers twelve as
   POSIX.1-2024 reads them** (`command` with a special built-in's error,
   `export --`, `printf --`, `exit` in an `EXIT` trap, `readonly -p` of
   an unset readonly, `pwd -x`, `PWD` from the environment, `PS4`
   expanded, the `set -x` forms, `-o notify`, `ignoreeof`, `MAIL`). The
   two it does not are the two new in 2024 that dash lacks: `cd -e` and
   `trap -p` (both already take `bash --posix` as their recorded oracle,
   as sh06 and sh25 found). No corner is a dash self-contradiction, so no
   `R-sh26-N` comes from them.
4. **Item 2:** a slashed path that does not exist is dash's `not found`
   with 127 on the plain-command path already in a script; the
   "cannot be run" of pelt#61 is the interactive autocd fall-through,
   which answers 126. A `#!`-less text file already runs as a script on
   the plain path (`start_child`'s ENOEXEC fallback), so #63 is a case
   and a statement, not a fix; a binary garbage file is 126 under
   pelt and under dash (`simple/c_enoexec_binary`, recorded 126 from
   dash), so that case leaves `PENDING.md` without a source change.
5. **Item 3, `set -v`:** dash echoes each line of a script operand as the
   parser reads it, a here-document's body included, and a `-c` string
   once, whole, when `-v` is on at start; pelt writes nothing. One
   echo point in the reader closes both cases.
6. **Item 4:** `trap -x` ends a script with status 2 and the write
   errors answer 1 under both shells, as sh24 left them; the texts
   differ only in the prefix pelt writes before every message.
7. **Item 6:** dash's `jobs` line for `FOO=bar &` is the job's number,
   state and an empty command; `sh20`'s pending session turns green.
8. **Item 7, `$'\377'`: it cannot leave pelt on this pin.** pelt's words
   are `str` from the lexer to the argv, and `os_spawn_fds`/`os_exec`
   take `List[str]`, a UTF-8 type (`str_from_utf8`'s `utf8` row); a
   `List[byte]` word would have to replace `str` through expansion,
   field splitting, the built-ins and the spawn, and the spawn has no
   byte form. The case stays pending on wolf-lang#687 and #912 (no byte
   path or byte argv), and pelt stops writing `?`: a `$'…'` whose bytes
   are not UTF-8 is refused with a message naming the gap.
9. **The statements: 519 → 532 of 548** — the thirteen pending
   statements the items name (2.5.3/12, 2.5.3/13, 2.8.1/4, 2.9.1.6/3,
   exit/3, export/4, readonly/2, set/16, set/17, trap/7, sh/17, sh/21,
   printf/9) all met; the nine left are `~login`, `test -s` on btrfs,
   `-O`/`-G`, `printf %e %f %g`, the four `ulimit` ones and 2.2/1 (non-UTF-8
   bytes). New statements this lane adds (if any) are met.
10. **The corpus and sessions at the pin: 998 / 0 / 25 and 290 / 0 / 2 on
    both tiers**, as r40p left them; after: every pending case the items
    name green, the pending count down to 9 (corpus) and 0 (sessions),
    0 failing.
11. **pelt#57's bench at the pin**: within 10% of sh20's table (forked
    shapes 1.3–2.1× dash release, 2.0–3.0× native; `configure-shaped`
    about 1.5× release).

### 3.1 The prediction, scored

| # | predicted | measured | verdict |
|---|---|---|---|
| 1 | scripts at the pin 79 of 80, a pass printing 79 or 78 (`configure-sed`'s coin), `pfetch` unstable; with the coin: 78 same, 1 coin, 1 unstable | at the pin 78 same, 1 differs (`configure-sed`, its coin line 0.1 against 0.2), 1 unstable (`pfetch`); at the head 78 same, 1 coin, 1 unstable | held |
| 2 | flip rates: dash 9–15%, pelt 15–28%, the pin and the head alike | dash 8.7% and 12.7%; pelt 6.7% and 8.0%; the pin and the head alike | dash held; **pelt missed** (it now flips less than dash) |
| 3 | dash answers 12 of #16/#17's 14 corners as POSIX reads them; the two not, `cd -e` and `trap -p`; no corner a dash self-contradiction | **10 of 14**: also `ignoreeof` (dash leaves after fifty messages, and applies it to scripts) and `MAILCHECK` (ignored); and pelt#56's job text is a self-contradiction (R-sh26-3) | **missed** by two |
| 4 | a slashed missing path already dash's `not found` 127 in a script; #61's `cannot be run` the interactive autocd path's; #63 a case, not a fix; a binary 126 under both | ENOENT held; **missed**: the autocd path says `not found` on Linux too (#61's answer came from PAX's spawn), and ENOTDIR, ELOOP and ENAMETOOLONG were 126 where dash says 127; the plain path held (the runtime's `/bin/sh`), **missed** for `exec`, which ran pelt itself; the binary is 126 only where `/bin/sh` is bash (R-sh26-1) | mixed |
| 5 | `set -v`: a script per line, here-documents included; a `-c` string once, whole | the script held; **missed**: dash never writes a `-c` string | half |
| 6 | `trap -x` and the writes as sh24 left them, the texts parting only in the prefix | the statuses held; **missed**: the phrases parted (`no such option`/`Illegal option`, `write error`/`I/O error`, `bad`/`Bad`) | half |
| 7 | `FOO=bar &`'s job line: number, state, empty command | held in a fresh shell; **missed**: dash leaves every assignment out (`a=1 sleep` is `sleep`) and writes stale bytes after other commands | half |
| 8 | `$'\377'` cannot leave pelt; pending on #687/#912; refused, not `?` | held; dash's `\xff` is c3 bf (a code point), and dash dies on `$'\342\202\254'` | held |
| 9 | statements 519 → 532 of 548 | 532 of 548 | held |
| 10 | 998/0/25 and 290/0/2 at the pin; after, pending down to 9 and 0 | the pin held; after 15 corpus pending (13 not this lane's, 2 new for #65) and 0 sessions | half (the 9 was miscounted) |
| 11 | the bench within 10% of sh20's table | every ratio within 2–9% of sh20's (forked shapes 1.40–2.12 release, 1.98–3.28 native; configure-shaped 1.47) | held |

## 4. What was measured

All on kasumi, CPUs 0–3 under `flock ~/lanes/kasumi-cores-0-3.lock`,
inside this lane's container (`notes/sh26-evidence/ctr.sh`: rootless
podman, `--cpuset-cpus 0-3` and `taskset -c 0-3` inside, `ulimit -c 0`,
`--network none`, kasumi's `/usr` read only); the script census's own
containers through `podman-03` (a private store, `--cpuset-cpus 0-3`).
**crun resets the affinity a container is started with** (measured: an
outer `taskset -c 0-3` left the container's processes on 0–15), so the
first base run, started that way, was stopped by its container id after
two minutes and every later job binds the cpuset; the stopped run's
partial status is kept (`logs/base-allcores-killed.status`).

### 4.1 The four numbers

| measure | at the pin (`70eec14`) | at the head |
|---|---|---|
| POSIX statements met (`tools/clause-census`) | **519 of 548** (22 pending, 2 gap, 5 untestable) | **532 of 548** (9 pending, 2 gap, 5 untestable) |
| differential corpus, native and release | **998 pass / 0 fail / 25 pending** (2 PEND-ok) on each tier | **1,023 / 0 / 15** (1 PEND-ok) on each tier: 15 new cases, 12 pending cases cleared, 2 new pending |
| sessions, native and release | **290 / 0 / 2** on each tier | **295 / 0 / 0** on each tier: 3 new, both pending cleared |
| real scripts (`tools/script-census`, unaided) | **78 same, 1 differs, 1 unstable of 80** (trunk's tool; the one `differs` is `configure-sed`'s coin line, 0.1 against dash's 0.2; the `unstable` is `pfetch`) | **78 same, 1 coin, 1 unstable of 80** (the head's tool on the head's static build, `logs/sc-head-unaided.log`): `configure-sed` counted apart as a coin (that pass dash, dash again and pelt all printed 0.2), `pfetch` unstable as before; no script differs, none hangs |

**76 → 78 of 80, and 79 of 80 but for the coin.** xzgrep, xzdiff,
zgrep and zdiff are `same` at the pin (sh20's fork gave each stage its
process); the two left are not pelt's to fix: `configure-sed`'s
timestamp-resolution line is a coin (§4.3), and `pfetch`'s memory-in-use
line differs between dash's own two runs (the tool calls the row
`unstable` and compares the status and standard error only).

### 4.2 The corners, one by one

dash's answer is measured in this container, black-box
(`notes/sh26-evidence/probe/pNN-*.sh`, run by `probe/run.sh` under dash,
`bash --posix` and pelt; the interactive ones through `probe/pty.py`).
"Before" is pelt at the pin, "after" the head.

| corner | dash 0.5.13.4, measured | pelt before | pelt after | case |
|---|---|---|---|---|
| a slashed path that does not exist (pelt#61) | `not found`, 127; a link loop and a too-long name the host's words, 127; a directory, a file without x, an unsearchable directory `Permission denied`, 126 (`p01`, `p07`, `p21`) | `not found` 127 for ENOENT, but **126** and `cannot be run` for ENOTDIR, ELOOP, ENAMETOOLONG; `cannot be run` for the 126s | dash's words and statuses (the reason asked of the file: the os family sets no `os_error()` at 0.2.35) | `simple/cannot_run_reasons` |
| a `#!`-less executable (pelt#63) | run as `/bin/sh FILE ARG…`, the plain command, through `PATH` and after `exec` (`p06`, `p20`); a binary handed over too (`p02`) | the plain path the same (wolf 0.2.35's spawn still runs `/bin/sh` itself, wolf-lang#682's fix is in no release); **`exec` ran pelt itself** | both paths `/bin/sh`, as dash (R-sh26-1) | `simple/no_shebang_plain`, `simple/c_enoexec_binary` (rewritten) |
| `set -v` (pelt#6) | a script's lines as read, comment and blank lines, every line of a compound command and a here-document, a sourced file's; never an `eval` or a `-c` string (`p14`, `p15`) | nothing for a script | as dash | `option/c_verbose`, `option/c_verbose_stderr`, `option/verbose_forms`, `option/verbose_inputs` |
| `trap -x` (pelt#28) | `trap: Illegal option -x`, the script ends, 2 (`p03`) | ends, 2, `trap: -x: no such option` | dash's words | `builtin/trap_bad_option_text` |
| a built-in's failed write (pelt#28) | `echo: echo: I/O error`, 1, for a closed standard output, a full device, a read-only descriptor; `3: Bad file descriptor`, 2, for a redirection to a closed one (`p04`, `p22`) | statuses as dash, `write error` | dash's words | `builtin/write_error_text` |
| `command . missing`, `command set -o bad`, `command exec 3</x` | each 2, the script goes on (`p08`) | the first ends the shell | as dash | `builtin/c_special_error_command` |
| `export -- n`, `printf -- fmt` | `--` ends the options (`p08`, `p24`) | `--` an operand (`export` ended the shell) | as dash | `builtin/c_export_invalid`, `printf/c_usage`, `builtin/export_p_order` |
| `exit` in an `EXIT` trap | the status the shell was leaving with (`p08`) | the action's last status | as dash | `builtin/c_exit_in_trap_status` |
| `readonly -p`, `export -p` | every marked name in one sorted list, an unset one as `readonly b` (`p24`) | an unset readonly left out; an unset exported name listed after the set ones | as dash | `builtin/c_readonly_p`, `builtin/export_p_order` |
| `pwd -x`, `cd -e` | `Illegal option`, 2, for both: dash has no `cd -e` (`p08`) | sh25's: `pwd -x` 2, `cd -e` taken (POSIX.1-2024, bash the case's oracle) | unchanged | sh25's cases |
| `PWD` from the environment | kept when it names the directory with no dot component | always the physical directory | as dash | `cd/c_pwd_from_env` |
| `trap -p` | none: `Illegal option -p` (`p09`); bash lists | refused | bash's form (POSIX.1-2024; dash lacks it, sh06's rule) | `signal/c_trap_p` (written to a file, not a pipe: `p28`), `signal/trap_p_forms` |
| `PS4` | expanded: parameters, arithmetic, command substitution untraced, `LINENO`; unset is no prefix (`p12`) | written as it stands; unset `+ ` | as dash | `option/c_ps4`, `option/ps4_forms` |
| `set -x` forms | an assignment-only command traced, values unquoted, after its substitutions; redirections not written (`p09`) | not traced | as dash | `option/c_xtrace_forms`, `option/xtrace_assign` |
| `-o notify` | `b` second in `$-` (`u b a C v x s m i I f e`), listed by `set +o` (`p11`, `p25`) | `b` after `x`; not in `set +o`, so `eval "$(set +o)"` lost it | as dash | `option/notify_ignoreeof_flags` |
| `ignoreeof` | interactive: one Ctrl-D answered fifty times with `Use "exit" to leave shell.`, then the shell leaves 0; in a script the same at its end (`p16`, `p11`); bash tells once per Ctrl-D and stays | accepted, did nothing | stays, dash's words once per end-of-file, leaves at the fifty-first (R-sh26-4); `I` in `$-` | `session:c_ignoreeof` (bash's transcript) |
| `MAIL`, `MAILPATH`, `MAILCHECK` | `you have mail` before the prompt when the mailbox is made or its modification time (seconds) moves, any size; checked before every prompt whatever `MAILCHECK` says; a `MAILPATH` `%` message runs past the colon that ends it (`p17`–`p19`) | nothing | dash's rule and words, POSIX's interval (default 600 s, 0 every prompt) and colon (R-sh26-5) | `session:c_mail`, `session:mail_path`, `session:mail_interval` (bash's transcript) |
| a job's text (pelt#56) | a simple command's assignments left out (`a=1 sleep 30` is `sleep 30`), a blank before every redirection; an assignment-only command empty in a fresh shell, **a stale or uninitialised text after other commands** (`p05`, `p10`, `p13`, `p23`) | the assignments kept | as dash where dash's text is defined (R-sh20-1, R-sh26-3) | `jobsctl/jobs_assign_text`, `session:jc_assign_text`, `src/sh/selftest.lu`'s rows |
| `$'\377'`, `$'\xff'` (pelt#65) | `\377` the byte ff; `\xff` U+00FF in UTF-8, c3 bf (bash: ff, POSIX's byte); `$'\342\202\254'` **kills dash with SIGSEGV** (`p26`, `p27`) | `?` (3f) | refused as an expansion error, status 2 (R-sh26-6); still pending on the byte path | `quote/c_ds_octal_high`, `quote/c_ds_hex_high` (pending), `quote/ds_split_utf8` |

Of the fourteen corners pelt#16 and #17 name, dash answers **ten** as
POSIX.1-2024 reads them; the four it does not are `cd -e` and `trap -p`
(new in 2024, absent from dash), `ignoreeof` (dash leaves at the end of
file after fifty messages, and applies the option to a script) and
`MAILCHECK` (ignored). None is a dash self-contradiction; the job text
of pelt#56 is (R-sh26-3).

### 4.3 The coin (pelt#28's third point)

`tools/script-census` gains `COIN(line, witness)` on a row: `line` is a
pattern for the standard-output line that flips for dash itself because
it measures the shell's own speed, `witness` the measurement alone, in
this project's words (`tools/census-coins/fs-timestamp-resolution.sh`,
sh14's `ts.sh`). A coin row's coin lines are compared apart; a row that
agrees everywhere else is `coin`, counted apart, **never `same`**, with
the three answers (dash, dash again, pelt) in its notes; any other
difference is still `differs`. `--coins N` runs no script: it runs each
coin's witness N times under dash and N under pelt in one container of
the row's image and writes the answers and each shell's flip rate (the
share of runs that are not dash's commonest answer) to `coins.tsv`.
`--selftest` checks the verdict rules on made-up runs (no podman); its
planted break is in §6. `configure-sed` is the one coin.

Measured with the head's tool, in one `sh06-arch` container a row
(`--network none`, CPUs 0–3), 300 runs a shell (`logs/sc-coins-*.log`,
`sc/coins-*.tsv`; about a minute each):

| pelt | dash: second file newer at the first look (configure says 0.1) | pelt: the same | load at the start |
|---|---:|---:|---:|
| the pin (`70eec14`, static) | 26 of 300, **8.7%** | 20 of 300, **6.7%** | 37.7 (other lanes, on other cores) |
| the head (`cf1e7cd`, static) | 38 of 300, **12.7%** | 24 of 300, **8.0%** | 14.8 |

So both shells flip, dash about one run in eight to eleven, and pelt
now *less* often than dash: sh14 measured pelt at 51–73 of 300 against
dash's 34–35, before sh15–sh25 made the shell's own work cheaper. The
pin and the head cannot be told apart (20 and 24 of 300).

### 4.4 pelt#65: `$'\377'` on this pin

**It cannot leave pelt.** A pelt word is a `str` from the lexer to the
program's argv, and `os_spawn_fds(exe: str, args: List[str], map)` and
`os_exec(str, List[str], List[str], List[int])` (wolf 0.2.35,
`spec/11-os.md` at `cf0c13d`; std `2386522e`'s `std.process` keeps
`argv: List[str]`) take UTF-8 strings by type: `str_from_utf8` refuses
the byte (`utf8`). `List[byte]` could carry the word through a
built-in's write (pelt's own `printf '\377'` writes ff), but not through
expansion, field splitting and the spawn, and the spawn has no byte
form; wolf-lang#687 (a byte path) and #912 (a byte-path open) are the
named gaps. So `quote/c_ds_octal_high` (dash: ff) and
`quote/c_ds_hex_high` (bash: ff; dash writes c3 bf, U+00FF in UTF-8)
stay pending under `non-utf8-bytes`, and pelt no longer writes `?`: a
run of `$'…'` side by side is decoded whole, and when its bytes are not
UTF-8 the word is refused as an expansion error, `pelt: …: $'\377': a
byte that is not UTF-8 cannot be carried yet (pelt#65)`, status 2, a
script ends (R-sh26-6). Witness: `probe/p26-ds-bytes.sh` (dash, bash,
the pin), the head's answer in `logs/probe-head/p26-ds-bytes.txt`.
`$'\303'$'\251'` is é (`quote/ds_split_utf8`).

### 4.5 pelt#57: the fork's cost at the pin (measured only)

sh20's bench (`notes/sh26-evidence/bench/`, sh20's scripts unchanged;
`configure-shaped.sh` generated again, sha256 `4f1f4096…`, sh20's) at
the pin, inside the container on CPUs 0–3, nine runs each, the median
(`logs/bench-pin.txt`; load 14.8 at the start, other lanes on other
cores; sh20's was 0.08). A turn is a loop's two thousand.

| loop | dash | pin release | ratio | pin native | ratio | sh20's ratios (release, native) |
|---|---:|---:|---:|---:|---:|---|
| `fork` (2,000 programs) | 0.336 s | 0.530 s | 1.58 | 0.583 s | 1.73 | 1.59, 1.74 |
| `pipeline` | 0.337 | 0.446 | 1.32 | 0.521 | 1.54 | 1.32, 1.51 |
| `param` (in process) | 0.361 | 1.778 | 4.93 | 7.540 | 20.90 | 5.08, 20.36 |
| `configure-shaped` | 0.341 | 0.503 | **1.47** | 0.665 | 1.95 | 1.48, 2.00 |
| forked shapes (`s-sub2`, `s-cmdsub2`, `s-bg-sub`, `s-bg-brace`, `s-func-pipe`, `s-stage-read`) | 82–128 µs a turn | **156–180 µs** | 1.40–2.12 | **211–278 µs** | 1.98–3.28 | 148–166.5 µs (1.33–2.06), 196.5–245.5 µs (1.97–3.00) |
| in-process shapes (`s-sub`, `s-cmdsub`, `s-cmdsub-echo`, `s-stage`) | 82–120 µs | 4.5–8 µs | 0.05–0.07 | 20.5–35.5 µs | 0.25–0.33 | — |
| a program (`s-program`) | 161.5 µs | 257.5 µs | 1.59 | 284.5 µs | 1.76 | — |

Within 9% of sh20's table on every row (most within 3%), at a higher load: the fork is
where it was. No performance change in this lane.

## 5. Rulings asked (each carried out as recommended meanwhile)

- **R-sh26-1, which shell runs a `#!`-less file the kernel refuses.**
  dash 0.5.13.4 runs `/bin/sh FILE ARG…` (argv[0] `/bin/sh`), on the
  plain path, through `PATH` and after `exec`, and hands a binary file
  over too, so its status for a binary is the host's `/bin/sh`'s (126
  where that is bash, 127 where it is dash: `probe/p02`, `p06`, `p20`,
  the second run with dash bound as `/bin/sh`). (A) copy dash: `/bin/sh`
  on both paths, no bypass; (B) pelt itself (`os_exe()`), as pelt#63
  asks and pelt's `exec` did, with the optional 126 bypass for a binary.
  **Recommended A**: byte-identical to dash on every host, and the same
  as B on PAX, where `/bin/sh` is pelt. At wolf 0.2.35 the plain path's
  spawn still runs `/bin/sh` itself (wolf-lang#682's fix, s260, is in no
  release), so A changes only `exec`'s fallback and is ready for the pin
  that brings s260. `simple/c_enoexec_binary` compares with `/bin/sh`'s
  own answer, green on every host.
- **R-sh26-2, dash's words in pelt's messages.** The contract asks for
  dash's text (`not found`, `Permission denied`, `Illegal option -x`,
  `echo: echo: I/O error`, `Bad file descriptor`, `Use "exit" to leave
  shell.`, `you have mail`); pelt's `CLAUDE.md` says "do not copy any
  shell's error text: write pelt's own". (A) dash's phrase after pelt's
  own prefix where a contract names it (done here), the rest pelt's own
  until a lane is given them; (B) dash's phrases everywhere (every
  built-in's bad option is `Illegal option -X` in dash, `no such
  option` in pelt); (C) pelt's own words everywhere. **Recommended A**
  now and B as its own lane, with `CLAUDE.md`'s sentence amended by the
  maintainer: the words are measured behaviour, not source, and a
  script that greps a message reads the phrase.
- **R-sh26-3, dash's job text for an assignment-only command.** R-sh20-1
  says copy dash. dash leaves every assignment out of a simple
  command's text, so `FOO=bar &` is an empty text in a fresh shell, but
  after other commands dash writes a stale text (`jobs`) or
  uninitialised bytes (`c0 58 d0 0b f0 55`) for `FOO=$(echo a) &`, and
  two identical commands in one script got two texts (`probe/p10` rows 5
  and 6, 9; `p13` repeated 20 times in a fresh shell: empty each time).
  **Recommended: empty**, dash's only defined answer; the corpus case
  holds no substitution row.
- **R-sh26-4, `ignoreeof`.** dash answers one Ctrl-D at a terminal with
  `Use "exit" to leave shell.` fifty times and leaves with status 0, and
  applies the option to a script's end (fifty messages on standard
  error); POSIX keeps an interactive shell, and bash tells once per
  Ctrl-D (`probe/p16`, `p11`). (A) POSIX's behaviour with dash's words,
  once per end-of-file, leaving at the fifty-first in a row, nothing for
  a script (done); (B) copy dash. **Recommended A.**
- **R-sh26-5, `MAIL`.** dash checks before every prompt whatever
  `MAILCHECK` says, and runs a `MAILPATH` message past the colon that
  ends its entry (`probe/p17`–`p19`). (A) dash's rule for what is new and
  dash's words, POSIX's interval (600 s by default, 0 every prompt) and
  colon (done); (B) copy dash. **Recommended A**: the session
  `mail_interval` takes bash, which honours `MAILCHECK`.
- **R-sh26-6, the refusal of a non-UTF-8 `$'…'`.** (A) an expansion error
  (XCU 2.8.1): said, status 2, a non-interactive shell ends, as for
  `${x?}` (done); (B) the one command fails, status 1, and the script
  goes on. **Recommended A**: a script that went on would act on a
  missing word (`rm -f -- $'\377'name`), and ruling #123's rule is to
  refuse and preserve rather than hand over wrong bytes.

## 6. Plants (every new gate seen red before green)

| gate | planted break | where | red | then green |
|---|---|---|---|---|
| the corpus (`set -v`'s four cases) | `verbose_to` writes nothing (`sh26-plant-diff` `32a3f96`) | CI, tier pr dispatch **40149165444** | `gauntlet (ubuntu-latest, true, native)` and `release`, step "the differential corpus": `FAIL option/c_verbose`, `c_verbose_stderr`, `verbose_forms`, `verbose_inputs`, `difftest: total 1019 4 15` on each tier (`logs/plants/red-40149165444.txt`) | the head, both tiers, kasumi (`logs/head2.status`) |
| the sessions (`MAIL`) | no mail check (`sh26-plant-session` `adc9ddb`) | CI, tier pr dispatch **40149166929** | step "the session corpus", both tiers: `FAIL c_mail`, `FAIL mail_path`, `session: pass 293 fail 2` (`logs/plants/red-40149166929.txt`) | the head |
| `MAILCHECK`'s interval | the interval ignored, a check before every prompt as dash does (local, kasumi, `plant-session` tree at `cf1e7cd` plus one line) | kasumi, CPUs 0–3, in the container | `FAIL mail_interval`, `! pelt err yes` (`logs/plant-mailcheck-local.log`) | the head |
| the table checks (`node_text`) and the job text cases | assignments kept in a job's text (`sh26-plant-selfcheck` `c9d89ce`) | CI, tier pr dispatch **40149168514** | steps "wolf test (the table checks)" and "the table checks", five `node_text(…)` rows; "the differential corpus" `FAIL jobsctl/jobs_assign_text`; "the session corpus" `FAIL jc_assign_text`, both tiers (`logs/plants/red-40149168514.txt`) | the head |
| `tools/script-census`'s verdict rules (the coin) | a coin row reported `same` (local copy of the head's tool) | kasumi, in the container | `script-census --selftest: 5 of 8`, the three coin rows `FAIL … same (want coin)`, exit 1 (`logs/census-selftest-plant.log`) | the head's tool 8 of 8 (`logs/census-selftest-head.log`) |
| the new and cleared cases | the pin itself | kasumi, the pin's native build | 22 corpus cases and 4 sessions red (`logs/red-at-pin-diff.log`, `red-at-pin-sess.log`); `no_shebang_plain`, `c_enoexec_binary`, `ds_split_utf8` and `mail_interval` pass at the pin, pinning answers the pin already gave as dash does | the head |

An unplanned red too: the first head (`1246d20`, `logs/head1.status`)
built two empty lists for every assignment-only command, and
`tools/shape-rss` caught it on `substitution-pipeline`,
`typed-substitution` and `script-fork-substitution` (`script-substitution`
22 → 152 B a turn native, `logs/head1/shape-*.log`); `cf1e7cd` builds the
trace only under `set -x`, and the final head is back at the pin's
numbers (19 B, `logs/head2/shape-native.log`). The plant dispatches
40149009674, 40149012706 and 40149016268 ran on the head before that
commit was fixed for W0308 and are red at the build: void, not cited.
The plant branches never merge.

## 7. Issues

**To close at the merge:** pelt#6 (`set -v`), pelt#16 (its corners:
`command` with a special built-in's error, `export --`, `printf --`,
`exit` in an `EXIT` trap, `readonly -p`, `PWD` from the environment;
`pwd -x`, `cd -e` and `printf %d 12x` were sh25's; `%e %f %g` stays
pending as `printf/c_floats`, its own corner — close #16 only if the
orchestrator files that one apart, else comment), pelt#17 (`trap -p`,
`PS4`, the `set -x` forms, `-o notify`, `ignoreeof`, `MAIL`; `$(trap)`
was sh20's), pelt#28 (`trap -x`, the failed write, the coin), pelt#56
(R-sh20-1), pelt#61, pelt#63 (R-sh26-1).

**To keep open, with a comment:** pelt#65 (the refusal landed; the
bytes wait on wolf-lang#687/#912 and W06), pelt#20 (the same gap for a
substitution's byte), pelt#57 (measured here, §4.5; sh27's).

**To file** (each with its witness under `notes/sh26-evidence/`):

1. pelt: `set +o` and `set -o` list neither `monitor` nor `nolog` (dash
   lists both, and `interactive`, `stdin`, `debug`), so `eval "$(set
   +o)"` does not put `-m` back. Witness `probe/p11-set-o.sh`.
2. pelt: `set -n` inside a script does not stop the commands after it:
   `(set -nb; echo "$-")` prints `bn` where dash prints nothing (XCU
   `set -n`). Witness `probe/p25-flags.sh`, row 8.
3. pelt: a `PATH` search that finds only a directory says `not found`
   where dash says `Permission denied` (127 both). Witness
   `probe/p07-exec-errnos.sh`, the `dir-on-path` row.
4. wolf-lang: the os family sets no `os_error()` (`os_spawn_fds`,
   `os_exec`), so a shell cannot name `ETXTBSY` (dash: `Text file
   busy`), `E2BIG` and the like from the call itself; pelt asks the file
   with `fs_stat`, which cannot see those. Witness
   `probe/wolf-spawn-errno/` (`./busy: spawn io os_error 0`).
5. pelt (if R-sh26-2 is B): every built-in's bad option in dash's words
   (`Illegal option -X`).
6. pelt (sh27's, drafted below): the fork's cost.

Not an issue of ours, recorded: **dash 0.5.13.4 dies of SIGSEGV** on a
script holding `$'\342\202\254'` (a three-byte UTF-8 character spelled
in octal), before running anything (`probe/p27-ds-crash.sh`, status 139);
bash and pelt write e2 82 ac.

## 8. sh27's draft: the fork's cost (pelt#57)

**sh27 — the fork's cost** (pelt#57; a pelt lane, Opus or Sol, kasumi
0–3, the 0.2.35 pin or the next). The numbers to beat are §4.5's: a
forked shape costs pelt 156–180 µs a turn on the release tier and
211–278 µs native, against dash's 82–128 µs (1.40–2.12× and
1.98–3.28×); `configure-shaped` is 1.47× (it was 1.03× before the
fork); a program started costs 1.59×.

1. **Measure where the child's time goes**, before any change: `strace
   -f -c` and `-ttt` of one forked `( true; true )`, `$(true; true)`, a
   `{ …; } | cat` stage and `( … ) &`, pelt against dash; `perf stat` of
   the loops; the parent's and the child's system calls apart (sh20 §3.8
   counted `clone`, `pipe2`, `rt_sigaction` 15,424 → 18,546 over the
   corpus, `getpid` 208 → 1,133). Prediction first: the child's
   disposition loop (`sig_apply` over every signal) and the descriptor
   closes dominate, not `clone` itself.
2. **Candidates, each a row of the bench and a session**: set only the
   dispositions that differ from the default in the child (a mask of
   what the parent changed); close only the descriptors the parent's
   table names; read the job table's state lazily; skip the parent's
   `flush` when nothing is buffered; for a pipeline stage that is a
   function or a compound command of programs, keep the fork (dash
   forks too) but start its programs with `os_spawn_fds` from the child
   without its own wait table. `os_fork` against a `posix_spawn`-shaped
   fast path is a wolf-lang question (a runtime spawn that runs a pelt
   closure is not on offer); file it, do not build it in pelt.
3. **Done when**: the forked shapes within 1.3× dash on release, the
   bench in the note before and after, `tools/shape-rss` and the
   corpus unchanged, no new system call name (PAX's list, sh20 §3.8).

## 9. Evidence index

Commits, in order (each item its own, the prose last):

- `9621f16` notes: sh26 forbidden, inputs and prediction
- `63dfb55` Count script-census coins apart and measure their flip rates (pelt#28)
- `f4b5327` Name why a command cannot run as dash does; hand a #!-less file to /bin/sh (pelt#61, #63)
- `78b947f` Write a script's input to stderr as it is read under set -v (pelt#6)
- `1e3ba3c` Report a built-in's failed write in dash's words (pelt#28)
- `d9ac7b9` Add trap -p; refuse a bad trap option in dash's words (pelt#17, #28)
- `48a78d2` Keep the shell after a special built-in's error under command (pelt#16)
- `fd47c15` Take -- in export, readonly and printf; list unset names in order (pelt#16)
- `73e36a9` Keep the leaving status for exit in an EXIT trap (pelt#16)
- `c28f23e` Take PWD from the environment when it names the directory (pelt#16)
- `ab907da` Expand PS4 and trace assignment-only commands under set -x (pelt#17)
- `01817f0` Take ignoreeof, notify and MAIL at the prompt as dash does (pelt#17)
- `ccd0a9c` Leave assignments out of a job's text, as dash (pelt#56, R-sh20-1)
- `767b7e8` Refuse a $'...' word that is not UTF-8 instead of writing ? (pelt#65)
- `1246d20` notes: sh26 black-box probes and the bench copy
- `cf1e7cd` Build an assignment's trace line only under set -x
- the prose: the note's results, `docs/CENSUS.md` §5 regenerated, `docs/CHANGELOG.md`, `docs/PLAN.md`, the README (a README-only commit), the evidence

Under `notes/sh26-evidence/`:

- `ctr.sh`, `launch.sh`, `gauntlet.sh`, `census.sh`, `podman-03`,
  `after.sh`: the container, the detached launcher (pid file, log, exit
  marker), the gauntlet (CI's linux steps, both tiers), the census
  runner and its cpuset-bound podman, the chain after the gauntlet.
- `probe/`: every black-box probe (`pNN-*.sh`), `run.sh` (dash, `bash
  --posix`, pelt; stdout, stderr and status, bytes escaped), `pty.py`
  (typed probes), `wolf-spawn-errno/` (what a failed spawn answers).
- `logs/base.status`, `logs/head2.status` (every gate, both tiers, at the
  pin and the final head), `logs/head1.status` and `logs/head1/shape-*`
  (an intermediate head whose assignment-only commands built two empty
  lists a turn: `shape-rss` red on `substitution-pipeline`,
  `typed-substitution`, `script-fork-substitution`; fixed in `cf1e7cd`,
  green in `head2`), `logs/base-allcores-killed.status`.
- `logs/sc-*.log`, `sc/*.tsv`: the script census at the pin (trunk's
  tool) and at the head (the head's tool), the coins' runs and
  `coins-*.tsv`.
- `logs/bench-pin.txt`: pelt#57's bench at the pin.
- `logs/probe-base/`, `logs/probe-head/`: every probe's answers at the
  pin and the head.
- `logs/red-at-pin-*.log`: the new and cleared cases against the pin's
  binaries (red), `logs/census-selftest-*.log`: the census's verdict
  rules, planted red and green.

## 10. Done-when

- [x] Prediction committed before the first change (`9621f16`).
- [x] Item 1: the four numbers at the pin (§4.1); the coin mechanism, its
  self-test seen red (§6) and its flip rates (§4.3).
- [x] Items 2–7: every corner measured against dash first (§4.2); each
  has its case, recorded from the oracle the case names; the census
  statements they close (519 → 532 of 548).
- [x] Item 8: pelt#57's bench at the pin (§4.5), no performance change.
- [x] Item 9: this note; the rulings asked (§5); the issues (§7); sh27's
  draft (§8).
- [x] Every gate seen red before green (§6): CI plant runs for the
  corpus, the sessions and the table checks; the census self-test
  locally.
- [x] Final gauntlet green at the head, both tiers (`logs/head2.status`).
- [x] README read and refreshed (counts, the census, the prompt's own).
- [ ] `tier pr` green at the head: read once at hand-back; the
  orchestrator watches and merges.

## 11. Prune list (after the merge)

On kasumi (`~/lanes/sh26`, about 3.2 GB at the hand-back):
- `sc/` (the census's private podman store, images and trees, ~2.2 GB):
  `podman --root ~/lanes/sh26/sc/store --runroot ~/lanes/sh26/sc/run-podman system reset -f`,
  then `rm -rf ~/lanes/sh26/sc` (the overlay files belong to sub-uids:
  `podman unshare rm -rf` for what is left);
- `pelt/.wolf-bin` (363 MB), `pelt/target`, `head/target`, `plant-*/`
  (three worktrees of the lane clone; `git worktree prune` after),
  `bin/` (the pin's, head1's and head2's builds), `bench/`, `tmp/`;
- then the lane clone itself, `~/lanes/sh26`.

On nomad: the worktrees `~/lanes/sh26/pelt` (after the merge) and
`~/lanes/sh26/plant`; the branches `sh26-plant-diff`, `sh26-plant-session`,
`sh26-plant-selfcheck` on origin (never merged).
