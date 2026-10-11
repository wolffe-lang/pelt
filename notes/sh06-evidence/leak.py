#!/usr/bin/env python3
"""leak — lane-local bisection of pelt's per-command memory at the prompt."""
import os, pty, select, subprocess, sys, time
ENV = {"PATH": "/usr/bin:/bin", "HOME": "/", "LC_ALL": "C", "PS1": "$ "}
def until(m, want):
    buf = b""; end = time.time() + 10
    while time.time() < end:
        r, _, _ = select.select([m], [], [], 0.01)
        if r:
            d = os.read(m, 65536)
            if not d: break
            buf += d
            if buf.endswith(want): return buf
    return buf
def hwm(pid):
    for ln in open(f"/proc/{pid}/status"):
        if ln.startswith("VmRSS:"): return int(ln.split()[1])
def run(shell, line, out_to_pty, n=3000):
    master, slave = pty.openpty()
    rp, wp = os.pipe()
    p = subprocess.Popen([shell, "-i"], stdin=slave, stdout=slave if out_to_pty else wp,
                         stderr=slave, env=ENV, start_new_session=True, close_fds=True)
    os.close(slave); os.close(wp)
    until(master, b"$ ")
    a = None
    for i in range(n):
        os.write(master, line + b"\n")
        until(master, b"$ ")
        while select.select([rp], [], [], 0)[0]:
            if not os.read(rp, 65536): break
        if i == 500: a = hwm(p.pid)
    b = hwm(p.pid)
    os.write(master, b"exit\n"); p.wait(timeout=5)
    return a, b, (b - a) * 1024 / (n - 501)
shell = sys.argv[1]
for line in [b":", b"x=1", b"x=$((x+1))", b"echo hi", b"echo $x", b"true; true", b"/bin/true"]:
    for tty in (True, False):
        a, b, per = run(shell, line, tty)
        print(f"{line.decode():<14} stdout={'pty ' if tty else 'pipe'}  rss@500 {a} KB  rss@3000 {b} KB  {per:7.1f} B/command", flush=True)
