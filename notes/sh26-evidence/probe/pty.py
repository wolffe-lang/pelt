#!/usr/bin/env python3
"""sh26: type lines into SHELL ARGS... on a pty (stdin, stdout and stderr
the pty, its controlling terminal), waiting WAIT seconds after each, and
print everything the shell wrote, escaped. A line `^D` types the EOF
character, `^C` the interrupt; `@N` waits N more seconds.
usage: pty.py WAIT 'ENV=V ...' SHELL ARG... -- LINE..."""
import os, pty, select, sys, time, signal
wait = float(sys.argv[1]); envs = sys.argv[2].split()
i = sys.argv.index("--")
argv, lines = sys.argv[3:i], sys.argv[i + 1:]
pid, fd = pty.fork()
if pid == 0:
    for n in range(1, signal.NSIG):
        if n in (signal.SIGKILL, signal.SIGSTOP):
            continue
        try:
            signal.signal(n, signal.SIG_DFL)
        except (OSError, ValueError):
            pass
    signal.pthread_sigmask(signal.SIG_SETMASK, [])
    env = {"PATH": "/usr/bin:/bin", "HOME": os.environ.get("PROBE_HOME", os.getcwd()), "LC_ALL": "C", "TERM": "dumb", "PS1": "$ "}
    for kv in envs:
        k, _, v = kv.partition("=")
        env[k] = v.replace("\\s", " ")
    os.execve(argv[0], argv, env)
out = b""
def drain(t):
    global out
    end = time.time() + t
    while time.time() < end:
        r, _, _ = select.select([fd], [], [], 0.02)
        if r:
            try:
                b = os.read(fd, 4096)
            except OSError:
                return False
            if not b:
                return False
            out += b
    return True
drain(wait)
for l in lines:
    if l.startswith("@"):
        drain(float(l[1:])); continue
    if l == "^D":
        os.write(fd, b"\x04")
    elif l == "^C":
        os.write(fd, b"\x03")
    else:
        os.write(fd, (l + "\n").encode())
    out += ("<<" + l + ">>").encode()
    if not drain(wait):
        break
end = time.time() + 3
while time.time() < end:
    p, st = os.waitpid(pid, os.WNOHANG)
    if p:
        break
    drain(0.1)
else:
    os.kill(pid, 9); p, st = os.waitpid(pid, 0)
print(out.decode("latin-1").encode("unicode_escape").decode())
print("status", os.waitstatus_to_exitcode(st))
