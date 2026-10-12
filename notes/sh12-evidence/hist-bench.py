#!/usr/bin/env python3
"""hist-bench — what the history costs, measured from outside (sh12).

pelt runs interactively on a pseudo-terminal (tools/lib_session.py's
arrangement, the line editor on). Three numbers:

  prompt   Enter to the next prompt for `:`, N lines: with no history
           file (HOME=/, so $HOME/.sh_history cannot be made) and with
           one (HISTFILE in a scratch directory): median and p99, ms
  start    spawn to the first prompt with HISTSIZE=32767 and a history
           file of 0 and of 32,767 entries: median of R runs, ms
  ctrl-r   with that full file: Ctrl-R then `z` (no line holds it, so the
           whole list is searched) until the screen answers, R times:
           median and p99, ms

usage: hist-bench.py [-n N] [-r R] PELT
"""

import os
import pty
import select
import shutil
import statistics
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
import lib_session as ls  # noqa: E402


class Sh:
    def __init__(self, pelt, env):
        self.master, slave = pty.openpty()
        rout, wout = os.pipe()
        self.rerr, werr = os.pipe()
        base = {"PATH": "/usr/bin:/bin", "HOME": "/", "LC_ALL": "C", "PS1": "$ ", "COLUMNS": "200"}
        base.update(env)
        self.t0 = time.perf_counter()
        self.p = subprocess.Popen([pelt, "-i"], stdin=slave, stdout=wout, stderr=werr, env=base,
                                  start_new_session=True, preexec_fn=ls._ctty, close_fds=True)
        os.close(slave)
        os.close(wout)
        os.close(werr)
        self.rout = rout
        self.prompts = 0
        self.err = b""

    def wait_prompt(self):
        want = self.prompts + 1
        while self.err.count(b"$ ") < want:
            r, _, _ = select.select([self.rerr, self.master, self.rout], [], [], 5)
            if not r:
                raise RuntimeError("no prompt")
            for fd in r:
                d = os.read(fd, 65536)
                if fd == self.rerr:
                    self.err += d
        self.prompts = want

    def drain_tty(self, until, secs=5):
        """Read the terminal until `until` has been seen."""
        got = b""
        end = time.time() + secs
        while until not in got and time.time() < end:
            r, _, _ = select.select([self.master, self.rerr], [], [], 1)
            for fd in r:
                d = os.read(fd, 65536)
                if fd == self.master:
                    got += d
                else:
                    self.err += d
        return got

    def quit(self):
        os.write(self.master, b"\x15exit\r")
        self.p.wait(10)


def pct(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(len(xs) * p))]


def prompt_cost(pelt, env, n):
    sh = Sh(pelt, env)
    sh.wait_prompt()
    ts = []
    for _ in range(n):
        t = time.perf_counter()
        os.write(sh.master, b":\r")
        sh.wait_prompt()
        ts.append((time.perf_counter() - t) * 1000)
    sh.quit()
    return statistics.median(ts), pct(ts, 0.99)


def start_cost(pelt, env, reps, pristine):
    ts = []
    for _ in range(reps):
        # each run reads the same file (the last one appended `exit`)
        shutil.copyfile(pristine, env["HISTFILE"])
        sh = Sh(pelt, env)
        sh.wait_prompt()
        ts.append((time.perf_counter() - sh.t0) * 1000)
        sh.quit()
    return statistics.median(ts)


def ctrl_r_cost(pelt, env, reps):
    sh = Sh(pelt, env)
    sh.wait_prompt()
    ts = []
    for _ in range(reps):
        os.write(sh.master, b"\x12")
        sh.drain_tty(b"(search '') ")
        t = time.perf_counter()
        os.write(sh.master, b"z")
        sh.drain_tty(b"(failed search 'z') ")
        ts.append((time.perf_counter() - t) * 1000)
        os.write(sh.master, b"\x07")
        sh.drain_tty(b"\x1b[J", 0.3)
    sh.quit()
    return statistics.median(ts), pct(ts, 0.99)


def main(argv):
    n, reps = 500, 20
    while argv[:1] in (["-n"], ["-r"]):
        if argv[0] == "-n":
            n = int(argv[1])
        else:
            reps = int(argv[1])
        argv = argv[2:]
    pelt = os.path.abspath(argv[0])
    d = tempfile.mkdtemp(prefix="pelt-hist-bench.")
    try:
        m, p = prompt_cost(pelt, {}, n)
        print(f"prompt, no file:          median {m:.3f} ms  p99 {p:.3f} ms  ({n} lines)")
        m, p = prompt_cost(pelt, {"HISTFILE": os.path.join(d, "h")}, n)
        print(f"prompt, HISTFILE:         median {m:.3f} ms  p99 {p:.3f} ms  ({n} lines)")
        empty = os.path.join(d, "empty")
        open(empty, "wb").close()
        full = os.path.join(d, "full")
        with open(full, "wb") as fh:
            for i in range(32767):
                fh.write(b"echo line %d of the history\n" % i)
        big = {"HISTSIZE": "32767"}
        run = os.path.join(d, "run")
        s0 = start_cost(pelt, dict(big, HISTFILE=run), reps, empty)
        s1 = start_cost(pelt, dict(big, HISTFILE=run), reps, full)
        print(f"start, empty file:        median {s0:.1f} ms  ({reps} runs)")
        print(f"start, 32,767 entries:    median {s1:.1f} ms  ({reps} runs; +{s1 - s0:.1f} ms)")
        shutil.copyfile(full, run)
        m, p = ctrl_r_cost(pelt, dict(big, HISTFILE=run), reps)
        print(f"Ctrl-R z over 32,767:     median {m:.2f} ms  p99 {p:.2f} ms  ({reps} searches)")
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
