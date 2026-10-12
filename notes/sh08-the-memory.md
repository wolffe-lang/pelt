# sh08 — the memory (pelt#19, P13)

Contract: `sprints/pelt/08-the-memory/sh08-the-memory.md` in the
planning repo. This file is the lane's record: §1 to §3 are committed
before the first change under `src/`, and the evidence (§4) is filled
in as the work lands.

## 1. Forbidden

No shell's source is read or searched for (ruling #43): POSIX.1-2024
(pubs.opengroup.org), man pages as documentation, black-box runs of
dash 0.5.13.4 and `bash --posix` only. No `extern "c"`. The wolf
runtime's own source (wolf-lang, ours) is read where it explains where
memory goes. The editor and history (`sh.edit`, the history half of
`sh.interact`) are sh12's, running beside this lane: not touched here;
whichever lands second rebases. No merge, no tag, no issue filed or
closed, no package installed, no other lane's CI run cancelled, nothing
under `~/.claude`; no attribution trailers. The toolchain from the
release archives by digest (the pin does not move). Detached kasumi
jobs by `setsid` with the pid recorded and killed by that pid only;
scratch under `~/lanes/sh08/` (`TMPDIR` points there), never `/tmp`;
no build on nomad-1. Strict evidence (#571).

## 2. Inputs, verified (2026-10-12, before any change)

Paths named `logs/…` and `probe/…` below are under `notes/sh08-evidence/`.

| input | contract says | measured | drift |
|---|---|---|---|
| pelt trunk | `96828ac` on 0.2.28 | `origin/trunk` = `96828ac`; branch `sh08` cut from it; wolf 0.2.28 / lupin 0.1.51 / std `98e1b7b` | none |
| pelt#19 | 9.9 KB a pipeline, 6.2 KB a substitution, 1.3 KB a call, 1.7 KB a script line; 258 MB for 20,000 lines of `true \| true` | open, the same text | none |
| the shapes at trunk | — | `logs/base-shapes.log` (sh06's `loopmem.sh` widened, `probe/shapes.sh`; its `true &` row is a syntax error in the probe, `&;`, and is not read): per turn from 5,000 to 20,000, release tier — `true \| true` **10.0 KB**, `echo x \| cat` 10.7, `x=$(true)` **6.3**, `x=$(echo y)` 7.0, backquote 6.4, `x=$(echo a \| cat)` **18.2**, `( true )` 4.3, `f` **1.4**, `g a b` (`local`, an assignment, `return`) **6.7**, `case` 0.35, `for` 0.73, `{ true; }`, `&&`, `if` under 0.1; a script of N lines: `true` **1.7 KB a line**, `true \| true` 12.9, `x=$(true)` 9.3, `f` 3.0, `: $((i=i+1))` **5.6**. The native tier within 5% of these. dash flat on every row (2.8–3.1 MB) | sh06's numbers reproduce (`true \| true` 200 → 203 MB at 20,000 turns; the 20,000-line script 258 → 261 MB) |
| the existing gates | loop-rss, session-rss | `tools/loop-rss` passes on both tiers (`logs/base-loop-*.log`); `tools/session-rss` is a tool, not a CI step | none |
| the trunk gauntlet | (sh13) corpus 835/0/99, sessions 171/0/26, clauses 431 of 544 | so far (`logs/base.status`, running): fmt, `wolf test`, the clause table (**431 of 544**), the corpus **835/0/99** on both tiers and under `taskset -c 0-3`, the corpus self-test, sessions native **171/0/26**; the rest is recorded in §4 when the run ends | none so far |
| the new gate at trunk | — | `tools/shape-rss` (written for this lane, below) on trunk's binaries: **all 19 shapes fail on both tiers** (release: `( true )` 2.8 KB a turn up to `x=$(echo a \| cat)` 13.5 KB; the typed lines 4.4–11.7 KB) and dash passes all 19 (`logs/shape-base-*.log`) | — |

## 3. Prediction (committed before the first change under `src/`)

### 3.1 The cause, per shape (from the heap profile)

The wolf runtime's process root is a bump arena over 64 KiB chunks that
is never freed (`wolf_rt` `str.rs`, `ambient_alloc`); a region's chunks
are pooled and freed wholesale. Everything pelt allocates outside a
`region` block lands in the root and stays. `probe/heapprof.py` runs
pelt (native tier, which carries DWARF) under gdb with a breakpoint on
every `malloc` of 64 KiB or more — after warm-up only the root grows
that way — and records the pelt frames that overflowed the chunk: a
byte-proportional sample of who allocates in the root
(`logs/prof-base/`, 3,000 turns a shape; the sampling aliases with a
loop's period, so shares are rough and the sites are what counts).

| shape | where the root grows | why |
|---|---|---|
| a pipeline | `snap` and `restore` (`map_copy`, `list_copy`) around every stage, the stage's simple command on the ordinary path (`run_slow`: the copied words, the lists, the expansion), `cap_end_bytes`'s two slices | a stage runs as an in-process subshell: the state is copied before (`snap`) and copied again to put it back (`restore`), and both copies live in the root; a non-last stage has a capture open, which keeps it off the `copy region` fast path (`fast_ok` wants no capture) |
| a substitution | `snap`/`restore` in `run_cmdsub`, `cap_end`, the `"{i}:{w}"` parse-cache key, the outer command on the ordinary path | as a pipeline stage, plus: the command around a substitution can never take the fast path (the shadow bails at `$(`), and the substitution's body sees a capture |
| a subshell `( )` | `restore`'s `map_copy` | as above |
| a function call | `run_slow`: the copied word list, `assigns`/`rest`/`names`/`values`/`shown`/`had`/`old`, the expansion, `redirs_of`, `args_of`; `call_function`'s copy of `$@` and its new one | a function is never on the fast path, and the ordinary path builds a dozen lists per command in the root |
| `local`, `return`, an arithmetic assignment | the ordinary path, and the arithmetic parser's `level_ops` lists | a built-in that writes the state, and an expansion that assigns (`$((j=j+1))`, `${x=…}`), bail out of the shadow to the ordinary path |
| a script line | the tree: `add`'s node and its four lists, `parse_list_top`, the lexer's `buf`/`text` per word, `read_docs`'s three fresh lists per newline | every complete command is parsed into `sh.ast`, which only grows: a script's tree is kept whole although nothing reads a finished top-level command again |
| a typed compound line | the same tree, through `eval_from` | as a script line |

### 3.2 The design

The rule wolf asks of an interpreter (`[mem.region.copyout]`): compute
in a `copy region`, commit outside it; and whatever must be written to
the state is written in place (into capacity the state already has)
rather than as a fresh copy. Five changes, each its own commit:

1. **Subshells keep a journal, not a copy.** `snap`/`restore` go. A
   subshell (`( )`, `$( )`, a pipeline stage, an `&` list) opens a
   frame; every write to the variables, export and read-only marks,
   functions and traps goes through one helper per table that records
   the old value once per frame (a name already recorded in this frame
   is found through a name → journal-index map and not recorded again);
   closing the frame plays the journal back. The scalars (options,
   `loops`, `fdepth`, `dots`, the mask, the `local` stack's lengths)
   and the descriptor table and `$@` are pushed onto reusable stacks.
   A subshell that writes nothing allocates nothing; one that writes
   keeps only the values it wrote. The trap reset at a subshell's start
   is done in place over the fixed set of condition names.
2. **Buffers in place.** `flush` clears `out` instead of making a new
   list; a capture's bytes are cut out of `cap_data` in place, the
   substitution's text made inside a `copy region` and a pipeline
   stage's caught bytes fed to the next stage from inside one;
   `run_pipeline`'s child list lives in the state.
3. **The fast path under a capture.** A simple command whose standard
   output is the innermost capture (a substitution's body, a pipeline
   stage) runs in the shadow inside `copy region` like any other: a
   pure built-in hands back its output (as the `str`, or hex when the
   bytes are not UTF-8), a program run for a substitution is waited for
   with its output drained into the region, and a non-last stage's
   program is started on the stage's pipe and its handle handed back.
   An expansion that assigns (`$((j=j+1))`, `${x=…}`) no longer bails
   out of the shadow: the assignment is recorded and committed after,
   in order.
4. **The ordinary path, lean.** No copied word list; the lists built
   only when there is something to put in them; the words of a
   function call or of a built-in expanded inside `copy region` when no
   substitution is among them, handed back NUL-joined in one `str`;
   `$@` for a call written in place (the caller's parameters pushed on
   a stack and put back), not rebuilt; an assignment whose value is a
   whole `$(…)` or `` `…` `` takes the substitution's text as is; the
   substitution parse cache keyed by the word (a view of the tree)
   instead of a built string; `case` and `for` expand their words in a
   region.
5. **The tree recycles.** After a complete command parsed by
   `eval_from` (a script line, a typed line, `eval`, `.`, a trap action)
   has run, the nodes it added are taken back unless something kept
   one (a function definition, a substitution or backquote parse cache
   entry): `Ast.top` marks the live end, `add` reuses a dead slot by
   clearing its lists in place, and the here-document list does the
   same. The lexer scans into one buffer the parser owns and makes a
   word a view of the source when its bytes are the source's.

### 3.3 Numbers

A new gate, `tools/shape-rss`, runs each shape at N = 10,000 and
2N = 20,000 turns and allows the bound `tools/loop-rss` allows: 100 B a
turn plus 1 MiB (2,000 KB over the second 10,000), on both tiers, in CI
on linux x86-64 and macOS arm64. dash passes every row today (growth
-76 to +128 KB: `logs/shape-base-dash.log`).

| shape | trunk, release (KB a turn) | predicted after | gated |
|---|---:|---:|---|
| `true \| true` | 10.0 | under 0.1 | yes |
| `echo x \| cat >/dev/null` | 10.7 | under 0.1 | yes |
| `x=$(true)` | 6.3 | under 0.1 | yes |
| `x=$(echo y)` | 7.0 | under 0.1 | yes |
| `` x=`true` `` | 6.4 | under 0.1 | yes |
| `x=$(echo a \| cat)` | 18.2 | under 0.1 | yes |
| `( true )` | 4.3 | under 0.1 | yes |
| `f a b` | ~1.5 | under 0.1 | yes |
| `g a b` (`local v; v=$1; return 0`) | 6.7 | under 0.2 | yes |
| `: $((j=j+1))` | — (5.6 a script line) | under 0.1 | yes |
| a script of N `true` | 1.7 | under 0.1 | yes |
| a script of N `true \| true` | 12.9 | under 0.1 | yes |
| a script of N `x=$(true)` | 9.3 | under 0.1 | yes |
| a script of N `f` | 3.0 | under 0.1 | yes |
| typed `true \| true; i=$((i+1))` | 11.7 | under 0.2 (the line's text is kept by the editor's history, sh11's, at about its length) | yes |
| typed `true && true; …`, `{ true; }; …`, `if true; then :; fi; …` | 4.8, 4.4, 6.5 | under 0.2 | yes |
| typed `x=$(true); …` | 9.5 | under 0.2 | yes |
| `case`, `for` in a loop | 0.35, 0.73 | under 0.1 | no (`tools/shape-rss` lists them for the record) |

Falsified if any gated shape exceeds the bound on either tier on
kasumi, or if a shape the table predicts under 0.1 KB lands above
0.2 KB a turn.

What is still kept, stated: a variable's superseded value (the root
frees nothing, so `i=$((i+1))` keeps its few bytes a turn, as at
trunk: about 36 B); a substitution's output when it is assigned;
the line a person typed (the editor's history); a function body, a
substitution's parse, a here-document's text, each once per distinct
text. The gates allow these by their per-turn bound; bounding them too
needs the state compacted into a fresh region, which wolf 0.2.28 has
no way to do without copying it into the root (a separate question,
named in `[mem.region.copyout]`).

### 3.4 Behaviour

None moves. The differential corpus (835/0/99 at trunk) and the
session corpus (171/0/26) the same on both tiers and under
`taskset -c 0-3`; `tools/exec-witness`, `tools/edit-witness`,
`tools/glob-rss`, `tools/loop-rss` green; the script census at trunk's
76 of 80 (aided) with every verdict and exit status as at trunk.

### 3.5 Speed (`tools/bench`)

The four loops, head against trunk, release and native: **pipeline
and configure-shaped 3–15% faster** (a stage no longer copies the state
twice), **fork and param within 3%** (their commands are already on the
fast path; the journal costs one length check per write outside a
subshell). Falsified if any row is more than 3% slower on user
instructions or, pinned to four cpus, on the median wall time.

### 3.6 The result against the prediction

Measured on kasumi (linux x86-64) at the head `a09a162` (`logs/head3.*`)
against trunk `96828ac` (`logs/base.*`); per-turn numbers are
`tools/shape-rss`'s, 10,000 → 20,000 turns, and include the loop's own
cost (the `baseline` row: 46 B release, 49 B native).

| prediction | predicted | measured | held? |
|---|---|---|---|
| 3.3 every gated shape within the bound, both tiers | 22 of 22 | **22 of 22 on both tiers** (trunk: 21 of 22 fail, `logs/shape-base-*`) | held |
| 3.3 `true \| true` | under 0.1 KB a turn | 56 B release, 55 native (trunk 7,124 B) | held |
| 3.3 `echo x \| cat` | under 0.1 | 110 B release, 60 native (trunk 7,795) | held net of the loop (64 B); the raw row is over 0.1 |
| 3.3 `x=$(true)`, `$(echo y)`, backquote | under 0.1 | 74 / 81 / 79 B release, 85 / 102 / 90 native (trunk 4.9–5.6 KB) | held net of the loop |
| 3.3 `x=$(echo a \| cat)` | under 0.1 | 147 B release, 139 native (trunk 13,479) | **missed** by about 0.05 KB (about 100 B net of the loop); under the falsifier's 0.2 KB |
| 3.3 `( true )` | under 0.1 | 60 / 34 B (trunk 2,848) | held |
| 3.3 `f a b` | under 0.1 | 60 / 95 B (trunk 2,430) | held |
| 3.3 `g a b` (`local`, assignment, `return`) | under 0.2 | 117 / 96 B (trunk 6,800) | held |
| 3.3 `: $((j=j+1))` | under 0.1 | 55 / 33 B (trunk 3,959) | held |
| 3.3 scripts of N `true`, `true \| true`, `x=$(true)`, `f` | under 0.1 a line | 9 / 16 / 13 / 35 B release, 8 / 32 / 27 / 87 native (trunk 1,690–10,050); the 20,000-line `true \| true` script peaks at **3,484 KB** release (trunk 200,996; dash 2,588) | held |
| 3.3 typed lines (pty, the editor on) | under 0.2 | 112–144 B a line on both tiers (trunk 4,404–11,670) | held |
| 3.3 `case`, `for` (not predicted gated) | under 0.1 | 48 / 72 B release (trunk 360 / 749); gated after all | held |
| 3.4 corpus, sessions, gates | unchanged | corpus **835/0/99** on both tiers and under `taskset -c 0-3`; sessions **171/0/26** likewise; `wolf test`, fmt, clauses (431 of 544), glob-rss, loop-rss (33 / 32 B a turn), exec-witness, edit-witness, oracle check, static build: all exit 0 (`logs/head3.status`) | held |
| 3.4 the script census | as trunk | unaided and aided **76 same, 3 differ, 1 unstable**; every verdict and exit status identical to trunk's (`scripts/*-unaided.tsv`, `*-aided.tsv`, compared column by column) | held |
| 3.5 pipeline, configure-shaped faster | 3–15% | wall time, medians of 9 pinned to cpus 0-3: pipeline **−24% release, −22% native**; configure-shaped **−34% release, −29% native** (system time halved: fewer pages to fault in). Unpinned the same within 3 points (`bench/`) | direction held; the band was too timid |
| 3.5 fork, param within 3% | no row more than 3% slower | release: fork −0.6%, param **−4.6%** wall, +0.4% / −3.3% instructions. **Native: fork +5.7%, param +6.3% wall (pinned), +3.1% / +3.3% instructions**; unpinned +2.1% / +3.1% | **held on release, falsified on native** (below) |

**Why the native tier is slower on fork and param.** Every fast-path
command builds a shadow state (`new_sh`) inside its region; the state
now has six more lists (the journal's two, two stacks, the
substitution cache and its word map, where trunk had three maps), and
a pipeline stage or substitution body that trunk ran on the ordinary
path now runs on the fast one. On the release tier that costs about
7% instructions per fast command and is repaid by everything the root
no longer has to grow; on the native tier, which does not optimise,
it is about 11% per fast command (`logs/instructions-per-command.txt`).
Two speed commits (`303956b`, `a09a162`) took the cost per command
from +36% to +7% release and folded `case` onto a plain path that is
faster than trunk's; what is left would need a shadow that is not a
whole `Sh`, which is a larger change than this lane's.

**Seen red.** `tools/shape-rss` failed 21 of 22 rows on trunk's
binaries on both tiers before any change (`logs/shape-base-*`). The new
table checks were planted red once on kasumi (the journal's replay
removed and the tree's recycling made unconditional: `want_journal`
and `want_recycle` failed by name, `logs/plant-selftest.log`) and put
back. In CI the plant is branch `sh08-plant` (`0337d7f`: a subshell
keeps a copy of the variables again), dispatched as run 38243184319.

## 4. Evidence index

Under `notes/sh08-evidence/`:

- `logs/base.status`, `logs/head3.status` (and `head1`, `head2` for the
  intermediate heads `224441a` and `70c51dd`): every gauntlet step's
  exit status; the logs beside them for the corpus, sessions, gates
  and the two tiers at the head.
- `logs/shape-base-*.log`, `logs/shape-base-extra-*.log`: the new gate
  on trunk; `logs/head3-shape-*.log`: on the head.
- `logs/base-shapes.log`, `logs/prof-base/`: the measurement and heap
  profile §3.1 rests on; `probe/shapes.sh`, `probe/heapprof.py`,
  `probe/profall.sh` made them.
- `logs/instructions-per-command.txt`: instruction counts per command
  and per commit (`probe/kasumi/icount.sh`, `icommits.sh`).
- `scripts/`: the script census at trunk and at the head, both passes.
- `bench/`: `tools/bench` pinned and unpinned, load before and after,
  instruction counts, the binaries' digests.
- `logs/plant-selftest.log`: the table checks seen red.
- `witness/`: lane-local wolf programs: `emptystr` (what `copy region`
  keeps for a `str` in its value), `pool` (a `List` pushed into a
  `List` is copied, so lists cannot be pooled), `enumcopy` (the
  compiler refusal below).
- `probe/kasumi/`: the scripts that ran all of it on kasumi.

### 4.1 A wolf finding, for wolf-lang (not filed; text below)

**Title:** `cannot compile this yet — a zero value of this type` for a
payload-less variant of an enum whose other variant carries a `str`,
chosen by an `if` expression; the checked machine and lupin run it.

**Body:** On wolf 0.2.28 (`f71ece8`), linux x86-64, `witness/enumcopy/min.lu`:

```
enum T { Nothing, Text(str) }
fn main() -> int {
    let i = env_args().len
    let t = if i == 1 then T.Text("x") else T.Nothing
    match t { T.Nothing => print("nothing"), T.Text(s) => print(s) }
    0
}
```

`wolf build` and `wolf build --release` both stop with "cannot compile
this yet — a zero value of this type @282..291" (the span is
`T.Nothing`), exit 4. `wolf conform-run --checked` answers
`exit(0)`, stdout `nothing`; `lupin run` prints `nothing`, exit 0. The
same refusal comes when the value is a struct field built in a
`copy region` block (`witness/enumcopy/main.lu`, `plain.lu`), which
is how pelt met it: an optional `str` in the fast path's result could
not be spelled as an enum. A tier disagreement, though an honest one
(the conservatism ledger).

Not a finding, measured and set aside: an empty `str` in a
`copy region` block's value costs about 16 bytes of root per copy
inside pelt, but under 2 bytes in every witness built to show it
(`witness/emptystr`); pelt's fast-path result carries one `str`, as
trunk's did, and that is where it was left.

## 5. Done-when

- PR open with the five sections, the commits as bullets and the test
  checklist: wolffe-lang/pelt#25.
- CI green at the head on linux x86-64 and macOS arm64 (and the
  aarch64 refusal job): recorded in the PR.
- The planted break red in CI: run 38243184319 on `sh08-plant`.
- `wolf/tools/lane-audit.sh pelt sh08 25` run from the org directory,
  its exit status read directly: in the lane's report.

## 6. Not verified

- macOS arm64's numbers for the new gate are CI's only; nothing was
  run on nomad-1 (no builds there).
- linux aarch64 builds no tier (wolf-lang#614), so no shape is measured
  there.
- What a turn still keeps (a superseded variable value, about 16–36 B;
  the editor's history line at the prompt) is bounded only by the
  gate's per-turn allowance, not freed.
- The journal's dedup scans the open frame's entries: a subshell that
  writes thousands of distinct names would pay quadratic time; no case
  or script in the corpus does, and it was not measured.
- pelt under lupin: still stops at `env_vars` (wolf-interp#240), so the
  checked tier of this work is the compiler's only.
- sh12 (the history) touches `sh.interact`; whichever lands second
  rebases, and the gates are to be re-run then.
