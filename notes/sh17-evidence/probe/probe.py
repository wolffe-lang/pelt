#!/usr/bin/env python3
"""probe.py — sh17's black-box rows, run under each shell named.

usage: probe.py [--diff] ROWS NAME=SHELL [NAME=SHELL ...]

--diff prints only the rows where the shells part (exit, stderr presence,
stdout), then the count of rows alike.

ROWS is a text file of blocks, each starting `### name`; the block is a
script written to <scratch>/s.sh and run as `SHELL ../s.sh` from
<scratch>/w, with `../sh` a symbolic link to SHELL (so a row can start
the shell under test with options, and bash, named `sh`, takes its
POSIX mode), from the environment PATH=/usr/bin:/bin, HOME=/home/pelt,
LC_ALL=C, signals at their defaults, a 10 s limit. Prints, per row and
shell, the exit status, whether anything reached standard error, and
standard output (repr). Shells are run as programs; nothing here reads
any shell's source (rulings #42-#45).
"""
import os
import shutil
import signal
import subprocess
import sys
import tempfile

ENV = {"PATH": "/usr/bin:/bin", "HOME": "/home/pelt", "LC_ALL": "C"}


def defaults():
    for n in range(1, signal.NSIG):
        if n in (signal.SIGKILL, signal.SIGSTOP):
            continue
        try:
            signal.signal(n, signal.SIG_DFL)
        except (OSError, ValueError):
            pass
    signal.pthread_sigmask(signal.SIG_SETMASK, [])


def rows(path):
    out, name, body = [], None, []
    for line in open(path, encoding="utf-8"):
        if line.startswith("### "):
            if name:
                out.append((name, "".join(body)))
            name, body = line[4:].strip(), []
        elif name:
            body.append(line)
    if name:
        out.append((name, "".join(body)))
    return out


def run(shell, script):
    holder = tempfile.mkdtemp(prefix="sh17-probe.")
    try:
        with open(os.path.join(holder, "s.sh"), "w", encoding="utf-8") as fh:
            fh.write(script)
        w = os.path.join(holder, "w")
        os.mkdir(w)
        os.symlink(shell, os.path.join(holder, "sh"))
        argv = [shell] + (["--posix"] if os.path.basename(shell) == "bash" else []) + ["../s.sh"]
        try:
            p = subprocess.run(argv, cwd=w, env=dict(ENV), stdin=subprocess.DEVNULL,
                               capture_output=True, timeout=10, preexec_fn=defaults)
        except subprocess.TimeoutExpired:
            return None
        return p.returncode, bool(p.stderr), p.stdout, p.stderr
    finally:
        shutil.rmtree(holder, ignore_errors=True)


def main(argv):
    only_diff = argv[:1] == ["--diff"]
    if only_diff:
        argv = argv[1:]
    shells = [a.split("=", 1) for a in argv[1:]]
    if only_diff:
        # print only the rows where the shells do not all answer alike
        same = 0
        for name, script in rows(argv[0]):
            got = [run(os.path.abspath(sh) if os.sep in sh else shutil.which(sh), script)
                   for _, sh in shells]
            keys = [None if g is None else g[:3] for g in got]
            if all(k == keys[0] for k in keys):
                same += 1
                continue
            print(f"### {name}")
            for (sname, _), g in zip(shells, got):
                if g is None:
                    print(f"  {sname:5} TIMEOUT")
                else:
                    print(f"  {sname:5} exit={g[0]} err={'yes' if g[1] else 'no'} out={g[2]!r}")
        print(f"probe: {same} rows alike")
        return 0
    for name, script in rows(argv[0]):
        print(f"### {name}")
        for sname, sh in shells:
            r = run(os.path.abspath(sh) if os.sep in sh else shutil.which(sh), script)
            if r is None:
                print(f"  {sname:5} TIMEOUT")
                continue
            st, err, out, errt = r
            print(f"  {sname:5} exit={st} err={'yes' if err else 'no'} out={out!r}")
            if err and os.environ.get("PROBE_STDERR"):
                print(f"  {sname:5} stderr={errt!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
