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
