#!/usr/bin/env python3
"""sh20: type LINE into `SHELL -i -m` on a pty, then `exit`; print what
the shell wrote, prompts and echo removed as far as a reader needs.
usage: typein.py SHELL LINE [LINE...]"""
import os, pty, select, sys, time
sh, lines = sys.argv[1], sys.argv[2:]
pid, fd = pty.fork()
if pid == 0:
    # a login's defaults: python ignores PIPE and XFSZ, which a child
    # would otherwise start with
    import signal
    for n in range(1, signal.NSIG):
        if n in (signal.SIGKILL, signal.SIGSTOP):
            continue
        try:
            signal.signal(n, signal.SIG_DFL)
        except (OSError, ValueError):
            pass
    signal.pthread_sigmask(signal.SIG_SETMASK, [])
    os.environ["PS1"] = "$ "
    os.execvp(sh, [sh, "-i", "-m"])
out = b""
def drain(t):
    global out
    end = time.time() + t
    while time.time() < end:
        r, _, _ = select.select([fd], [], [], 0.05)
        if r:
            try:
                b = os.read(fd, 4096)
            except OSError:
                return
            if not b:
                return
            out += b
drain(0.5)
for l in lines + ["exit"]:
    os.write(fd, (l + "\n").encode())
    drain(3.0)
os.waitpid(pid, 0)
for l in out.decode(errors="replace").replace("\r", "").splitlines():
    if ": ign=" in l or "bg-trap-int" in l or l.startswith("flags"):
        print(l[l.find(l.split(":")[0]):])
