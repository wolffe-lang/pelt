"""lib_cases — what a differential case is, shared by tools/difftest and
tools/oracle-record.

A case is three files in tests/diff/<area>/:

  <name>.sh    the script
  <name>.out   the oracle's standard output, byte for byte
  <name>.meta  key=value lines:
                 exit=N          the oracle's exit status
                 stderr=yes|no   whether the oracle wrote to standard error
                                 (compared by presence only: pelt's
                                 messages are its own)
                 mode=script|parse|stdin
                                 script (default): `SHELL ../s.sh ARGS`
                                 parse: `SHELL -n ../s.sh`, and `line=N`
                                 is the line the oracle refused at
                                 stdin: `SHELL` with no operand and the
                                 script on standard input (a pipe): the
                                 shell must not take itself for
                                 interactive (XCU `sh`)
                 line=N          parse rows only
                 args=a b c      optional operands, split on blanks
                 stdin=TEXT      optional standard input (\\n for newline)
                 oracle=dash|bash  whose answer this is (default dash;
                                 bash means `bash --posix`, used only where
                                 POSIX.1-2024 and dash part, and said why)
                 bash=agree|differs
                                 the second opinion, recorded by
                                 oracle-record
                 pending=WHAT    the case needs a primitive pelt does not
                                 have yet; listed in PENDING.md by name
                 why=TEXT        free text

Every case runs in a fresh scratch directory: the script is copied to
<scratch>/s.sh and the shell runs with <scratch>/w as its working
directory, so `../s.sh` is the same $0 on every host and a glob sees
only what the case made; `../sh` is a link to the shell under test. The environment is built from nothing:
PATH=/usr/bin:/bin, HOME=/home/pelt, LC_ALL=C.
"""

import os
import re
import shutil
import signal
import subprocess
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# $PELT_DIFF_DIR points the tools at another corpus (the self-test's).
DIFF = os.environ.get("PELT_DIFF_DIR") or os.path.join(ROOT, "tests", "diff")
ENV = {"PATH": "/usr/bin:/bin", "HOME": "/home/pelt", "LC_ALL": "C"}


def read_meta(path):
    meta = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            k, _, v = line.partition("=")
            meta[k.strip()] = v
    return meta


def write_meta(path, meta):
    order = ["mode", "exit", "line", "stderr", "args", "stdin", "oracle",
             "bash", "pending", "why"]
    keys = [k for k in order if k in meta] + sorted(
        k for k in meta if k not in order)
    with open(path, "w", encoding="utf-8") as fh:
        for k in keys:
            fh.write(f"{k}={meta[k]}\n")


def cases(areas=None):
    """Every case as (area, name, script path), sorted. `areas` names
    areas, or single cases as `area/name`."""
    out = []
    for area in sorted(os.listdir(DIFF)):
        d = os.path.join(DIFF, area)
        whole = not areas or area in areas
        if not os.path.isdir(d) or not (whole or any(a.startswith(area + "/") for a in areas)):
            continue
        for f in sorted(os.listdir(d)):
            if f.endswith(".sh") and (whole or f"{area}/{f[:-3]}" in areas):
                out.append((area, f[:-3], os.path.join(d, f)))
    return out


LINE = re.compile(rb"(?:: |line )(\d+):")


def _default_signals():
    """Start the shell as a login would: the signals a case traps or
    sends at their defaults and nothing blocked. A harness started in
    the background of a non-interactive shell, or under `nohup`,
    inherits SIGINT, SIGQUIT or SIGHUP IGNORED, and a shell may not trap
    a signal that was ignored when it started (XCU `trap`): the oracle
    and pelt would both answer for the harness's parent, not the case."""
    for s in (signal.SIGHUP, signal.SIGINT, signal.SIGQUIT, signal.SIGTERM,
              signal.SIGPIPE, signal.SIGUSR1, signal.SIGUSR2, signal.SIGALRM):
        signal.signal(s, signal.SIG_DFL)
    signal.pthread_sigmask(signal.SIG_SETMASK, [])


def run(shell, script, meta, timeout=10):
    """Run one case under `shell` (an argv prefix). Answers a dict with
    stdout, exit, stderr (bool), line (parse rows), or None on a
    timeout."""
    holder = tempfile.mkdtemp(prefix="pelt-case.")
    try:
        s = os.path.join(holder, "s.sh")
        shutil.copyfile(script, s)
        w = os.path.join(holder, "w")
        os.mkdir(w)
        # `../sh` is the shell under test, for a case about how a shell
        # starts (its environment, `-c`, `-s`, options): a symbolic link
        # named `sh`, so bash takes its POSIX mode from the name.
        real = shutil.which(shell[0]) or shell[0]
        os.symlink(os.path.abspath(real), os.path.join(holder, "sh"))
        argv = list(shell)
        data = None
        if meta.get("mode") == "parse":
            argv += ["-n", "../s.sh"]
        elif meta.get("mode") == "stdin":
            data = open(script, "rb").read()
        else:
            argv += ["../s.sh"] + meta.get("args", "").split()
        if "stdin" in meta and meta.get("mode") != "stdin":
            data = meta["stdin"].replace("\\n", "\n").encode()
        try:
            p = subprocess.run(argv, cwd=w, env=dict(ENV), input=data,
                               stdin=None if data is not None
                               else subprocess.DEVNULL,
                               capture_output=True, timeout=timeout,
                               preexec_fn=_default_signals)
        except subprocess.TimeoutExpired:
            return None
        code = p.returncode if p.returncode >= 0 else 128 - p.returncode
        res = {"stdout": p.stdout, "exit": code, "stderr": bool(p.stderr),
               "err": p.stderr}
        m = LINE.search(p.stderr)
        res["line"] = int(m.group(1)) if m else 0
        return res
    finally:
        shutil.rmtree(holder, ignore_errors=True)
