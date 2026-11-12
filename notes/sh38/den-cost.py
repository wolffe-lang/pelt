#!/usr/bin/env python3
"""den-cost — what the friendly prompt's `den status --porcelain` costs, by
repository size (sh38's measurement for the prompt's version-control segment).

For each size N it makes a repository of N files with den, commits them, then
changes min(60, N) of them, and measures:

  status    `den status --porcelain` run directly, ROUNDS times: the wall
            time of each (the median and the largest), and its row count
  prompt    pelt invoked as `pelt` (friendly) on a pseudo-terminal in that
            directory, `true` typed ROUNDS times: the wall time from the
            Enter to the next prompt's marker, and what each prompt's
            segment showed: `fresh` ([vcs:N] drawn plain), `stale` (dimmed:
            the probe missed its deadline and the last value was kept) or
            `none` (no segment)
  baseline  the same prompt with no `den` on PATH

usage: den-cost.py DEN PELT WORKDIR [N ...]   (default N: 10 100 400 2000 10000)
Prints one line per measurement. Nothing is deleted outside WORKDIR.
"""

import os
import pty
import re
import select
import shutil
import statistics
import struct
import subprocess
import sys
import termios
import fcntl
import time

ROUNDS = 15


def run(cmd, cwd, env):
    r = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True)
    if r.returncode != 0:
        raise SystemExit(f"den-cost: {cmd} failed: {r.stderr[:300]!r}")
    return r.stdout


def make_repo(den, root, n, env):
    d = os.path.join(root, f"repo-{n}")
    if os.path.exists(d):
        shutil.rmtree(d)
    os.makedirs(d)
    for i in range(n):
        sub = os.path.join(d, f"d{i // 200}")
        os.makedirs(sub, exist_ok=True)
        with open(os.path.join(sub, f"f{i}.txt"), "w") as fh:
            fh.write(f"file {i}\n" * 4)
    run([den, "init"], d, env)
    run([den, "config", "user.name", "sh38"], d, env)
    run([den, "config", "user.email", "sh38@example.invalid"], d, env)
    if n <= 2000:
        run([den, "add", "."], d, env)
        run([den, "commit", "-m", "many"], d, env)
    else:
        # den at this head refuses larger first commits (`den add .` of
        # 10,000 files exits 1 with nothing on standard error; a commit of
        # 3,000 new files says "not yet implemented: commit rename summary
        # budget"): one directory of 200 files a commit
        for sub in sorted(os.listdir(d)):
            if sub.startswith("d"):
                run([den, "add", sub], d, env)
                run([den, "commit", "-m", sub], d, env)
    for i in range(min(60, n)):
        with open(os.path.join(d, f"d{i // 200}", f"f{i}.txt"), "a") as fh:
            fh.write("changed\n")
    return d


def status_cost(den, d, env):
    times = []
    rows = -1
    for _ in range(ROUNDS):
        t = time.perf_counter()
        out = run([den, "status", "--porcelain"], d, env)
        times.append((time.perf_counter() - t) * 1000)
        rows = len([ln for ln in out.splitlines() if ln.strip()])
    return times, rows


