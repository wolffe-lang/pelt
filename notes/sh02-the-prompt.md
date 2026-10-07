# sh02 — the prompt (pelt H3's first step)

Contract: `sprints/pelt/02-the-prompt/sh02-the-prompt.md` in the
planning repo (`wolffe-lang/wolf`, trunk). This file is the lane's
record: §2 is written first, §3 is committed before the first change,
and the evidence index (§4) is filled in as the work lands.

## 2. Inputs, verified (2026-10-07, re-derived from origin)

| input | contract says | measured | drift |
|---|---|---|---|
| pelt trunk | `f0014da` (sh01) | origin/trunk `f0014da7e52b…`; CI green there: push run 37566452439, PR run 37556154743 | none |
| corpus | 244/0/19 | kasumi, `taskset -c 0-3`, `WOLF_PAIRING_REQUIRE_SIBLING=1`, lupin 0.1.47 staged beside wolf: native `244 0 19 (3)`, release `244 0 19 (3)`; `tools/check-test` rc 0 | none |
| CI hosts | linux x86-64, macOS arm64; aarch64 asserts refusals (wolf-lang#614) | `.github/workflows/ci.yml` at `f0014da`: exactly that | none |
| pins | wolf 0.2.24 / lupin 0.1.47 | `wolf-toolchain.toml`: `wolf 0.2.24 (wolfgang, pin 294d626)`, lupin `0.1.47`; fetched by digest on kasumi (`0ddc4ff38d6178ae…` lupin x86-64 OK); wolf-lang's latest release is still `v0.2.24` (2026-10-06), so no 0.2.25 to drift to | none |
| child stdin | the null device (`[os.proc.spawn]`) | spec `11-os.md` at `v0.2.24`, line 623: "descriptor 0 wired to the host's null device" | none |
| #612 | stands | wolf-lang#612 OPEN | none |
| oracle | dash, `bash --posix` | kasumi: `dash 0.5.13.4-1.1` (`c6221703b6197ce2…`), `bash 5.3.20-2` (`a8ce2b3c38c81853…`), kernel 7.2.8 | none |

What the contract does not say and the spec at `v0.2.24` does:

- **Standard input as bytes.** `[os.fs.std]`: `fs_read_chunk` answers
  `io` on descriptor 0 (byte I/O on the standard streams is
  wolf-lang#405's), and `read_line` reads ahead into a buffer the
  runtime holds. A byte-wise reader therefore opens `/dev/stdin`
  (a new handle on the same terminal, pipe or file; pelt already
  writes standard output through `/dev/stdout` the same way) and reads
  it one byte per `fs_read_chunk`. When the open fails, the shell falls
  back to `read_line`.
- **No terminal test.** `fs_fstat(0)` answers kind 0 for a regular
  file and kind 2 for "a pipe, a socket or a terminal" alike
  (`[os.fs.fstat]`), so 0.2.24 can tell a file on standard input from
  everything else and nothing finer. `os_isatty` is s215's, unreleased.
- **No interrupt meaning.** `[os.signal.set]` has four meanings
  (HUP, TERM, QUIT, USR2); none is `SIGINT`, so a wolf program cannot
  catch Ctrl-C. No open wolf-lang issue names it (searched
  `signal OR isatty OR termios OR interrupt`: #423 is SIGPIPE, #534 the
  wait status, #141 getpid).

Black-box runs of `dash -i +m` on kasumi through a pty (standard
input the pty's slave; standard output and error separate pipes) that
shape the design: prompts go to standard error; `PS1` and `PS2` are
expanded as a double-quoted word would be (parameter, arithmetic and
command substitution: `PS1='[$x]$((x+1))$(echo c)> '` shows `[7]8c> `);
an expansion error, a special built-in's error, a syntax error and an
assignment to a read-only variable each abandon the rest of the line,
set `$?` to 2 and return to the prompt; a command not found does not
abandon the line; `set -e` then `false` ends the interactive shell; at
end of file dash writes a newline to standard error and exits with the
last status; end of file inside an open `if` is a syntax error, then
the `EXIT` trap, then status 2; `$ENV` is parameter-expanded and the
file read before the first prompt, a missing file silently ignored;
`$-` is `si`.

## 3. Prediction (committed before the first change)

**What works at the prompt.** `pelt` with no operands and no `-c`,
`pelt -i`, and `pelt -s [arg…]` print `PS1` (default `$ `) to standard
error, read one line byte by byte, and when the text so far is not a
complete command (an open quote, `if` without `fi`, a `{` without `}`,
a here-document whose delimiter has not come, a trailing `&&`, `|` or
`\`) print `PS2` (default `> `) and read another; then run it and loop.
`PS1` and `PS2` are expanded as dash expands them (parameter, arithmetic,
and command substitution of built-ins and functions — the in-process
kind sh01 built). End of file exits with the last status; `exit [n]`
works; a syntax error, an expansion error, a special built-in's error
and an assignment error print and return to the prompt with `$?` 2.
`$ENV` is expanded and its file run before the first prompt. `$-`
carries `i` and `s`. The maintainer's list (`echo hi`, `ls`, `date`,
`pwd`, `x=3; echo $((x*2))`, a function defined and called, `exit`,
Ctrl-D) all works, `ls` and `date` writing straight to the terminal.

**Interactive by default.** POSIX makes the shell interactive with no
operands and no `-c` when standard input and standard error are
terminals; 0.2.24 cannot ask (no isatty). pelt is interactive when
standard input is the command source **unless `fs_fstat(0)` says it is
a regular file** (the one thing 0.2.24 can see), so `pelt < script`
stays a script and `echo cmd | pelt` prompts where dash does not. The
pipe case goes to PENDING on `os_isatty`. Non-interactive standard input
is read and run one complete command at a time, as dash does, not
slurped whole as sh01's `pelt` did.

**PENDING, and why.**
- a child reading the keyboard (`cat` at the prompt ends at once:
  descriptor 0 is the null device) — s215's descriptor map;
- `cd` — s215's `os_chdir`;
- pipes, redirections, here-documents to a command — s215;
- `&`, `jobs`, `fg`, `bg`, Ctrl-Z — process groups, a later s lane;
- **Ctrl-C at the prompt kills pelt** (SIGINT's default action: no
  interrupt meaning to catch, to be filed on wolf-lang); a child
  killed by Ctrl-C reports `128+?` (#534);
- a pipe on standard input prompts — `os_isatty`;
- line editing and history — none in this lane (contract).

**Numbers.**
- The session corpus holds **at least 30** cases (I expect 35–40),
  every non-pending case passing on both tiers with identical verdicts;
  **5 to 10** pending, each naming its primitive.
- **RSS after 1,000 interactive commands** (`x=$((x+1))`, typed one per
  prompt through the pty, release tier): pelt grows linearly and never
  returns it (#612 plus the parse arena, which keeps every line's
  nodes), **10–20 KB per command, so 12–25 MB after 1,000**, against
  dash's flat ~1–2 MB. Falsified by growth under 5 MB or over 40 MB, or
  by RSS that stops growing.
- Wolf-lang findings to file: **one** (no interrupt meaning). Falsified
  by a second gap I have to name.

## 4. Evidence index

Every log named here is committed under `notes/sh02-evidence/`, with its
sha256. The gauntlet ran on kasumi from a clean clone at the named sha,
`taskset -c 0-3`, `WOLF_PAIRING_REQUIRE_SIBLING=1`, lupin 0.1.47 staged
beside wolf 0.2.24 (both version lines are in the log).

**At head** (`1ba87c0`; `gauntlet-1ba87c0.log` `b6f7a68d6df58dea…`,
sources digest `4103e296752df968…` over `src tools tests`): `wolf fmt`
clean, both tiers build with warnings denied, `wolf test` rc 0, and on
**both tiers, identical**:

| corpus | pass | fail | pending (of which pass) |
|---|---|---|---|
| differential (`tests/diff/`, sh01's) | 244 | 0 | 19 (3) |
| session (`tests/session/`, new) | 51 | 0 | 8 (1) |

`session-selftest` (right 0, wrong prompt 1, unlisted pending 1) and
`difftest-selftest` rc 0. CI at `1ba87c0`: run **37684766817**, green on
linux x86-64 and macOS arm64 (both tiers, both corpora; the macOS legs
answer the same 51/0/8), aarch64 asserting its refusals.

The session corpus: 59 cases typed through a pty, each recorded twice
from `dash -i +m` (`tools/session-record` refuses a transcript two runs
disagree on) and once from `bash --posix -i +m` as a second opinion on
standard output and exit status (8 differ: bash's `--posix` interactive
shell takes another line for some errors; dash is the oracle). The one
pending case that passes, `background`, does so because `sleep 0 &` run
in the foreground prints what dash prints; it stays pending.

**Signal rows** (`ctrl_c_prompt`, `ctrl_c_child`): the harness starts
the shell with SIGINT and SIGQUIT at their defaults and nothing blocked
(a harness launched in a non-interactive shell's background inherits
both ignored — the first recording showed `sleep 5` outliving its ^C for
that reason, and it was re-recorded after the fix, `df942b5`). Measured
from `/proc`: dash `SigBlk 0000000000000000 SigIgn 0000000000004004`
(QUIT and TERM ignored, as an interactive shell does); pelt `SigBlk
0000000000000000 SigIgn 0000000000000000` on both tiers. pelt dies of
the ^C (`signal 2`): wolf-lang#622.

**Red, then green** (the session corpus run against trunk's pelt):
`witness-f0014da-native.log` `61d1b8ab89bf30a9…`: pelt built at
`f0014da`, **pass 0, fail 51**, pending 8 (0) — it reads all of standard
input before running anything and takes `-i` for an unknown `set`
option. Green: the head gauntlet above. (The release-tier run of the
same witness was stopped after the native one finished: every case waits
out the prompt timeout there, and the two tiers share the source.)

**The planted break**: `c940f04` makes an interactive shell exit on a
shell error, as a script does. Locally (`plant-c940f04-release.log`
`4fb9d6c5fa3cca9f…`): 7 FAIL — `arith_error`, `expansion_error`,
`readonly_assign`, `set_u_error`, `special_builtin_error`,
`syntax_error_continues`, `syntax_error_midline`. In CI: run
**37681872386**, red on linux x86-64 and macOS arm64 at "the session
corpus, native tier" with the same seven. The revert `36a2fc5` has a tree
byte-identical to `e8658aa`'s (`git diff e8658aa 36a2fc5` empty); its run
**37683449313** is green.

**RSS after 1,000 interactive commands** (`tools/session-rss`, in the
head gauntlet log; `x=$((x+1))` typed 1,000 times, each after its
prompt; `ps -o rss`, KB):

| shell | 0 | 250 | 500 | 750 | 1,000 | per command |
|---|---|---|---|---|---|---|
| pelt native | 2,856 | 4,468 | 5,888 | 7,348 | 8,732 | 5.9 KB |
| pelt release | 2,628 | 4,060 | 5,480 | 6,940 | 8,324 | 5.7 KB |
| dash 0.5.13.4 | 2,744 | 2,812 | 2,812 | 2,812 | 2,812 | flat |

Linear and never returned: wolf-lang#612's shape at the prompt (the
command's scratch in the ambient region) plus the parse arena, which
keeps every line's nodes in `Sh.ast`. The two are not separated here.
pelt would hold about 60 MB after 10,000 commands; not worked around, as
the contract says.

**The demo** (`demo-1ba87c0.txt` `ba058980c1d27038…`, from
`tools/session-demo`: all three descriptors on one pty, as a terminal
runs it): the maintainer's first commands, typed into pelt `1ba87c0`'s
release build on kasumi.

## 5. Prediction against result

| prediction | result |
|---|---|
| plain `pelt`, `-i`, `-s` prompt with `PS1`, continue with `PS2` on an open quote, `if`, `{`, here-document, trailing `&&`/`\|`/`\` | as predicted; the here-document's prompts are right but the case is pending (a here-document needs a redirection) |
| `PS1`/`PS2` expanded as dash does (parameter, arithmetic, built-in command substitution), `$?` untouched | as predicted (`ps1_param`, `ps1_arith_cmdsub`, `ps1_status`, `ps1_unchanged_status`) |
| EOF exits with the last status; `exit` works; 2.8.1's interactive column | as predicted, and dash's EOF inside an open `if` (syntax error, `EXIT` trap, status 2) matches too |
| `$ENV` expanded and run; `$-` carries `s` and `i` | as predicted; `$-` now also in dash's letter order (`uaCvxsife`), which sh01's order was not |
| the maintainer's list works, `ls`/`date` straight to the terminal | as predicted (the demo) |
| interactive unless standard input is a regular file | as predicted; the pipe case is a named gap (PENDING) |
| PENDING: child stdin, `cd`, pipes, redirections, jobs, Ctrl-C, isatty, line editing | as predicted; 8 pending cases plus two named gaps without a case |
| at least 30 session cases, expected 35–40; 5–10 pending; identical verdicts on both tiers | **59** cases (more than expected), 8 pending, identical on both tiers |
| **RSS: 10–20 KB per command, 12–25 MB after 1,000** | **wrong by half**: 5.7–5.9 KB per command, 8.3–8.7 MB after 1,000. The shape held (linear, never returned; dash flat at 2.8 MB), and the falsifier's bounds (growth under 5 MB or over 40 MB) were not crossed — 5.7 MB grew |
| one wolf-lang finding (no interrupt meaning) | one: **wolf-lang#622** |

Not predicted, found by the work: the harness itself had a signal hole
(an inherited SIGINT ignore made dash's ^C rows meaningless until
`df942b5`), and the `read` built-in now answers 1 on a final line with
no newline, as the utility says (sh01 noted `read_line` could not tell).
