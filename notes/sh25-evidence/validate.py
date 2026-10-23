#!/usr/bin/env python3
"""Reject unfinished/partial gauntlets and nonzero or missing assertions."""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
status = (root / 'final.status').read_text()
assert status.rstrip().endswith('done'), 'unfinished'
expected = {'fmt', 'build', 'test', 'clause', 'width', 'diff-selftest',
            'sess-selftest', 'oracle-check', 'shape-native-worker', 'shape-release-worker'}
for tier in ('native', 'release'):
    expected.update(f'{g}-{tier}' for g in ('diff', 'sess', 'self', 'glob-rss',
        'loop-rss', 'exec-witness', 'edit-witness', 'hist-witness', 'signal-witness',
        'reap', 'notice', 'notice-check'))
    expected.update(f'{g}-{tier}-taskset' for g in ('diff', 'sess'))
    for p in (1, 2, 3):
        expected.update((f'shape-{tier}-{p}', f'shape-{tier}-{p}-taskset'))
found = dict(re.findall(r'^([a-z0-9-]+)=(\d+)$', status, re.M))
assert set(found) == expected, (sorted(expected - set(found)), sorted(set(found) - expected))
assert all(v == '0' for v in found.values()), {k: v for k, v in found.items() if v != '0'}
for tier in ('native', 'release'):
    for suffix in ('', '-taskset'):
        diff = (root / 'final' / f'diff-{tier}{suffix}.log').read_text()
        assert re.search(r'difftest: total\s+998\s+0\s+25\b', diff), f'corpus {tier}{suffix}'
        sess = (root / 'final' / f'sess-{tier}{suffix}.log').read_text()
        assert re.search(r'session: pass 290\s+fail 0\s+pending 2\b', sess), f'sessions {tier}{suffix}'
    for p in (1, 2, 3):
        for suffix in ('', '-taskset'):
            log = (root / 'final' / f'shape-{tier}-{p}{suffix}.log').read_text()
            assert len(re.findall(r'^shape-rss: ok\s+\S+\s+(?:loop|script|typed|jobs|monitor)\s', log, re.M)) == 52, f'shape count {tier}/{p}{suffix}'
            assert 'FAIL' not in log and 'SKIP' not in log, f'shape verdict {tier}/{p}{suffix}'
for p in (root / 'final').glob('*.log'):
    assert not re.search(r'\bSKIP\b', p.read_text()), f'unaccounted SKIP {p}'
print(f'gauntlet: {len(expected)} zero exits; corpus998/0/25 x4; sessions290/0/2 x4; 624 shape assertions; no SKIP')