def prompt_cost(pelt, d, env):
    master, slave = pty.openpty()
    fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack("HHHH", 30, 160, 0, 0))

    def pre():
        fcntl.ioctl(0, termios.TIOCSCTTY, 0)

    p = subprocess.Popen(["pelt", "-i"], executable=pelt, stdin=slave, stdout=slave, stderr=slave,
                         env=env, cwd=d, start_new_session=True, preexec_fn=pre, close_fds=True)
    os.close(slave)
    buf = b""

    def pump(secs):
        nonlocal buf
        end = time.perf_counter() + secs
        while time.perf_counter() < end:
            r, _, _ = select.select([master], [], [], 0.005)
            if r:
                try:
                    data = os.read(master, 65536)
                except OSError:
                    return
                if not data:
                    return
                buf += data
                if b"\x1b[6n" in data:
                    os.write(master, b"\x1b[1;1R")

    def until_prompt(start, secs=10):
        end = time.perf_counter() + secs
        while time.perf_counter() < end:
            pump(0.002)
            tail = buf[start:]
            if re.search(rb"> \x1b\[0m(\x1b\[0m)*$", tail) or tail.endswith(b"> "):
                return time.perf_counter()
        return None

    first = until_prompt(0, 15)
    pump(0.3)
    lat, kinds = [], []
    for _ in range(ROUNDS + 3):
        start = len(buf)
        t0 = time.perf_counter()
        os.write(master, b"true\r")
        t1 = until_prompt(start)
        if t1 is None:
            lat.append(-1)
            kinds.append("noprompt")
            continue
        lat.append((t1 - t0) * 1000)
        seg = buf[start:]
        if re.search(rb"\x1b\[0;2m \[vcs:", seg):
            kinds.append("stale")
        elif b"[vcs:" in seg:
            kinds.append("fresh")
        else:
            kinds.append("none")
        pump(0.05)
    os.write(master, b"exit\r")
    end = time.time() + 5
    while p.poll() is None and time.time() < end:
        pump(0.05)
    if p.poll() is None:
        p.kill()
        p.wait()
    os.close(master)
    return lat[3:], kinds[3:], first is not None


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    den, pelt, work = (os.path.abspath(a) for a in argv[:3])
    sizes = [int(x) for x in argv[3:]] or [10, 100, 400, 2000, 10000]
    bindir = os.path.join(work, "bin")
    os.makedirs(bindir, exist_ok=True)
    link = os.path.join(bindir, "den")
    if not os.path.exists(link):
        os.symlink(den, link)
    home = os.path.join(work, "home")
    os.makedirs(home, exist_ok=True)
    base = {"HOME": home, "LC_ALL": "C.UTF-8", "TERM": "xterm-256color", "USER": "tester",
            "HOSTNAME": "box"}
    with_den = dict(base, PATH=bindir + ":/usr/bin:/bin")
    without = dict(base, PATH="/usr/bin:/bin")
    for n in sizes:
        if n > 2000:
            # what `den add .` and one commit answer at this size (the rows below commit in steps)
            probe = os.path.join(work, f"probe-{n}")
            if os.path.exists(probe):
                shutil.rmtree(probe)
            os.makedirs(probe)
            for i in range(n):
                sub = os.path.join(probe, f"d{i // 200}")
                os.makedirs(sub, exist_ok=True)
                with open(os.path.join(sub, f"f{i}.txt"), "w") as fh:
                    fh.write(f"file {i}\n")
            run([den, "init"], probe, with_den)
            run([den, "config", "user.name", "sh38"], probe, with_den)
            run([den, "config", "user.email", "sh38@example.invalid"], probe, with_den)
            r = subprocess.run([den, "add", "."], cwd=probe, env=with_den, capture_output=True)
            print(f"add      N={n:<6} `den add .` exit {r.returncode} stderr {r.stderr[:160]!r}", flush=True)
            if r.returncode == 0:
                r = subprocess.run([den, "commit", "-m", "all"], cwd=probe, env=with_den, capture_output=True)
                print(f"commit   N={n:<6} one commit of all: exit {r.returncode} stderr {r.stderr[:160]!r}",
                      flush=True)
            shutil.rmtree(probe)
        d = make_repo(den, work, n, with_den)
        times, rows = status_cost(den, d, with_den)
        print(f"status   N={n:<6} rows={rows:<3} median_ms={statistics.median(times):8.1f} "
              f"max_ms={max(times):8.1f}", flush=True)
        lat, kinds, ok = prompt_cost(pelt, d, with_den)
        good = [x for x in lat if x >= 0]
        print(f"prompt   N={n:<6} median_ms={statistics.median(good) if good else -1:8.1f} "
              f"max_ms={max(good) if good else -1:8.1f} fresh={kinds.count('fresh')} "
              f"stale={kinds.count('stale')} none={kinds.count('none')} noprompt={kinds.count('noprompt')}",
              flush=True)
        lat, kinds, ok = prompt_cost(pelt, d, without)
        good = [x for x in lat if x >= 0]
        print(f"baseline N={n:<6} median_ms={statistics.median(good) if good else -1:8.1f} "
              f"max_ms={max(good) if good else -1:8.1f} (no den on PATH)", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
