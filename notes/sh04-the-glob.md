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

(filled in as the work lands)

## 5. Prediction against result

(filled in at the end)
