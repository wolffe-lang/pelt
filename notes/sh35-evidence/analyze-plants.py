#!/usr/bin/env python3
"""Check each recorded plant's actual delta against its printed bound."""
import json
from pathlib import Path
import re
import sys

root = Path(sys.argv[1])
raw = (root / 'resumed-plant-records/plant-001.log').read_text()
assert 'wrong answer' not in raw
pattern = re.compile(r'^shape-rss: FAIL ([a-z][a-z0-9-]*)\s+\S+\s+(\d+)\s+(\d+) KB\s+(\d+)\s+(\d+) KB\s+grew\s+(-?\d+) KB \((-?\d+) B a turn\).*bound=(\d+)B\+(\d+)KiB$')
records = []
for line in raw.splitlines():
    m = pattern.match(line)
    if not m:
        continue
    name, n, first, twice, second, grew, per, bound, slack = m.groups()
    n, first, twice, second, grew, per, bound, slack = map(int, (n, first, twice, second, grew, per, bound, slack))
    assert twice == 2 * n and second - first == grew
    limit = n * bound // 1024 + slack
    assert grew > limit, (name, grew, limit)
    records.append({'shape': name, 'n': n, 'first_kib': first, 'second_kib': second,
                    'grew_kib': grew, 'bytes_per_turn': per,
                    'bound_bytes_per_turn': bound, 'slack_kib': slack, 'limit_kib': limit})
assert len(records) == 52 and len({r['shape'] for r in records}) == 52
(root / 'plant-margins.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in records))
print('PLANT_MEMORY_DELTAS_VERIFIED', len(records))
for r in records:
    if r['shape'] in ('baseline', 'jobs-set-m', 'jobs-loop', 'script-background-wait', 'typed-background-wait'):
        print(json.dumps(r))
