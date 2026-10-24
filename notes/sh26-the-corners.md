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
