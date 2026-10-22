#!/usr/bin/env python3
# sh20: probe/table.sh's passes summed up: each row's bytes a turn and its
# peak at the larger N, per binary, the three passes side by side.
# usage: table-sum.py DIR
import os, re, sys
d = sys.argv[1]
tags = ["pin-native", "head-native", "pin-release", "head-release", "dash"]
rows, data = [], {}
for t in tags:
    for p in (1, 2, 3):
        f = os.path.join(d, f"rows-{t}-{p}.log")
        if not os.path.exists(f):
            continue
        for l in open(f):
            m = re.match(r"shape-rss: (ok|FAIL)\s+(\S+)\s+\S+\s+\d+\s+(\d+) KB\s+\d+\s+(\d+) KB\s+grew\s+(-?\d+) KB \((-?\d+) B a turn\)", l)
            if m:
                ok, name, a, b, g, bt = m.groups()
                if name not in rows:
                    rows.append(name)
                data[(name, t, p)] = (ok, int(b), int(bt))
print("row | " + " | ".join(tags) + "   (B a turn, passes 1/2/3; FAIL marked !)")
for r in rows:
    cells = []
    for t in tags:
        v = [data.get((r, t, p)) for p in (1, 2, 3)]
        cells.append("/".join("-" if x is None else (("!" if x[0] == "FAIL" else "") + str(x[2])) for x in v))
    print(f"{r} | " + " | ".join(cells))
print()
print("peak KB at the larger N, pass 3:")
for r in rows:
    print(f"{r} | " + " | ".join(str(data.get((r, t, 3), ("", "-"))[1]) for t in tags))
