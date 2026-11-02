#!/usr/bin/env python3
"""Record every default-size row and exit; bounded four-worker hasu rig."""
import argparse
import concurrent.futures
import json
from pathlib import Path
import re
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument('mode', choices=('baseline', 'proof', 'plant'))
parser.add_argument('shell')
parser.add_argument('records', type=Path)
args = parser.parse_args()
args.records.mkdir(parents=True, exist_ok=True)
listed = subprocess.run(['tools/shape-rss', '--list'], check=True, capture_output=True, text=True)
names = {line.split()[0] for line in listed.stdout.splitlines()}
count = {'baseline': 50, 'proof': 200, 'plant': 1}[args.mode]
loads = []


def run(i):
    path = args.records / f'{args.mode}-{i:03}.log'
    with path.open('w') as log:
        result = subprocess.run(['tools/shape-rss', args.shell], stdout=log, stderr=subprocess.STDOUT)
    raw = path.read_text()
    # Exclude the final 'FAIL 3: ...' summary: it is not a shape row.
    rows = re.findall(r'^shape-rss: (ok  |FAIL) ([a-z][a-z0-9-]*)\s', raw, re.M)
    complete = len(rows) == len(names) and {name for _, name in rows} == names
    reds = [name for verdict, name in rows if verdict == 'FAIL']
    if args.mode == 'plant':
        good = complete and result.returncode == 1 and set(reds) == names and 'wrong answer' not in raw
    elif args.mode == 'proof':
        good = complete and result.returncode == 0 and not reds
    else:
        # Noise is a measured result, not a reason to erase/retry the run.
        good = complete and result.returncode in (0, 1)
    record = {'run': i, 'exit': result.returncode, 'complete': complete,
              'red': reds, 'good': good, 'log': str(path)}
    print(json.dumps(record), flush=True)
    return record


try:
    if args.mode == 'proof':
        # These four loads inherit the job's FOUR-CPU affinity, not the
        # maintainer's CPUs. Only our recorded children are terminated.
        for _ in range(4):
            loads.append(subprocess.Popen([sys.executable, '-c', 'while True: pass']))
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        records = list(pool.map(run, range(1, count + 1)))
    summary = {'mode': args.mode, 'runs': count, 'shapes': len(names),
               'red_runs': sum(bool(r['red']) for r in records),
               'invalid_runs': sum(not r['good'] for r in records),
               'load_processes': len(loads), 'records': records}
    (args.records / f'{args.mode}-summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(f"SH35 {args.mode} runs={count} shapes={len(names)} red_runs={summary['red_runs']} invalid_runs={summary['invalid_runs']}", flush=True)
    if any(p.poll() is not None for p in loads):
        raise RuntimeError('a load process ended during the proof')
    sys.exit(1 if summary['invalid_runs'] else 0)
finally:
    for p in loads:
        if p.poll() is None:
            p.terminate()
        p.wait()
