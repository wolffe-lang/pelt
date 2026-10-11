#!/usr/bin/env python3
"""drive — run the sh06 terminal witnesses through a pseudo-terminal.

usage: drive.py DIR   (DIR holds the four built witnesses)
Each witness is started with a fresh pty as its controlling terminal;
this program plays the terminal (it answers a cursor-position request
as an 80x24 screen would), types, resizes and signals, and prints what
the witness wrote.
"""
import fcntl, os, pty, select, signal, struct, subprocess, sys, termios, time

def start(path, rows=24, cols=80):
    master, slave = pty.openpty()
    fcntl.ioctl(master, termios.TIOCSWINSZ, struct.pack("HHHH", rows, cols, 0, 0))
    def ctty():
        fcntl.ioctl(0, termios.TIOCSCTTY, 0)
        for s in (signal.SIGINT, signal.SIGQUIT):
            signal.signal(s, signal.SIG_DFL)
    p = subprocess.Popen([path], stdin=slave, stdout=slave, stderr=slave,
                         start_new_session=True, preexec_fn=ctty, close_fds=True)
    os.close(slave)
    return p, master

def pump(master, secs, on=None):
    out = b""
    end = time.time() + secs
    while time.time() < end:
        r, _, _ = select.select([master], [], [], 0.05)
        if r:
            try:
                d = os.read(master, 4096)
            except OSError:
                break
            if not d:
                break
            out += d
            if on:
                on(out)
    return out

def show(name, out):
    print(f"== {name}")
    for line in out.replace(b"\r", b"").split(b"\n"):
        if line.strip():
            print("   " + repr(line.decode("utf-8", "replace")))

def state(pid):
    r = subprocess.run(["ps", "-o", "stat=", "-p", str(pid)], capture_output=True, text=True)
    return r.stdout.strip()

def main(d):
    # 1. term_keys: answer the cursor report, type a, ESC [ D as three bytes
    p, m = start(os.path.join(d, "term_keys"), 24, 80)
    answered = [False]
    def on(out):
        if b"\x1b[6n" in out and not answered[0]:
            answered[0] = True
            os.write(m, b"\x1b[24;80R")
            time.sleep(0.3)
            os.write(m, b"a")
            time.sleep(0.1)
            os.write(m, b"\x1b[")
    out = pump(m, 3, on)
    p.wait(timeout=5)
    show("term_keys", out.replace(b"\x1b", b"<ESC>"))
    # 2. winch: resize twice while it polls
    p, m = start(os.path.join(d, "winch"))
    out = pump(m, 1)
    for size in ((30, 100), (40, 120)):
        fcntl.ioctl(m, termios.TIOCSWINSZ, struct.pack("HHHH", size[0], size[1], 0, 0))
        out += pump(m, 1)
    out += pump(m, 4)
    p.wait(timeout=10)
    show("winch (resized to 30x100, then 40x120)", out)
    # 3. stop_report: the child stops; the witness stays in its wait
    p, m = start(os.path.join(d, "stop_report"))
    out = pump(m, 2)
    child = int(out.split()[1])
    print("== stop_report")
    print(f"   after 2 s: child {child} state {state(child)!r}, witness state {state(p.pid)!r}, witness has printed {out.strip().decode()!r} only")
    os.kill(child, signal.SIGCONT)
    out2 = pump(m, 2)
    p.wait(timeout=5)
    show("stop_report, after the driver sent SIGCONT", out2)
    # 4. read_vs_signal
    p, m = start(os.path.join(d, "read_vs_signal"))
    out = pump(m, 1)
    os.kill(p.pid, signal.SIGINT)
    out += pump(m, 2)
    alive = p.poll() is None
    print("== read_vs_signal")
    print(f"   2 s after SIGINT: witness still in its read: {alive}; printed so far {out.strip().decode()!r}")
    os.write(m, b"x\n")
    out2 = pump(m, 2)
    p.wait(timeout=5)
    show("read_vs_signal, after a key", out2)

if __name__ == "__main__":
    main(sys.argv[1])
