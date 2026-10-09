# sh04 — the glob (pelt#3)

Contract: `sprints/pelt/04-the-glob/sh04-the-glob.md` in the planning
repo (`wolffe-lang/wolf`, trunk). This file is the lane's record: §2 is
written first, §3 is committed before the first change, and the
evidence index (§4) is filled in as the work lands.

## 2. Inputs, verified (2026-10-09, re-derived from origin)

| input | contract says | measured | drift |
|---|---|---|---|
| pelt trunk | `dd22a86` (sh02) | origin/trunk `dd22a86caf49…`; CI green there: push run 37685574742 | none |
| pins | 0.2.24 / 0.1.47 | `wolf-toolchain.toml`: `wolf 0.2.24 (wolfgang, pin 294d626)`, lupin `0.1.47`; fetched by digest on kasumi (`501d6d3f45124c84…` wolf, `0ddc4ff38d6178ae…` lupin, both OK) | none; sh03 owns 0.2.26 |
| corpus at trunk | (sh02: 244/0/19) | kasumi, `taskset -c 0-3`: native `244 0 19 (3)`, release `244 0 19 (3)`; `tools/check-test` rc 0 (`notes/sh04-evidence/base-dd22a86.log`, `d45081280e437b5c…`) | none |
| pelt#3 | open | OPEN, filed by s216 | none |
| where expansion decides to glob | — | `src/sh/expand.lu` `expand_words`: every field `has_magic` accepts goes to `glob`, which calls `fs_read_dir` once per magic path component and sorts the names. `has_magic` (`src/sh/pattern.lu`) answers true for ANY unquoted `[`, closed or not. The matcher already treats an unclosed `[` as an ordinary byte (`bracket_end` answers -1, `pmatch` matches it literally), so the read can never change a result: it only costs | the bug is exactly where s216 said |
| s216's RSS | 163→490 MB at 20,000 turns, empty vs 24 files, "how it measured them (`tools/session-rss`)" | s216 did **not** use `tools/session-rss`: its log (kasumi `~/lanes/s216/evidence/pelt2.log`, `355ce5b4c421fff0…`) and script (`~/lanes/s216/pelt2.sh`) run `pelt -c 'i=0; while [ $i -lt N ]; do i=$((i+1)); done; echo $i'` under `env -i`, `/usr/bin/time -f %M`, median of 3, built by wolf **trunk `a67c066`** (0.2.25+dev), not pelt's 0.2.24 pin. `tools/session-rss` types `x=$((x+1))`, which has no `[` and cannot see this bug. Re-taken on the pin with s216's method: release 162,852 KB (empty) and 489,608 KB (24 files) at 20,000; 323,128 / 977,092 at 40,000 (native within 0.1%) | method named wrongly in the contract; figures reproduce on 0.2.24 to 0.2% |

