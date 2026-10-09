# sh03 — the plumbing (pelt H2)

Contract: `sprints/pelt/03-the-plumbing/sh03-the-plumbing.md` in the
planning repo (`wolffe-lang/wolf`, trunk). This file is the lane's
record: §2 is written first, §3 is committed before either release
archive is unpacked, and the evidence index (§4) is filled in as the
work lands.

## 1. Forbidden, absolutely

As the contract's §1: no `rm` outside `~/lanes/sh03/` and this lane's
own clones; no `git add -A`; nothing under `~/.claude`; no merge to
trunk, no tag; no `2>/dev/null` on a checkout; no attribution
trailers; the toolchain from the release archives by digest; no "seen
red" without a run id, sha, path or digest; strict evidence (#571);
detached kasumi jobs by recorded pid; no build on nomad-1; no package
installs. **No shell's source is read** (ruling #43): POSIX.1-2024 XCU,
the man pages, and black-box runs of `dash` and `bash --posix`. No
`extern "c"`.

## 2. Inputs, verified (2026-10-09, re-derived from origin)

| input | contract says | measured | drift |
|---|---|---|---|
| wolf 0.2.26 | wolf-lang `89dc1394`, released; linux x86-64 `05acdc5e…`, linux aarch64 `8b019b64…`, macOS arm64 `8ea7ef3b…`, windows `9cb6958d…` | tag `v0.2.26` → `89dc139443da38078df6093568da87bc6d0ee6f9`; release 408143286, published 2026-10-09T17:48:26Z, not a draft; the API's asset digests: x86-64 linux `05acdc5ea2f261f6…`, aarch64 linux `8b019b649575dd57…`, aarch64 darwin `8ea7ef3b1e6ccab2…`, windows `9cb6958d731a190f…` | none |
| lupin 0.1.49 | wolf-interp `f516a5f`; x86-64 `84911a35…`, aarch64 `e1f53d15…`, macOS `ad188d58…`, windows zip `ebff44ab…`, `lupin.exe` `64212006…` | tag `v0.1.49` → `f516a5f4ea4341acd3a30f3e5cdd4327aede1912`; release 408028965, published 2026-10-09T15:05:40Z; x86-64 linux `84911a353a03878c…`, aarch64 linux `e1f53d15d92d604c…`, aarch64 darwin `ad188d5872f520ef…`, windows zip `ebff44ab8cb56cb8…`, `lupin.exe` `642120060ef5fd65…` | none |
| what 0.2.26 changes for pelt | s217 capabilities, #618, `copy region`, `-> never`, `!` on ints, the new builtins, 10 prelude names | read in wolf-lang's CHANGELOG at the tag and `spec/11-os.md` `[os.host.sigs]`: `os_spawn_fds(str, List[str], List[int]) -> int ! {denied, invalid, io, not_found, unsupported}`, `os_pipe() -> (int, int) ! {io}`, `os_chdir(str) -> () ! {denied, io, not_found}`, `os_isatty(int) -> bool ! {io}`; `fs_read_chunk`/`fs_write_chunk` serve 0..2 (`[os.fs.std]`). A grep of pelt `1c1d0f7` for a declaration of any of the ten new names finds none (two comments mention `os_isatty`); pelt imports no std module and has no `wolf.pkg`, so s217 cannot reach it | none |
| what 0.2.26 does NOT give a shell | — | no `dup`/`dup2` of the program's OWN descriptors (a redirection of a built-in must be done by pelt itself); no `exec` and no environment unset (wolf-lang#534, OPEN); `os_wait`'s `signal` row carries no number (#534); no `getpid` (wolf-lang#141, OPEN); the handle `os_spawn*` answers is a table index, "never raw pids" (`crates/wolf_rt/src/os.rs:16` at the tag), so `$!` cannot be a process id; no SIGINT meaning (wolf-lang#622, OPEN); linux aarch64 still has no tier (wolf-lang#614, OPEN) | the contract lists `$!`; it can name a job, not a process (§3) |
| `[mem.region.copyout]` | `copy region` per command | the clause (`spec/02-memory-model.md` at the tag): the block's value is deep-copied out and the region freed; "a `mut` argument passed to a call inside the block gains the call's site (D12), so the state is written after the copy, not during the work" | shapes the design: compute inside, commit outside (§3) |
| pelt trunk | `1c1d0f7` (sh04), corpus 257/0/19, session 51/0/8 | origin/trunk `1c1d0f7d9bdaf1c7…`; push run 37953340956 green on all three hosts: difftest `257 0 19` on both tiers (PEND-ok 3 on linux: `control/async_list`, `pending/background`, `pending/pid`; 2 on macOS, no `/proc`), session `51 0 8 (1)` (`background`) | **a second push run at the same sha, 37953346374, was cancelled on macOS**: "the session corpus, native tier" started and never finished inside the job's 45 minutes (every earlier step green). A hang in the session step on macOS; watched in this lane's runs |
| PENDING | every H2 case waiting on s215 listed | `tests/diff/PENDING.md`: 15 cases wait on s215/H2 (pipe 2, redirection 7, capture 1, background 2, chdir 2, child stdin 1) and 4 on other blockers (`pending/signal_status` and `pending/unset_env` on #534, `pending/pid` on #141, `tilde/user` on a user database). `tests/session/PENDING.md`: 6 wait on H2 (`child_stdin`, `cd_root`, `pipe`, `redirect_file`, `heredoc`, `background`) and 2 on #622 (`ctrl_c_prompt`, `ctrl_c_child`); the isatty gap has no case | none |
| s216's pelt measurement | 163 → 34 MB at 20,000 turns | kasumi `~/lanes/s216/evidence/pelt2.log`: release, empty directory, 20,000 turns 163,072 KB (trunk `f0014da`) → 34,440 KB (the throwaway); **40,000 turns 66,208 KB**, so the throwaway still grew about 1.6 KB a turn. Its method: the simple command's expansion recomputed read-only in a 569-line copy of the expander (`pelt-throwaway-expand_ro.lu`) inside `copy region`, falling back to the old path for anything that writes the state; built by a wolf-lang trunk binary, not a release | the 34 MB is not flat |
| oracle | dash 0.5.13.4, bash 5.3.20 on kasumi | `pacman -Q`: `dash 0.5.13.4-1.1`, `bash 5.3.20-2`; `tests/diff/ORACLE` names both | none |
| kasumi | disk tight | `/home` 887 G used of 928 G, 38 G free (96%) at 14:45Z | builds use `CARGO_INCREMENTAL=0`, one target dir, pruned |

## 3. Prediction (committed before either archive is unpacked)

### 3.1 The pin alone (0.2.24 / 0.1.47 → 0.2.26 / 0.1.49), before any pelt change

- `tools/fetch-toolchain` accepts the six archives (linux x86-64, linux
  aarch64, macOS arm64, for wolf and lupin) at the digests in §2; the
  std tree stays at `2f389a7` (pelt imports no std module, so the pin
  is inert: wolf-std's own 0.2.26 bump, sc57, is in flight, and
  nothing here would test it).
- `wolf fmt --check` clean (neither CHANGELOG since 0.2.24 names a
  formatter change); `--deny-warnings` builds clean on both tiers (no
  W0304: no new name is declared; no #618 E1010: s216 measured pelt's
  verdicts unchanged); `wolf test` passes.
- **No verdict moves**: difftest `257 0 19` on both tiers with the same
  PEND-ok set, session `51 0 8 (1)`, `glob-rss` ok; linux aarch64
  still refuses both tiers by name (#614 open), so that job stays
  green unchanged.
- **Every binary moves.** The native tiers embed the compiler version
  in DWARF; with debug info and build-id stripped
  (`objcopy --strip-debug --remove-section .note.gnu.build-id`) both
  tiers still differ, because `libwolf_rt.a` is linked whole into each
  and changed in 0.2.25 and 0.2.26 (s200's `print` lock and fd 0..2
  path, s215's spawn, s214's added loads).
- RSS of s216's loop (`pelt -c 'i=0; while [ $i -lt N ]; …'`, `env -i`,
  median of 3, release) moves less than 5% from sh04's 149,844 KB at
  20,000 turns: nothing in the two releases touches what pelt keeps.

### 3.2 H2: what clears, what does not

**The 15 differential cases waiting on s215 pass on both tiers**, and
leave PENDING in the commits that make them pass: `control/pipeline`,
`pending/pipeline_status`, `pending/redirect_out`,
`pending/redirect_err`, `pending/heredoc`, `builtin/dot`,
`builtin/times`, `func/unset_f`, `tilde/middle`, `cmdsub/external`,
`control/async_list`, `pending/background`, `builtin/cd`,
`pending/cd_subshell`, `pending/child_stdin`. The corpus goes from
257/0/19 to **272/0/4** before any new case, plus every case this lane
adds passing (none added as pending unless named with its blocker).

**Four stay pending, each with its blocker:** `pending/signal_status`
(`os_wait`'s `signal` row has no number: pelt answers 128, dash 143;
#534), `pending/unset_env` (no environment unset: `unset HOME` still
reaches `/usr/bin/env`, so `grep -c` prints 1, not 0; #534 — and it
now runs as a real pipeline, so the remaining difference is only the
unset), `pending/pid` (macOS has no `/proc`; #141 — PEND-ok on linux as
today), `tilde/user` (no user database).

**The six session cases waiting on H2 pass** (`child_stdin`, `cd_root`,
`pipe`, `redirect_file`, `heredoc`, `background`): 51/0/8 → **57/0/2**,
the two left being `ctrl_c_prompt` and `ctrl_c_child` (#622). New
session cases for pipes, redirections and `cd` typed through the pty
pass against dash.

**The design that makes them pass** (what moves, and why):

- **A descriptor table of pelt's own.** wolf has no `dup2` for the
  program's own descriptors, so a redirection of a built-in, a function
  or a compound command cannot move descriptor 1; pelt keeps a table
  (shell descriptor → a wolf handle, 0..2 its own standard streams, or
  closed, or "the open capture") and everything pelt writes or reads
  goes through it. A child is spawned with `os_spawn_fds` and a map
  built from the whole table, so `n>&m`, `n>&-`, `exec 3>f` and a
  child's view agree. A redirection list saves and restores only the
  descriptors it names, so `exec` inside a redirected `{ }` survives.
- **Pipelines** run left to right. A stage that is an external simple
  command is spawned and not waited for (its descriptor 1 a pipe's
  write end, closed in pelt at once), so `a | b | c` of programs runs
  concurrently. A stage pelt runs itself (a built-in, a function, a
  compound command) runs as a subshell in-process; if it is not the
  last stage its output is collected and handed to the next stage
  through an unlinked temporary file, so pelt never blocks writing a
  pipe nobody is draining. Every stage's status is collected; the
  pipeline's is the last stage's, `!` negating it. **Named
  limitation:** an in-process stage that is not last runs to
  completion before the next starts, so an endless in-process producer
  (`while :; do echo y; done | head -1`) never ends (dash ends it by
  SIGPIPE in a forked child); no case asserts that shape.
- **Here-documents** go through an unlinked temporary file as the
  command's descriptor 0, for a child and for pelt's own `read` alike.
- **Command substitution of a program** spawns it with descriptor 1 a
  pipe and reads the pipe to its end into the capture.
- **`&`** spawns an external simple command and does not wait; any
  other asynchronous list runs to completion in-process (no fork) and
  is recorded as a finished job. `$!` is that job's number in pelt's
  table, **not a process id** (wolf-lang#141; the handle `os_spawn_fds`
  answers is not one): `wait $!` works, `kill $!` names the wrong
  process, so the corpus never feeds `$!` to `kill`. An asynchronous
  list's standard input is the null device (XCU 2.9.3.1, no job
  control).
- **`cd`** with `-L`/`-P`, `-`, `CDPATH`, `HOME`, `PWD` and `OLDPWD`
  (XCU `cd`), through `os_chdir`; a subshell, a command substitution
  and an in-process pipeline stage put the directory back when they
  end.
- **Interactive detection** asks `os_isatty(0)` and `os_isatty(2)`
  (XCU `sh`), so `printf 'echo hi\n' | pelt` neither prompts nor
  survives a syntax error, as dash; a case kind that runs pelt with the
  script on standard input and no operand witnesses it.
- **Input** is read from descriptor 0 itself (s200), no longer through
  a reopened `/dev/stdin`, so a child given pelt's standard input
  continues at the offset pelt left.

### 3.3 `copy region` per command: the memory

**Design.** A simple command whose words carry no expansion that
writes the shell's state (no command substitution, no `${x=…}`,
`${x:=…}`, `${x?…}`, no arithmetic assignment) is computed inside
`copy region` with the state read only: its fields, its assignments'
values, its redirection targets, and — for the built-ins that change
nothing but their output (`[`, `test`, `true`, `false`, `:`, `echo`,
`printf`) — its status and the bytes it writes. The block's value is
that plan; the state is written after the copy (the clause's "compute
inside, commit outside"). One expander serves both paths: it takes the
state read-only and reports, rather than performs, what a write would
need, and the ordinary path runs whenever the plan says so. Beside it,
the runner stops copying a node's child list on every execution, and
`LINENO` is read from the current line rather than stored per command.

**Numbers** (kasumi, release and native, `env -i`, median of 3):

| measurement | at the pin (predicted ≈ trunk) | after (predicted) | falsified by |
|---|---|---|---|
| s216's loop, empty directory, 20,000 turns | ≈ 150,000 KB | **≤ 10,000 KB** | more than 10,000 KB on either tier |
| the same, 40,000 turns minus 20,000 turns | ≈ 148,000 KB (7.4 KB a turn) | **≤ 2,000 KB** (≤ 100 B a turn: only `i`'s superseded value strings are kept) | more than 2,000 KB |
| the same, 24 files | as empty (sh04) | as empty, within 2% | more than 2% above empty |
| `tools/session-rss`, `x=$((x+1))` typed at the prompt, 20,000 commands | ≈ 116,000 KB (5.8 KB a command) | **≤ 25,000 KB** (≤ 1.2 KB a command): the parse tree of each typed line is still kept, because `sh.ast` is the shell's for its life | more than 25,000 KB; or the claim "flat" made for this row |

The interactive row is predicted **not flat**: a typed line's nodes
live in the tree for the shell's life (a function body defined at the
prompt is found there later), and `[mem.region.copyout]` cannot free
what the state keeps ("bounding the state's own garbage … is a separate
question"). What remains is named in §5 with what it would take.

### 3.4 Gates and CI

- CI green at the head on linux x86-64 and macOS arm64 (both tiers:
  fmt, build, `wolf test`, `glob-rss`, difftest, session) and the
  linux aarch64 refusal job unchanged.
- A new gate, `tools/loop-rss`, runs s216's loop at two sizes and fails
  when the larger run exceeds the smaller by more than the stated bound;
  it is planted red in CI (the plant: the `copy region` removed) and
  green again after the revert, with run ids.
- `wolf test` gains table checks for the descriptor table (which
  handles a redirection list opens, saves and restores) and the
  side-effect test that routes a command to the region path.
