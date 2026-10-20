"""lib_reap — a harness ends the whole tree of processes it started for a
case that timed out, and says how many it ended (pelt#27).

A case's timeout used to end one process: the one `subprocess` started.
Under `tools/syscall-census` that is `strace`, and a process whose tracer
dies is let go, not ended, so the shell went on running; under
`tools/difftest` alone the shell was ended and whatever it had started
went on (a `sleep`, a job in a group of its own). sh14 found three such
shells left on kasumi (notes/sh14-the-signals.md); sh22 saw both shapes
in a container (notes/sh22-evidence/logs/reap-base.log).

On linux the harness makes itself a CHILD SUBREAPER
(`prctl(PR_SET_CHILD_SUBREAPER)`, a process attribute, nothing global),
so every process a case starts stays its descendant however its parents
end: a shell whose tracer died, a job whose shell was ended, a process in
a group or a session of its own. On a timeout it reads the process table
from `/proc` — the case's process and everything below it, and every
process re-parented to the harness since the case began — sends each
`SIGKILL` by its recorded pid, reaps what it adopted, and reads again
until nothing of the tree is left. Elsewhere (macOS) the tree is read
from `ps` before the first kill; a process already orphaned before the
timeout is not found there, and says so in the count only by its
absence. Nothing is ever sent by name, pattern or process group, and
only to a descendant of the harness.

`PELT_REAP_LOG`, when set, names a file each ending is appended to (one
line: the case, how many, the pids), which `tools/syscall-census` adds
up.
"""

import ctypes
import os
import signal
import subprocess
import sys
import time

PR_SET_CHILD_SUBREAPER = 36
_reaper = {"on": None}


def subreaper():
    """Make this process a child subreaper (linux); whether it is."""
    if _reaper["on"] is not None:
        return _reaper["on"]
    on = False
    if sys.platform.startswith("linux"):
        try:
            libc = ctypes.CDLL(None, use_errno=True)
            on = libc.prctl(PR_SET_CHILD_SUBREAPER, 1, 0, 0, 0) == 0
        except (OSError, AttributeError):
            on = False
    _reaper["on"] = on
    return on


def _table():
    """{pid: (ppid, state)} of every process the host shows this one."""
    t = {}
    if os.path.isdir("/proc/self"):
        for d in os.listdir("/proc"):
            if not d.isdigit():
                continue
            try:
                with open(f"/proc/{d}/stat") as fh:
                    st = fh.read()
            except OSError:
                continue
            # `pid (comm) state ppid …`: the command may hold blanks and
            # parentheses, so the fields are read after the last `)`
            rest = st[st.rfind(")") + 2:].split()
            if len(rest) >= 2:
                t[int(d)] = (int(rest[1]), rest[0])
        return t
    out = subprocess.run(["ps", "-A", "-o", "pid=", "-o", "ppid=", "-o", "stat="],
                         capture_output=True, text=True).stdout
    for line in out.splitlines():
        f = line.split()
        if len(f) >= 3 and f[0].isdigit() and f[1].isdigit():
            t[int(f[0])] = (int(f[1]), f[2][:1])
    return t


def children():
    """The pids whose parent is this process: what a case finds there
    already is not its own. Only a subreaper adopts, so elsewhere there
    is nothing to read (and no `ps` a case)."""
    if not subreaper():
        return set()
    me = os.getpid()
    return {p for p, (pp, _s) in _table().items() if pp == me}


def _below(roots, table):
    kids = {}
    for p, (pp, _s) in table.items():
        kids.setdefault(pp, []).append(p)
    seen = set()
    todo = list(roots)
    while todo:
        p = todo.pop()
        if p in seen or p not in table:
            continue
        seen.add(p)
        todo.extend(kids.get(p, []))
    return seen


def _reap(pids):
    for p in pids:
        try:
            os.waitpid(p, os.WNOHANG)
        except ChildProcessError:
            pass
        except OSError:
            pass


def end_tree(root, before=frozenset()):
    """End `root` (a process this harness started and has not yet waited
    for) and every process below it, and every process re-parented to
    this harness that was not its child when the case began (`before`,
    from `children()`). Answers the pids ended: the ones alive when the
    signal was sent. `root` itself is left for its owner to wait for."""
    me = os.getpid()
    ended = set()
    for _ in range(200):
        table = _table()
        adopted = {p for p, (pp, _s) in table.items()
                   if pp == me and p not in before and p != root}
        live = {p for p in _below({root} | adopted, table)
                if table[p][1] != "Z" and p != me}
        # the adopted ones that have already ended are reaped here
        _reap(p for p in adopted if table[p][1] == "Z")
        if not live:
            break
        for p in sorted(live):
            try:
                os.kill(p, signal.SIGKILL)
                ended.add(p)
            except ProcessLookupError:
                pass
            except PermissionError:
                pass
        time.sleep(0.02)
    return ended


def reap_adopted(before=frozenset()):
    """Reap the processes re-parented to this harness that have ended
    (a case's background job that outlived its shell), so none waits as
    a zombie; `before` are children that are not the harness's to reap.
    Nothing to do where the harness adopts nothing."""
    if not subreaper():
        return
    me = os.getpid()
    _reap(p for p, (pp, s) in _table().items() if pp == me and s == "Z" and p not in before)


def note(what, pids):
    """Say an ending in `$PELT_REAP_LOG`, when set."""
    path = os.environ.get("PELT_REAP_LOG")
    if not path:
        return
    with open(path, "a") as fh:
        fh.write(f"{what} ended {len(pids)}: {' '.join(str(p) for p in sorted(pids))}\n")
