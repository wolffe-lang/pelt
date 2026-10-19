#!/usr/bin/env python3
"""state — sh19 #34: what a shell process holds that a forked child
would inherit: its threads, its open descriptors, its signal
dispositions, read from outside while it waits in a known place.

usage: state.py SHELL...   (linux: /proc; macOS: ps -M and lsof)
The interactive shell's HOME (where it keeps its history) is $TMPDIR,
else the current directory: never /tmp.
Each row: shell, the situation, threads, descriptors (number -> what),
and on linux SigBlk/SigIgn/SigCgt.
"""
import os, pty, select, subprocess, sys, time

SITUATIONS = [
    ("script, waiting on a program", ["-c", "sleep 1"]),
    ("script with a trap, waiting", ["-c", "trap 'echo t' USR1 INT; sleep 1"]),
    ("script in $( ), waiting", ["-c", "x=$(sleep 1; echo y); echo $x"]),
    ("script, a pipeline", ["-c", "sleep 1 | cat"]),
]


def fds(pid):
    if sys.platform == "darwin":
        out = subprocess.run(["lsof", "-a", "-p", str(pid), "-d", "0-255", "-F", "ftn"],
                             capture_output=True, text=True).stdout.splitlines()
        rows, cur = [], None
        for ln in out:
            if ln.startswith("f"):
                cur = [ln[1:], "", ""]
                rows.append(cur)
            elif cur is not None and ln.startswith("t"):
                cur[1] = ln[1:]
            elif cur is not None and ln.startswith("n"):
                cur[2] = ln[1:]
        return " ".join(f"{a}->{b}:{os.path.basename(c) or c}" for a, b, c in rows)
    d = f"/proc/{pid}/fd"
    out = []
    for n in sorted(os.listdir(d), key=int):
        try:
            t = os.readlink(f"{d}/{n}")
        except OSError:
            t = "?"
        if t.startswith("/"):
            t = os.path.basename(t) if not t.startswith("/dev/") else t
        out.append(f"{n}->{t}")
    return " ".join(out)


def threads(pid):
    if sys.platform == "darwin":
        out = subprocess.run(["ps", "-M", "-p", str(pid)], capture_output=True, text=True).stdout
        return max(0, len(out.splitlines()) - 1)
    return len(os.listdir(f"/proc/{pid}/task"))


def sigs(pid):
    if sys.platform == "darwin":
        return "-"
    keep = {}
    for ln in open(f"/proc/{pid}/status"):
        k = ln.split(":")[0]
        if k in ("SigBlk", "SigIgn", "SigCgt"):
            keep[k] = ln.split()[1].lstrip("0") or "0"
    return " ".join(f"{k}={keep[k]}" for k in ("SigBlk", "SigIgn", "SigCgt"))


def row(shell, what, pid):
    print(f"state: {os.path.basename(shell):10} | {what:32} | threads {threads(pid)} | "
          f"fds {fds(pid)} | {sigs(pid)}", flush=True)


def interactive(shell):
    master, slave = pty.openpty()

    def ctty():
        os.setsid()
        import fcntl, termios
        fcntl.ioctl(0, termios.TIOCSCTTY, 0)

    p = subprocess.Popen([shell, "-i"], stdin=slave, stdout=slave, stderr=slave,
                         env={"PATH": "/usr/bin:/bin", "HOME": os.environ.get("TMPDIR") or os.getcwd(),
                              "TERM": "dumb", "PS1": "$ "},
                         preexec_fn=ctty)
    os.close(slave)
    got = b""
    end = time.time() + 5
    while time.time() < end and not got.endswith(b"$ "):
        r, _, _ = select.select([master], [], [], 0.2)
        if r:
            try:
                got += os.read(master, 4096)
            except OSError:
                break
    time.sleep(0.3)
    row(shell, "interactive, at the prompt", p.pid)
    os.write(master, b"sleep 1 &\n")
    time.sleep(0.3)
    row(shell, "interactive, a job running", p.pid)
    os.write(master, b"exit\n")
    end = time.time() + 5
    while p.poll() is None and time.time() < end:
        r, _, _ = select.select([master], [], [], 0.2)
        if r:
            try:
                os.read(master, 4096)
            except OSError:
                break
    if p.poll() is None:
        p.kill()
    p.wait()
    os.close(master)


def main(argv):
    for shell in argv:
        for what, args in SITUATIONS:
            p = subprocess.Popen([shell] + args, stdout=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                                 env={"PATH": "/usr/bin:/bin", "HOME": "/", "LC_ALL": "C"})
            time.sleep(0.4)
            row(shell, what, p.pid)
            p.wait()
        interactive(shell)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
