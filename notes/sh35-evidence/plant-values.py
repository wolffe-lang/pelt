#!/usr/bin/env python3
"""The per-turn plant must retain actual 1 KiB values, not just variable names."""
import importlib.machinery
import importlib.util
import os
from pathlib import Path
import subprocess
import sys

plant = Path(sys.argv[1]).resolve()
shell = str(Path(sys.argv[2]).resolve())
loader = importlib.machinery.SourceFileLoader('plant_values', str(plant / 'tools/shape-rss'))
spec = importlib.util.spec_from_loader(loader.name, loader)
module = importlib.util.module_from_spec(spec)
loader.exec_module(module)
script = '\n'.join([module._PLANT] * 3) + '\n'
script += 'echo ${#__shape_hold_1} ${#__shape_hold_2} ${#__shape_hold_3}\n'
for i in range(1, 4):
    value = str(i) + 'x' * 1024
    script += f'[ "${{__shape_hold_{i}}}" = "{value}" ] || exit 7\n'
script += 'echo preserved\n'
r = subprocess.run([shell, '-c', script], env=module.ENV,
                   capture_output=True, text=True, timeout=30)
print(f'PLANT_VALUE_RESULT shell_exit={r.returncode} stdout={r.stdout!r} stderr={r.stderr!r}', flush=True)
good = r.returncode == 0 and r.stdout == '1025 1025 1025\npreserved\n' and not r.stderr
print(f'END plant-value-invariant exit={0 if good else 1}', flush=True)
sys.exit(0 if good else 1)
