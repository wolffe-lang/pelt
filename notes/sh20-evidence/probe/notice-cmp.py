#!/usr/bin/env python3
# sh20: notice.sh's answers side by side, pelt's words read as dash's.
# usage: notice-cmp.py PELT.txt DASH.txt
import re, sys
def rows(p):
    out, cur = {}, None
    for l in open(p):
        m = re.match(r'^(\d\d) (.*)', l)
        if m:
            cur = m.group(1); out[cur] = [m.group(2)]
        elif cur:
            out[cur].append(l.strip())
    return out
a = rows(sys.argv[1]); b = rows(sys.argv[2])
same = 0
for k in sorted(b):
    pa = [re.sub(r'pelt: ended by signal 15 \(TERM\)', 'Terminated', x) for x in a.get(k, [])]
    if pa == b[k]:
        same += 1
        continue
    print(f"{k} {b[k][0]}")
    for x, y in zip(pa[1:], b[k][1:]):
        print(f"     pelt {x:28} dash {y}")
print(f"same {same} of {len(b)}")
