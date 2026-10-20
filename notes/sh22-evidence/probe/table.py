#!/usr/bin/env python3
"""table.py — lane-local (sh22): table.sh's logs as one markdown table,
bytes a turn, the least and the most of the three passes."""
import ast, glob, os, re, sys
O = sys.argv[1]
TAGS = ["trunk-native", "trunk-release", "head-native", "head-release", "dash"]
rows = {}
order = []
for path in sorted(glob.glob(os.path.join(O, "*.log"))):
    tag = re.match(r"(?:gate|nb)-(.+)-\d\.log", os.path.basename(path)).group(1)
    for line in open(path):
        m = re.match(r"shape-rss: (ok  |FAIL) (\S+)\s+\S+\s+(\d+).*\((-?\d+) B a turn\)\s+\[(.*)\]", line)
        if m:
            name, n, per, text = m.group(2), m.group(3), int(m.group(4)), m.group(5)
        else:
            m = re.match(r"shapes22: \S+\s+(\S+)\s+\S+\s+(\d+).*\((-?\d+) B a turn\) \S+ \[(.*)\]$", line.strip())
            if not m:
                continue
            name, n, per, text = m.group(1), m.group(2), int(m.group(3)), ast.literal_eval(m.group(4)).replace("\n", "; ")
        key = (name, text, n)
        if key not in rows:
            rows[key] = {}
            order.append(key)
        rows[key].setdefault(tag, []).append(per)
print("| row | shape | N | " + " | ".join(TAGS) + " |")
print("|---|---|---:|" + "---:|" * len(TAGS))
for key in order:
    name, text, n = key
    cells = []
    for t in TAGS:
        v = rows[key].get(t, [])
        cells.append("—" if not v else (f"{min(v)}" if min(v) == max(v) else f"{min(v)}–{max(v)}"))
    print(f"| {name} | `{text}` | {int(n):,} | " + " | ".join(cells) + " |")
