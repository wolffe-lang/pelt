#!/usr/bin/env python3
"""pend — lane-local: stamp pending= into the census cases' metas and
rewrite the census section of tests/diff/PENDING.md."""
import os, sys
ROOT = sys.argv[1]
DIFF = os.path.join(ROOT, "tests", "diff")
here = os.path.dirname(os.path.abspath(__file__))
tags = {}
for line in open(os.path.join(here, "pending.tsv")):
    c, t = line.rstrip("\n").split("\t")
    tags[c] = t
DESC = [
 # tag, what is missing, whose work / what it waits on
 ("test-file-primaries", "`test -x` is false for an executable regular file and `-r`/`-w` ignore the permission bits; no `-L`/`-h`; `-b`, `-p`, `-S` answer true for any file; `-u`, `-g`, `-ef` missing; `-nt`/`-ot` with a missing file", "pelt (sh06 issue P01); permission bits come from `fs_stat` (wolf 0.2.27), the caller's identity from wolf-lang#633"),
 ("sh-option-parsing", "`sh -ec 'cmd'` (option letters joined with `c`), `--`, and `-s -`", "pelt (P02)"),
 ("alias", "`alias`, `unalias`, alias substitution (XCU 2.3.1), and `command -v` of an alias or of a file that is not executable", "pelt (P03)"),
 ("type", "`type`", "pelt (P04)"),
 ("hash", "`hash`", "pelt (P04)"),
 ("command-p", "`command -p`", "pelt (P04)"),
 ("dollar-single-quote", "`$'…'` (XCU 2.2.4, new in POSIX.1-2024)", "pelt (P05)"),
 ("pipefail", "`set -o pipefail` is accepted and does nothing (XCU 2.9.2)", "pelt (P06)"),
 ("assignment-order", "`x=3 y=$x` on one command: the second assignment does not see the first (XCU 2.9.1.1)", "pelt (P07)"),
 ("star-in-assignment", "`x=$*` does not join with the first character of IFS (XCU 2.5.2)", "pelt (P07)"),
 ("declaration-utility", "`export x=$y` and `readonly x=$y` split and do not tilde-expand after `=` (declaration utilities, XCU 2.9.1.1; new in POSIX.1-2024)", "pelt (P07)"),
 ("read-trailing-delimiter", "`IFS=: read a b c` on `a:b:c:` leaves the trailing delimiter in the last variable", "pelt (P08)"),
 ("readonly-read-getopts", "`read` and `getopts` into a readonly variable, and `read` into an invalid name, answer 0", "pelt (P08)"),
 ("read-d", "`read -d delim` (new in POSIX.1-2024)", "pelt (P08)"),
 ("read-no-var", "`read` with no variable (unspecified by POSIX; dash refuses, pelt reads)", "pelt, with P08; not counted in the census"),
 ("command-special", "`command .`/`command set`/`command exec` with an error still ends the shell (XCU 2.8.1 note 1)", "pelt (P09)"),
 ("builtin-dashdash", "`export -- name` and `printf -- format`: `--` is taken as an operand", "pelt (P09)"),
 ("exit-in-exit-trap", "`exit` with no operand inside an EXIT trap action uses the action's last status, not the status from before the trap", "pelt (P09)"),
 ("readonly-p-unset", "`readonly -p` omits a readonly variable that has no value", "pelt (P09)"),
 ("pwd-bad-option", "`pwd -x` answers 0", "pelt (P09)"),
 ("cd-e", "`cd -P -e` (new in POSIX.1-2024)", "pelt (P09)"),
 ("pwd-from-env", "`PWD` is not taken from the environment at start, so a shell started in a directory reached through a symbolic link reports the physical path (XCU 2.5.3)", "pelt (P09)"),
 ("printf-partial-number", "`printf %d 12x` prints 0 where the leading digits are the value", "pelt (P09)"),
 ("printf-float", "`printf` `%e %f %g` (optional in POSIX; dash has them and configure scripts use `%f`)", "pelt (P09); wolf has float formatting"),
 ("printf-numbered", "`printf '%2$s'` (new in POSIX.1-2024; neither oracle has it)", "not counted in the census"),
 ("trap-p", "`trap -p` (new in POSIX.1-2024)", "pelt (P10)"),
 ("trap-in-cmdsub", "`$(trap)` shows nothing where it must show the invoking shell's traps", "pelt (P10)"),
 ("ps4-expansion", "`PS4` is written as is, not parameter-expanded (XCU 2.5.3)", "pelt (P10)"),
 ("xtrace-assignment", "`set -x` does not trace a command that is only assignments", "pelt (P10)"),
 ("verbose", "`set -v` writes nothing", "pelt#6"),
 ("notify-flag", "`set -o notify` does not put `b` in `$-`", "pelt (P10)"),
 ("dq-brace-escape", "`\"${x:-a\\}b}\"` keeps the backslash (XCU 2.2.3)", "pelt (P11)"),
 ("bracket-slash", "`${x##*[/]}`: a bracket expression holding a slash is not one outside pathname expansion too (XCU 2.14.3 restricts that rule to file names)", "pelt (P11)"),
 ("path-skips-non-executable", "a PATH search stops at a file that is not executable instead of going on to the next directory", "pelt (P11)"),
 ("arith-increment", "`$((++x))`: dash reads two unary pluses, pelt refuses it (`++` is optional in POSIX)", "pelt, a ruling (R4); not counted in the census"),
 ("special-name-function", "a function named after a special built-in is accepted (dash refuses; unspecified by POSIX)", "not counted in the census"),
 ("fork", "a compound command or function after `&`, and every pipeline stage pelt runs itself, runs to its end before the shell goes on: no concurrency, no SIGPIPE to a shell-written producer, a subshell is not a process (XCU 2.9.2, 2.9.3.1, 2.13)", "wolf-lang: a fork (sh06 issue W01), or pelt re-executing itself per subshell (ruling R1)"),
 ("umask", "`umask`", "wolf-lang `os_umask` (s230, merged for the release after 0.2.27), then pelt"),
 ("ulimit", "`ulimit`", "wolf-lang: no `getrlimit`/`setrlimit` surface (W02)"),
 ("kill", "`kill` as a built-in: `kill -l`, exit statuses, a signal to the shell's own pid", "wolf-lang#141 (a signal to any pid), then pelt"),
 ("job-ids", "`wait %1`, `kill %1`", "pelt once `kill` is a built-in (wolf-lang#141)"),
 ("jobs", "`jobs`, `jobs -p`", "pelt (P12); job states need wolf-lang W03"),
 ("job-control", "`set -m`: a process group per job", "wolf-lang: stop reporting, `SIGCONT`, a signal to a group, an interruptible wait (W03, wolf-lang#680)"),
 ("getppid", "`PPID`", "wolf-lang#141 (it asks for getpid; getppid is the same lane)"),
 ("ignored-on-entry", "a signal ignored when the shell started can be trapped", "wolf-lang#681"),
 ("uid", "`test -O`, `test -G`", "wolf-lang#633"),
 ("history", "`fc` (the case passes today only because a shell with no history and a shell with no `fc` both fail)", "pelt (sh08)"),
]
known = {d[0] for d in DESC} | {"getpid", "signal meaning", "interruptible wait", "user database"}
for c, t in tags.items():
    assert t in known, t
    mp = os.path.join(DIFF, c + ".meta")
    lines = [l for l in open(mp).read().split("\n") if l and not l.startswith("pending=")]
    lines.append(f"pending={t}")
    open(mp, "w").write("\n".join(lines) + "\n")
