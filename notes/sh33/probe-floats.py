#!/usr/bin/env python3
"""Independent black-box float and directory wording differential (sh33)."""
import os
from pathlib import Path
import random
import subprocess
import sys
import tempfile

pelt = str(Path(sys.argv[1]).resolve())
rng = random.Random(33)
rows = []
for _ in range(300):
    value = rng.randrange(-1000000, 1000000) / (10 ** rng.randrange(0, 10))
    fmt = '%' + rng.choice(['', '#', '+', ' ', '0', '-'])
    fmt += str(rng.randrange(0, 20)) + '.' + str(rng.randrange(0, 18))
    fmt += rng.choice('eEfFgG') + '\n'
    rows.append((fmt, repr(value)))
for value in ['0', '-0', '1e308', '1e-308', '5e-324', '0x1p-1022',
              '0x1p-1074', '0x1.fffffffffffffp1023', '0x1.fffffffffffff8p1023',
              '0x1.00000000000008p0', '0x1.00000000000018p0', 'inf', '-nan']:
    for conv in 'efg':
        rows.append(('%#15.8' + conv + '\n', value))
failed = 0
for fmt, value in rows:
    args = ['-c', 'printf "$@"', 'probe', fmt, value]
    d = subprocess.run(['dash', *args], capture_output=True, timeout=5)
    p = subprocess.run([pelt, *args], capture_output=True, timeout=5)
    if (d.returncode, d.stdout, bool(d.stderr)) != (p.returncode, p.stdout, bool(p.stderr)):
        failed += 1
        print('FAIL', repr(fmt), repr(value), 'dash', d.returncode, repr(d.stdout),
              'pelt', p.returncode, repr(p.stdout), repr(p.stderr))
print(f'float-black-box: {len(rows)-failed} pass, {failed} fail', flush=True)
with tempfile.TemporaryDirectory(prefix='sh33-path-', dir=os.environ.get('TMPDIR')) as tmp:
    Path(tmp, 'only-directory').mkdir()
    for invocation, status in [('only-directory', 127), ('command only-directory', 127),
                               ('exec only-directory', 126)]:
        args = ['-c', 'PATH=$1; ' + invocation, 'probe', tmp]
        d = subprocess.run(['dash', *args], capture_output=True, timeout=5)
        p = subprocess.run([pelt, *args], capture_output=True, timeout=5)
        ok = d.returncode == p.returncode == status and d.stderr.endswith(b'Permission denied\n') and p.stderr.endswith(b'Permission denied\n')
        print(('ok' if ok else 'FAIL'), 'directory-wording', invocation, status)
        if not ok:
            failed += 1
            print('dash', repr(d.stderr), 'pelt', repr(p.stderr))
sys.exit(bool(failed))
