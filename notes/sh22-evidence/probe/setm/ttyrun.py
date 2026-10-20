#!/usr/bin/env python3
"""ttyrun — lane-local (sh22): run ARGV with a fresh pseudo-terminal as
its controlling terminal and standard input, output and error, and print
what the terminal received (CR stripped), then `exit N`. A probe of what
a shell does when it can open its terminal (dash's `set -m`)."""
import os, pty, select, subprocess, sys, termios, fcntl, time

def ctty():
    os.setsid()
    fcntl.ioctl(0, termios.TIOCSCTTY, 0)

m, s = pty.openpty()
p = subprocess.Popen(sys.argv[1:], stdin=s, stdout=s, stderr=s, preexec_fn=ctty, close_fds=True)
os.close(s)
out = b""
deadline = time.time() + 60
while time.time() < deadline:
    r, _, _ = select.select([m], [], [], 0.2)
    if r:
        try:
            d = os.read(m, 65536)
        except OSError:
            d = b""
        if not d:
            break
        out += d
    elif p.poll() is not None:
        # drain what is left
        try:
            while True:
                r, _, _ = select.select([m], [], [], 0.2)
                if not r:
                    break
                d = os.read(m, 65536)
                if not d:
                    break
                out += d
        except OSError:
            pass
        break
rc = p.wait()
sys.stdout.write(out.replace(b"\r", b"").decode("utf-8", "replace"))
print(f"exit {rc}")
