#!/usr/bin/env python3
"""Black-box diagnosis at the pre-fix instrument; no shell source oracle."""
import argparse
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch

root = Path(__file__).resolve().parents[2]
loader = importlib.machinery.SourceFileLoader('shape_probe', str(root / 'tools/shape-rss'))
spec = importlib.util.spec_from_loader(loader.name, loader)
shape = importlib.util.module_from_spec(spec)
loader.exec_module(shape)
parser = argparse.ArgumentParser()
parser.add_argument('shell')
parser.add_argument('records', type=Path)
parser.add_argument('--typed-only', action='store_true')
args = parser.parse_args()
args.records.mkdir(parents=True, exist_ok=True)
shell = os.path.abspath(args.shell)

# Record actual read bytes by fd without changing what the harness sees.
read = os.read
captured = {}
def observe(fd, count):
    data = read(fd, count)
    captured.setdefault(fd, bytearray()).extend(data)
    return data

with patch.object(shape.os, 'read', side_effect=observe):
    result = shape.run_typed(shell, 'true & wait', 8)
print('TYPED_RESULT', repr(result), flush=True)
for fd, data in captured.items():
    if b'Done' in data:
        path = args.records / f'typed-stderr-fd-{fd}.bin'
        path.write_bytes(data)
        print('TYPED_STDERR', f'fd={fd} bytes={len(data)} Done={data.count(b"Done")}', repr(bytes(data[:4096])), flush=True)


def paired_script(kind, text, n):
    script = shape.PRELUDE + shape.sampler()
    if kind == 'monitor':
        script += 'exec 2>/dev/null\nset -m\n'
    script += 'i=0\n{\n'
    for limit in (n, 2 * n):
        script += f'while [ $i -lt {limit} ]; do\n{text}\ni=$((i+1))\ndone\n__shape_sample\n'
    script += 'echo $i\n'
    if kind == 'monitor':
        script += 'exec true\n'
    return script + '}\n'


if not args.typed_only:
    for kind, text, n, bound, slack in [('loop', ':', 10000, 100, 1024),
                                        ('monitor', 'env true & wait $!', 3000, 160, 64)]:
        for variant in ('if-per-turn', 'paired-loops'):
            for run in range(1, 4):
                with tempfile.TemporaryDirectory() as cwd:
                    if variant == 'paired-loops':
                        with patch.object(shape, 'file_script', side_effect=paired_script):
                            rows, ok, why = shape.run_file(shell, kind, text, n, cwd)
                    else:
                        rows, ok, why = shape.run_file(shell, kind, text, n, cwd)
                grew = rows[1] - rows[0]
                record = {'kind': kind, 'variant': variant, 'run': run, 'n': n,
                          'rows': rows, 'answer_ok': ok, 'why': why, 'grew_kib': grew,
                          'bytes_per_turn': grew * 1024 / n,
                          'memory_ok': grew <= n * bound // 1024 + slack}
                print('MEMORY', json.dumps(record), flush=True)
print('SH35_DIAG_COMPLETE', flush=True)