# drop a stale pending from census cases no longer listed
for area in os.listdir(DIFF):
    d = os.path.join(DIFF, area)
    if not os.path.isdir(d): continue
    for f in os.listdir(d):
        if f.startswith("c_") and f.endswith(".meta") and f"{area}/{f[:-5]}" not in tags:
            mp = os.path.join(d, f)
            s = open(mp).read()
            if "pending=" in s:
                open(mp, "w").write("\n".join(l for l in s.split("\n") if l and not l.startswith("pending=")) + "\n")
out = ["<!-- census:begin -->", "## The census cases (sh06)", "",
       "Cases named `c_*` were written by the clause census (`docs/CENSUS.md`,",
       "`tests/census/clauses.tsv`). The ones pelt does not answer as POSIX.1-2024",
       "requires are pending here, by what they wait on. \"P01\"… and \"W01\"… are",
       "the issue texts in the sh06 report (`notes/sh06-the-census.md`).", "",
       "| waits on | what is missing | whose work | cases |", "|---|---|---|---|"]
extra = [("getpid", "`$$` off linux (the cases pass on linux)", "wolf-lang#141"),
         ("signal meaning", "a trap for `USR1`, `ALRM`, `PIPE`, `ABRT`, `WINCH`, `CONT`: the shell dies or ignores where the action must run", "wolf-lang#679, #423"),
         ("interruptible wait", "`wait` cut short by a trapped signal", "wolf-lang#680"),
         ("user database", "`~login`", "wolf-lang: no `getpwnam` surface (W04)")]
for tag, what, who in DESC + extra:
    cs = sorted(c for c, t in tags.items() if t == tag)
    if cs:
        out.append(f"| **{tag}** | {what} | {who} | " + ", ".join(f"`{c}`" for c in cs) + " |")
out += ["<!-- census:end -->"]
p = os.path.join(DIFF, "PENDING.md")
s = open(p).read()
if "<!-- census:begin -->" in s:
    a, _, rest = s.partition("<!-- census:begin -->")
    _, _, b = rest.partition("<!-- census:end -->")
    s = a + "\n".join(out) + b
else:
    marker = "**No case, named:**"
    assert marker in s
    s = s.replace(marker, "\n".join(out) + "\n\n" + marker)
open(p, "w").write(s)
print(len(tags), "pending census cases")
