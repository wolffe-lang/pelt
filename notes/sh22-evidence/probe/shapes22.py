#!/usr/bin/env python3
"""shapes22 — lane-local (sh22): shape-rss's own measurement (tools/shape-rss's
run_file / run_typed: peak RSS at N and 2N turns, the answer checked) over
pelt#39's five built-ins, the job slot, and their controls; sh19's
bgshapes.py with sh22's rows.
usage: shapes22.py [-n N] [--only a,b] SHELL...
One row per shell and shape: KB at N, KB at 2N, bytes a turn.
"""
import importlib.machinery, importlib.util, os, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.environ.get("PELT_TOOLS") or os.path.join(HERE, "..", "..", "..", "tools")
loader = importlib.machinery.SourceFileLoader("shape_rss", os.path.join(TOOLS, "shape-rss"))
spec = importlib.util.spec_from_loader("shape_rss", loader)
sr = importlib.util.module_from_spec(spec)
sys.path.insert(0, TOOLS)
loader.exec_module(sr)

SHAPES = [
    # the controls: the bare loop, and a built-in sh19 brought down
    ("ctl-loop", "loop", ":"),
    ("ctl-wait", "loop", "wait"),
    # pelt#39's five, as sh19 measured them (notes/sh19-the-leak-and-the-ci.md §7)
    ("bi-read", "loop", "read x </dev/null"),
    ("bi-eval", "loop", "eval :"),
    ("bi-cd", "loop", "cd ."),
    ("bi-command", "loop", "command true"),
    ("bi-umask", "loop", "umask 022"),
    # their neighbours: the same built-ins another way
    ("bi-read-here", "loop", "read x <<E\nv\nE"),
    ("bi-eval-arg", "loop", "eval 'y=1'"),
    ("bi-cd-dir", "loop", "cd /"),
    ("bi-command-v", "loop", "command -v true >/dev/null"),
    ("bi-umask-print", "loop", "umask >/dev/null"),
    ("bi-jobs", "loop", "jobs"),
    ("bi-redir", "loop", "true >/dev/null"),
    # the job slot: a job nobody waits for (pelt#39's second half)
    ("bg-builtin-nowait", "loop", "true &"),
    ("bg-program-nowait", "loop", "env true &"),
    ("script-bg-builtin-nowait", "script", "true &"),
]


def main(argv):
    n = 10000
    only = None
    while argv[:1] in (["-n"], ["--only"]):
        if argv[0] == "-n":
            n = int(argv[1])
        else:
            only = set(argv[1].split(","))
        argv = argv[2:]
    for shell in argv:
        shell = os.path.abspath(shell) if os.sep in shell else shell
        for name, kind, text in SHAPES:
            if only is not None and name not in only:
                continue
            if kind == "typed":
                rows, ok, why = sr.run_typed(shell, text, n)
            else:
                rows, ok, why = [], True, ""
                with tempfile.TemporaryDirectory(prefix="shapes22.") as cwd:
                    for size in (n, 2 * n):
                        kb, good, why = sr.run_file(shell, kind, text, size, cwd)
                        rows.append(kb)
                        ok = ok and good
            grew = rows[1] - rows[0]
            per = grew * 1024 // n
            print(f"shapes22: {os.path.basename(shell):22} {name:24} {kind:6} {n:>6} {rows[0]:>8} KB "
                  f"{2 * n:>6} {rows[1]:>8} KB grew {grew:>7} KB ({per} B a turn) "
                  f"{'ok' if ok else 'WRONG ' + why} [{text!r}]", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