Black-box runs of `dash` 0.5.13.4 on kasumi (`env -i`, `LC_ALL=C`), in a
directory holding `[`, `]`, `[a`, `a]`, `\`, `a`, `b`, `x`: every edge
the contract lists answers the same from dash and from trunk's pelt —
`[`, `]`, `[ -f x ]`, `[a`, `a]`, `"["a]`, `[a"]"`, `\[a]`, `'['a]`,
`[]`, `[!]`, `[a/b]` and `x*[` stay themselves; `[!x]`, `[!a]`, `[]]`,
`[!]]`, `[a-]`, `["a"]`, `[\a]`, `[[:alpha:]]` match as bracket
expressions; `[[:alpha:]` is a literal `[` then the bracket expression
`[:alpha:]` (it matches `[a`). So the fix is invisible on standard
output; it is visible only as a directory read, which is what the
regression test counts. (Outside `LC_ALL=C`, dash under kasumi's
`LANG=en_US.UTF-8` sorts `*`'s names by the locale; with `LC_ALL=C` it
sorts by byte, as pelt does. The corpus runs in the C locale.)

The pattern clause: the contract cites XCU 2.13; pelt's `pattern.lu`
(sh01) cites the same text as XCU 2.14 of the 2024 edition. The rule
used is the one both name: a `[` that does not introduce a valid
bracket expression matches itself, and a `/` ends a bracket expression's
chance in pathname expansion.

## 3. Prediction (committed before the first change)

**The rule.** A field is a pattern, and pathname expansion reads a
directory, only when it holds an unquoted `*`, an unquoted `?`, or an
unquoted `[` for which `bracket_end` finds a closing `]` (quoted bytes
skipped, a leading `!`/`^` and a leading `]` taken as members,
`[:class:]` stepped over, a `/` ending the search). Every `[` in the
field is tried, not only the first (`[[:alpha:]` is a pattern through
its second `[`).

**Still glob (one directory read each):** `*`, `?`, `x*[`, `[!x]`,
`[]]`, `[!]]`, `[a-]`, `["a"]`, `[\a]`, `[[:alpha:]]`, `[[:alpha:]`.
**No longer read the directory:** `[`, `]`, the four fields of
`[ -f x ]`, `[a`, `a]`, `"["a]`, `[a"]"`, `\[a]`, `'['a]`, `[]`, `[!]`,
`[a/b]`. Standard output of every one is unchanged (identical to dash
before and after), so the new differential cases are green on trunk
and stay green; **the red is the directory-read count** (a table check
under `wolf test`) and the RSS gap between an empty directory and a
full one (an end-to-end check in CI).

**RSS at 20,000 turns** (s216's loop, release tier, kasumi, median of 3):

| directory | trunk (measured) | after (predicted) |
|---|---|---|
| empty | 162,852 KB | 135,000–155,000 KB (the empty directory's read, sort and lists gone, about 0.5–1.4 KB a turn) |
| 24 files | 489,608 KB | within 2% of the empty directory's figure |

The slope stays linear (about 7 KB a turn: wolf-lang#612's per-command
scratch, which this lane does not touch), so 40,000 turns is about twice
20,000. Falsified by: the 24-file run more than 2% above the empty one;
the empty run not below trunk's; any differential verdict moving.

## 4. Evidence index

Every log named here is committed under `notes/sh04-evidence/`, with its
sha256. Runs on kasumi (CachyOS linux x86-64, 16 cpus), wolf 0.2.24 /
lupin 0.1.47 fetched by digest, from a clean clone in `~/lanes/sh04/`.

**The fix** (`dfbe7ae`): `has_magic` answers true for a `[` only when
`bracket_end` finds its closing `]`; `glob` counts each directory it
lists in `Sh.dir_reads` (`9952adf`).

**Red, then green, on kasumi:**
- `witness-red-0f7b8cc.log` `03d4567e39fd9fe4…` — the tests on trunk's
  matcher: `wolf test` FAILS with 7 words that listed a directory (`[`,
  `[a`, `x[a`, `[a"]"`, `[]`, `[!]`, `[a/b]`); `tools/glob-rss` FAILS on
  both tiers (64 files 111,388 / 110,732 KB against 19,108 / 18,580 KB
  empty); the differential corpus 257/0/19 on both tiers (the 13 new
  cases pass on trunk, as §3 said). That head was also not `wolf fmt`
  clean (fixed in `fc293ae`).
- `witness-green-dfbe7ae.log` `571be5c2a16d350e…` — the fix: fmt clean,
  `wolf test` ok, `glob-rss` ok on both tiers (17,496 / 17,252 KB with
  64 files against 17,868 / 17,288 empty), differential 257/0/19 on
  both tiers.

**Red, then green, in CI** (linux x86-64 and macOS arm64, both tiers;
linux aarch64 asserts its refusals and is green throughout):

| head | what | run | result |
|---|---|---|---|
| `06642ab` | the tests and the CI step, trunk's matcher | 37950114998 | **red** on both hosts at `wolf test` (the same 7 words) and both `glob-rss` steps (linux 110,844 vs 18,492 KB native; macOS 110,976 vs 18,112) |
| `dfbe7ae` | the fix | 37950830381 | green |
| `83e8b83` | **PLANT**: any unquoted `[` magic again | 37951506549 | **red** on both hosts, the same three steps |
| `4a7acca` | the plant reverted (tree identical to `dfbe7ae` over `src tools tests .github`) | 37951656767 | green |

**RSS** (`rss-dd22a86-dfbe7ae.log` `b1c183810b52f7d8…`; s216's method:
`pelt -c 'i=0; while [ $i -lt N ]; do i=$((i+1)); done; echo $i'`,
`env -i`, `/usr/bin/time -f %M`, median of 3, KB; trunk `dd22a86` and the
fix `dfbe7ae` built in the same job):

| directory | tier | trunk 20,000 | fix 20,000 | trunk 40,000 | fix 40,000 |
|---|---|---|---|---|---|
| empty | native | 163,488 | 150,372 | 323,896 | 297,792 |
| empty | release | 163,124 | 149,896 | 323,468 | 297,200 |
| 24 files | native | 490,256 | 150,448 | 976,876 | 297,788 |
| 24 files | release | 489,508 | 149,844 | 976,716 | 297,300 |

The directory no longer matters (24 files within 0.05% of empty on
both tiers); the empty directory's own read is gone too (−13.2 MB at
20,000, about 0.66 KB a turn). What is left grows 7.4 KB a turn:
wolf-lang#612's per-command scratch, which s216's `copy region` (on
wolf-lang trunk, due in 0.2.26, sh03's pin) is for. `tools/session-rss` (no `[` in its
command) is unmoved, as it should be: 8,288 → 8,232 KB after 1,000
commands; dash flat at 2,748.

## 5. Prediction against result

| prediction | result |
|---|---|
| the rule: `*`, `?`, or a `[` that `bracket_end` closes; every `[` tried | as predicted |
| still glob: `*`, `?`, `x*[`, `[!x]`, `[]]`, `[!]]`, `[a-]`, `["a"]`, `[\a]`, `[[:alpha:]]`, `[[:alpha:]` | as predicted (one read each, `wolf test`) |
| no longer read: `[`, `]`, the fields of `[ -f x ]`, `[a`, `a]`, `"["a]`, `[a"]"`, `\[a]`, `'['a]`, `[]`, `[!]`, `[a/b]` | none read now; **but only 7 of them read before** — `]`, `a]`, `-f`, `x`, `\[a]`, `'['a]` never did (no unquoted `[`). pelt#3's title says `[` and `]` are globbed; only `[` was |
| standard output unchanged; new cases green on trunk; the red is the read count and the RSS gap | as predicted: 13 cases green before and after; red at `wolf test` and `glob-rss` |
| empty 20,000: 135,000–155,000 KB | **149,896** (release), 150,372 (native) |
| 24 files within 2% of empty | **within 0.05%** (149,844 vs 149,896) |
| 40,000 about twice 20,000; slope ~7 KB a turn | 297,200 / 149,896 = 1.98; 7.4 KB a turn |
| no differential verdict moves | 244/0/19 → 257/0/19, the 13 new cases the only change; the 276 verdict lines of trunk's matcher and the fix identical on each tier, and the two tiers identical |
