#!/usr/bin/env python3
"""close-timing.py LINES — from race.py's OUT (with the probes' log lines), for each boot of a close row,
the foreground probes' signals in the order they came, with their time from the shell's SIGHUP to them
(ms) and whether the shell (the probe's parent at its start, or the shell named by the HUP's sender) was
still its parent; then a tally of the orders seen, and of the kernel's SIGHUP recorded or not."""
import collections
import re
import sys

FG = {"fg", "mf", "pf1", "pf2", "sf1"}
rows = []
cur = None
for ln in open(sys.argv[1], errors="replace"):
    m = re.match(r"(\d+) (ok|FAIL) (\S+) \| (.*)", ln)
    if m:
        cur = dict(boot=int(m[1]), row=m[3], line=m[4], log=[])
        rows.append(cur)
        continue
    if ln.startswith("  log ") and cur is not None:
        cur["log"].append(ln[6:].rstrip("\n"))
orders = collections.Counter()
lost = collections.Counter()
for r in rows:
    starts, ev = {}, collections.defaultdict(list)
    for ln in r["log"]:
        f = ln.split()
        if f[0] == "start":
            starts[f[1]] = dict(pid=int(f[3]), ppid=int(f[9]))
        elif f[0] == "sig" and "at" in f:
            i = f.index("at")
            ev[f[1]].append((int(f[i + 1]), f[2], int(f[4]), int(f[6]), int(f[i + 3])))
        elif f[0] in ("die", "end") and "at" in f:
            i = f.index("at")
            ev[f[1]].append((int(f[i + 1]), f[0].upper() + (":" + f[2] if f[0] == "die" else ""), 0, -1,
                             int(f[i + 3])))
    for name in sorted(set(ev) & FG):
        st = starts.get(name)
        es = ev[name]  # the log order: handlers do not nest (sa_mask full), so it is the order they ran
        shell_hups = [e for e in es if e[1] == "HUP" and e[3] > 0]
        shell = shell_hups[0][3] if shell_hups else None
        t0 = shell_hups[0][0] if shell_hups else es[0][0]
        parent = st["ppid"] if st else None
        seq = []
        for t, s, code, frm, pp in es:
            who = "shell" if frm == shell and frm > 0 else ("kernel" if frm == 0 else ("-" if frm < 0 else "other"))
            alive = "parent" if pp == parent else "reparented"
            seq.append(f"{s}:{who}" + (f"@{t - t0:+d}ms/{alive}" if who != "-" else f"@{t - t0:+d}ms"))
        kind = " ".join(x.split("@")[0] for x in seq)
        orders[(r["row"], name, kind)] += 1
        got_k = any(e[1] == "HUP" and e[3] == 0 for e in es)
        lost[(r["row"], name, "kernel HUP recorded" if got_k else "kernel HUP not recorded")] += 1
        if "-v" in sys.argv:
            print(r["boot"], r["row"], name, " ".join(seq))
print("orders (signals as they came; END:x / DIE:x the probe's end):")
for k, c in sorted(orders.items()):
    print(f"  {c:5d}  {k[0]} {k[1]}: {k[2]}")
print("the kernel's SIGHUP:")
for k, c in sorted(lost.items()):
    print(f"  {c:5d}  {k[0]} {k[1]}: {k[2]}")
