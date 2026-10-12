#!/usr/bin/env python3
"""drive_chars — run the term_chars witness on a fresh pty.

usage: drive_chars.py PATH-TO-term_chars
The driver waits for `ready`, then through the master side sets the
interrupt character to Ctrl-X and turns IXON off then on again (the
terminal's settings are one object; either side may set them), types
Ctrl-S, a, Ctrl-V, b, Ctrl-O, c with IXON on and IEXTEN as the pty
starts (on), and prints what the witness says.
"""
import os, pty, select, subprocess, sys, termios, time

def main(path):
    master, slave = pty.openpty()
    p = subprocess.Popen([path], stdin=slave, stdout=slave, stderr=slave,
                         start_new_session=True, close_fds=True)
    os.close(slave)
    out = b""
    end = time.time() + 5
    while b"ready" not in out and time.time() < end:
        if select.select([master], [], [], 0.05)[0]:
            out += os.read(master, 4096)
    a = termios.tcgetattr(master)
    print(f"pty at start: IXON {bool(a[0] & termios.IXON)}, IEXTEN {bool(a[3] & termios.IEXTEN)}, VINTR {a[6][termios.VINTR]!r}")
    a[6][termios.VINTR] = b"\x18"
    a[0] &= ~termios.IXON
    termios.tcsetattr(master, termios.TCSANOW, a)
    a[0] |= termios.IXON
    termios.tcsetattr(master, termios.TCSANOW, a)
    for b in (b"\x13", b"a", b"\x16", b"b", b"\x0f", b"c"):
        os.write(master, b)
        time.sleep(0.1)
    os.write(master, b"\x11")
    end = time.time() + 5
    while p.poll() is None and time.time() < end:
        if select.select([master], [], [], 0.05)[0]:
            try:
                out += os.read(master, 4096)
            except OSError:
                break
    p.wait(timeout=5)
    for line in out.decode("utf-8", "replace").splitlines():
        print("   " + repr(line))
    print("typed: 19 (Ctrl-S) 97 22 (Ctrl-V) 98 15 (Ctrl-O) 99, then 17 (Ctrl-Q)")

main(sys.argv[1])
