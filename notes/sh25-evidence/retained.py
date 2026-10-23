#!/usr/bin/env python3
"""Diagnostic only: unchanged loop body, retained anonymous/file split."""
import os
import subprocess
import sys
import tempfile
for shell in sys.argv[1:]:
    for run in range(3):
        cells = []
        with tempfile.TemporaryDirectory(prefix='sh25-retained.') as d:
            for n in (10000, 20000):
                p = os.path.join(d, 's')
                with open(p, 'w') as f:
                    f.write('f() { :; }\ng() { local v; v=$1; return 0; }\ni=0\n')
                    f.write(f'while [ $i -lt {n} ]; do ( true ) & wait; i=$((i+1)); done; ')
                    f.write('echo $i; while read k v u; do case $k in RssAnon:|RssFile:|VmHWM:) echo $k $v;; esac; done </proc/self/status; exec true\n')
                r = subprocess.run([shell, p], capture_output=True, text=True,
                                   env={'PATH': '/usr/bin:/bin', 'HOME': '/', 'LC_ALL': 'C'})
                assert r.returncode == 0 and not r.stderr, r
                lines = r.stdout.splitlines()
                assert lines[0] == str(n), r
                cells.append({k: int(v) for k, v in (s.split() for s in lines[1:])})
        print(shell, run + 1, cells, 'delta B/turn',
              {k: (cells[1][k] - cells[0][k]) * 1024 // 10000 for k in cells[0]}, flush=True)
