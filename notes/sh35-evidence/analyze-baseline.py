#!/usr/bin/env python3
"""Read completed trunk measurements without treating partial logs as runs."""
from collections import defaultdict
import json
from pathlib import Path
import re
import sys

root = Path(sys.argv[1])
done = {int(i): int(code) for i, code in re.findall(r'^BASELINE run=(\d+) exit=(-?\d+)$',
                                                (root / 'baseline.log').read_text(), re.M)}
rows = defaultdict(list)
errors = defaultdict(list)
invalid = []
pattern = re.compile(r'^shape-rss: (ok  |FAIL) ([a-z][a-z0-9-]*)\s.*?grew\s+(-?\d+) KB \((-?\d+) B a turn\)')
for i in sorted(done):
    raw = (root / 'base/sh35-baseline' / f'run-{i:03}.log').read_text()
    found = [m.groups() for line in raw.splitlines() if (m := pattern.match(line))]
    bad = dict(re.findall(r'^shape-rss: +([a-z][a-z0-9-]*): wrong answer \((.*)\)$', raw, re.M))
    if len(found) != 52 or len({name for _, name, _, _ in found}) != 52 or bad:
        invalid.append(i)
    for verdict, name, grew, per in found:
        if name in bad:
            errors[name].append({'run': i, 'reason': bad[name]})
        else:
            rows[name].append((verdict == 'FAIL', int(grew), int(per)))
print(json.dumps({'completed_runs': len(done), 'red_runs': sum(code != 0 for code in done.values()),
                  'invalid_runs': invalid, 'shapes': len(rows)}))
for name in sorted(set(rows) | set(errors)):
    data = rows[name]
    print(json.dumps({'shape': name, 'attempted': len(data) + len(errors[name]),
                      'valid_readings': len(data), 'memory_red': sum(r[0] for r in data),
                      'errors': errors[name],
                      'grew_kib': [min(r[1] for r in data), max(r[1] for r in data)] if data else None,
                      'bytes_per_turn': [min(r[2] for r in data), max(r[2] for r in data)] if data else None}))
