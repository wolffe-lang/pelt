# sh01 — the language (pelt H1, first lane)

Contract: `sprints/pelt/01-the-language/sh01-the-language.md` in the
planning repo (`wolffe-lang/wolf`, trunk). This file is the lane's
record: §2 is written first, §3 is committed before the first change,
and the evidence index (§4) is filled in as the work lands.

## 2. Inputs, verified (2026-10-06, re-derived from origin)

| input | contract says | measured | drift |
|---|---|---|---|
| pelt trunk | `426c222`: LICENSE, LICENSE-TRAINING-DATA, CLAUDE.md, README.md | `426c222`, exactly those four files | none |
| wolf 0.2.24 | wolf-lang `294d626d`, release 404332628 | tag `v0.2.24` → tag object `97778851…` → commit `294d626dd596…`; release id 404332628, not a draft, published 2026-10-06T05:30:06Z | none |
| wolf archives | linux x86-64 `501d6d3f…`, linux aarch64 `3e4386bb…`, macOS arm64 `597421eb…` | release asset digests `501d6d3f45124c84…`, `3e4386bbba3c8a28…`, `597421eb349dcba4…`; the x86-64 archive re-hashed on kasumi after download: `501d6d3f45124c84…` | none |
| lupin 0.1.47 | wolf-interp `b3228cb5`, release 404283632 | tag `v0.1.47` → tag object `d5d24991…` → commit `b3228cb5905f…`; release id 404283632; assets: macOS arm64 `f58a51c8…`, linux aarch64 `470b43c2…`, linux x86-64 `0ddc4ff3…` (re-hashed on kasumi: `0ddc4ff38d6178ae…`) | none |
| wolf-std | trunk `2f389a7` | origin/trunk `2f389a7f60a8…` | none |
| `wolf --version` | — | `wolf 0.2.24 (wolfgang, pin 294d626)` / `paired with lupin 0.1.47 (reference interpreter), pin 8e36bc1` | — |
| oracle | `dash`, `bash --posix` on kasumi | kasumi: `dash 0.5.13.4-1.1` (`/usr/bin/dash` sha256 `c6221703b6197ce2…`), `bash 5.3.20-2` (`/usr/bin/bash` sha256 `a8ce2b3c38c81853…`) | none |
| std.process | `Command`, `start`, `run`, `wait`, `kill`, `exit`; argv only | as stated; the builtins under it are `os_spawn(List[str]) -> int ! {denied, io, not_found}` and `os_wait(int) -> int ! {io, signal}` (`spec/11-os.md` `[os.host.sigs]` at `v0.2.24`) | see below |

What the contract does not say and the spec at `v0.2.24` does
(`[os.proc.spawn]`): **a child's descriptor 0 is the null device**, and
1 and 2 are inherited. So a command pelt runs can never read pelt's own
standard input until s215's descriptor map lands; that is an H2 matter
but it shapes H1's corpus (no case may feed an external command input).
Also absent at `v0.2.24`, all already filed as **wolf-lang#534** (bu14):
no exec, no environment unset or clear, no child environment or working
directory, and `os_wait`'s `signal` row drops the signal number. No
`chdir` exists (`os_cwd` reads only), so `cd` waits on s215.

Probes on kasumi with the 0.2.24 archive (both tiers) that decide the
design: an `enum` whose variants carry differently shaped payloads is
refused ("enum payload slots with conflicting types across variants",
c06), and a struct holding a `List` of itself is refused at the push
("`copy` of a value nested this deep"). So the AST is an **arena**: one
`List[Node]`, children by index.

## 3. Prediction (committed before the first change)

**What lands in this lane.**
- Scaffold: pin, fetch, build on both tiers, CI on linux x86-64, linux
  aarch64 and macOS arm64, a planted break seen red. Certain.
- Lexer and parser for the whole XCU 2.10 grammar including here-document
  bodies and every quoting form, `--parse` printing the AST, `-n`
  refusing at dash's line. Expected to land complete.
- Expansions: tilde (`~` and `~/…`; **`~user` pending**: no password
  database lookup exists, and reading `/etc/passwd` is not what dash
  does on a host with other sources), every `${…}` form, arithmetic at
  signed 64-bit with the full operator set, field splitting, pathname
  expansion over `fs_read_dir`, quote removal. **Command substitution
  lands for builtins and functions only**, run in-process with the
  output captured in a buffer; a command substitution that runs an
  external program is **blocked** (no capture surface, `[os.proc.spawn]`)
  and goes to PENDING.
- Execution: assignments, `PATH` search, exit status, `set -e/-u/-x/-f`,
  every special built-in on the contract's list, `if/while/until/for/
  case`, functions, `&&`/`||`/`!`. **`cd` blocked** (no `chdir`); `pwd`
  lands. `exec` without redirections is approximated as run-then-exit
  (no exec builtin, #534), and says so. `trap` records every condition
  and runs `EXIT` only.

**Hard in wolf, expected.** The AST (no recursive payloads: arena);
building strings (`+=` is quadratic: byte buffers); the child's
environment (no unset: an `unset` or un-`export`ed variable that came in
from the environment still reaches a child — a known wrong answer,
#534); a signal death's status (`128+N` cannot be computed; pelt will
report 128+? and the case is PENDING on #534); subshell state for
in-process command substitution (copy the variable table and restore).

**Gaps expected to file.** None new beyond #534 and s215's set: the
password database (`~user`) is the one candidate, filed only if a case
needs it.

**Numbers.** The corpus at head holds **at least 150** cases across
parse, quoting, parameters, arithmetic, splitting, globbing, tilde,
command substitution, simple commands, built-ins, control flow,
functions and options; **at least 95 percent pass on both tiers**
(native and release give identical verdicts on every case, since no
case measures time); **at least 15** go to PENDING with the primitive
each waits on. M-SH1 is **not** reached by this lane: `cd` alone keeps
it open. A prediction falsified by any of: fewer than 150 cases, a
pass rate under 95 percent on either tier, a case whose verdict differs
between tiers, or `cd` landing.
