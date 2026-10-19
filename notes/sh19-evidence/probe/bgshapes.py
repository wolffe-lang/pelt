#!/usr/bin/env python3
"""bgshapes — lane-local (sh19): shape-rss's measurement over the
background shapes of pelt#33, and their controls.

Uses tools/shape-rss's own run_file / run_typed (the same peak-RSS and
typed-RSS method, the same answer check), with a list of shapes of its
own. usage: bgshapes.py [-n N] [--set bg|builtins] [--only a,b] SHELL...
Prints one row per shell and shape: KB at N, KB at 2N, bytes a turn.
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
    ("ctl-wait", "loop", "wait"),
    ("ctl-program", "loop", "env true"),
    ("bg-builtin-wait", "loop", "true & wait"),
    ("bg-program-wait", "loop", "env true & wait"),
    ("bg-program-wait-pid", "loop", "env true & wait $!"),
    ("bg-subshell-wait", "loop", "( true ) & wait"),
    ("bg-brace-wait", "loop", "{ true; } & wait"),
    ("bg-builtin-nowait", "loop", "true &"),
    ("bg-program-nowait", "loop", "env true &"),
    ("script-bg-program-wait", "script", "env true & wait"),
    ("script-bg-builtin-wait", "script", "true & wait"),
    ("typed-bg-program-wait", "typed", "env true & wait"),
    ("typed-bg-builtin-wait", "typed", "true & wait"),
]

# --set builtins: the other built-ins the fast path does not serve, for
# scale (each one the ordinary path, `run_slow`)
BUILTINS = [
    ("bi-cd", "loop", "cd ."),
    ("bi-export", "loop", "export X"),
    ("bi-read", "loop", "read x </dev/null"),
    ("bi-set", "loop", "set -- a"),
    ("bi-unset", "loop", "unset y"),
    ("bi-kill0", "loop", "kill -0 $$"),
    ("bi-jobs", "loop", "jobs"),
    ("bi-command", "loop", "command true"),
    ("bi-eval", "loop", "eval :"),
    ("bi-umask", "loop", "umask 022"),
]


def main(argv):
    n = 10000
    only = None
    shapes = SHAPES
    while argv[:1] in (["-n"], ["--only"], ["--set"]):
        if argv[0] == "-n":
            n = int(argv[1])
        elif argv[0] == "--set":
            shapes = BUILTINS if argv[1] == "builtins" else SHAPES
        else:
            only = set(argv[1].split(","))
        argv = argv[2:]
    for shell in argv:
        shell = os.path.abspath(shell) if os.sep in shell else shell
        for name, kind, text in shapes:
            if only is not None and name not in only:
                continue
            if kind == "typed":
                rows, ok, why = sr.run_typed(shell, text, n)
            else:
                rows, ok, why = [], True, ""
                with tempfile.TemporaryDirectory(prefix="bgshapes.") as cwd:
                    for size in (n, 2 * n):
                        kb, good, why = sr.run_file(shell, kind, text, size, cwd)
                        rows.append(kb)
                        ok = ok and good
            grew = rows[1] - rows[0]
            per = grew * 1024 // n
            print(f"bgshapes: {os.path.basename(shell):22} {name:24} {kind:6} {n:>6} {rows[0]:>8} KB "
                  f"{2 * n:>6} {rows[1]:>8} KB grew {grew:>7} KB ({per} B a turn) "
                  f"{'ok' if ok else 'WRONG ' + why} [{text}]", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
