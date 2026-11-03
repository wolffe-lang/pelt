#!/usr/bin/env python3
"""Default-size shape measurements in bounded, stop-on-red proof chunks."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
import lib_reap as lr  # noqa: E402

ROW = re.compile(r'^shape-rss: (ok  |FAIL) ([a-z][a-z0-9-]*)\s', re.M)


def classify(raw, code, names):
    rows = ROW.findall(raw)
    trailer = any(line.startswith('shape-rss: ok (default bound ') or
                  re.match(r'^shape-rss: FAIL [0-9]+:', line) for line in raw.splitlines())
    complete = len(rows) == len(names) and {name for _, name in rows} == names and trailer
    red = [name for verdict, name in rows if verdict == 'FAIL']
    return {'exit': code, 'complete': complete, 'red': red,
            'good': complete and code == 0 and not red,
            'wrong_answer': 'wrong answer' in raw}


def parser():
    p = argparse.ArgumentParser()
    p.add_argument('mode', choices=('baseline', 'proof', 'plant'))
    p.add_argument('shell')
    p.add_argument('records', type=Path)
    p.add_argument('--runs', type=int)
    p.add_argument('--first-run', type=int, default=1)
    p.add_argument('--tool', default='tools/shape-rss')
    return p


def main(argv=None):
    p = parser()
    a = p.parse_args(argv)
    if a.mode == 'proof' and (a.runs is None or not 1 <= a.runs <= 16):
        p.error('proof requires --runs in 1..16; one independently recorded bounded chunk')
    count = a.runs if a.runs is not None else {'baseline': 50, 'plant': 1}[a.mode]
    if count < 1 or a.first_run < 1 or (a.mode == 'proof' and a.first_run+count > 201):
        p.error('invalid global run range')
    if a.records.exists():
        p.error('record directory already exists; never overwrite or append a cut chunk')
    a.records.mkdir(parents=True)
    listed = subprocess.run([a.tool, '--list'], check=True, capture_output=True, text=True)
    names = {line.split()[0] for line in listed.stdout.splitlines()}
    if a.mode == 'proof' and len(names) != 52:
        raise RuntimeError('proof must include all 52 unchanged shapes')
    lr.subreaper()
    loads, active, records = [], {}, []
    next_run, started, first_red = a.first_run, 0, None
    begin, heartbeat = time.monotonic(), -60
    stop_reason = None
    workers = 1 if a.mode == 'plant' else 4

    def end_active(reason):
        for pid, item in list(active.items()):
            child = item['process']
            interrupted = child.poll() is None
            if interrupted:
                lr.end_tree(pid, {x for x in active if x != pid} | {x.pid for x in loads})
                child.wait()
            item['handle'].close()
            raw = item['log'].read_text(errors='replace')
            d = classify(raw, child.returncode, names)
            if interrupted:
                d.update(complete=False, good=False, cancelled=reason)
            else:
                d['stop_observed_after_exit'] = reason
            d.update(run=item['run'], log=str(item['log']),
                     traces=[str(x) for x in item['trace'].glob('*.json')] if item['trace'].exists() else [])
            records.append(d)
            print('CANCELLED ' + json.dumps(d), flush=True)
            del active[pid]

    try:
        if a.mode == 'proof':
            loads = [subprocess.Popen([sys.executable, '-c', 'while True: pass']) for _ in range(4)]
        print(f'CHUNK_BEGIN mode={a.mode} first={a.first_run} requested={count} workers={workers} loads={len(loads)} affinity={sorted(os.sched_getaffinity(0))}', flush=True)
        while active or (stop_reason is None and started < count):
            elapsed = time.monotonic()-begin
            if elapsed >= 6000:
                stop_reason = 'budget'
                end_active('chunk safety budget; incomplete, not a row verdict')
                break
            if elapsed >= 5400 and stop_reason is None:
                stop_reason = 'dispatch budget'
            while stop_reason is None and started < count and len(active) < workers:
                prefix = f'{a.mode}-{next_run:03}'
                log = a.records / (prefix+'.log')
                trace = a.records / (prefix+'-traces')
                handle = log.open('w')
                env = dict(os.environ, PELT_SHAPE_TRACE_DIR=str(trace.resolve()))
                child = subprocess.Popen([a.tool, a.shell], stdout=handle, stderr=subprocess.STDOUT, env=env)
                active[child.pid] = {'process': child, 'run': next_run, 'log': log,
                                     'trace': trace, 'handle': handle}
                started += 1
                next_run += 1
            for pid, item in list(active.items()):
                child = item['process']
                raw = item['log'].read_text(errors='replace')
                traces = []
                if item['trace'].exists():
                    for path in item['trace'].glob('*.json'):
                        try:
                            json.loads(path.read_text())
                        except (OSError, json.JSONDecodeError):
                            continue
                        traces.append(str(path))
                row_red = [name for verdict, name in ROW.findall(raw) if verdict == 'FAIL']
                if a.mode == 'proof' and (row_red or traces):
                    first_red = {'run': item['run'], 'rows': row_red or [Path(x).stem for x in traces],
                                 'log': str(item['log']), 'traces': traces}
                    stop_reason = 'red'
                    print('FIRST_RED ' + json.dumps(first_red), flush=True)
                    end_active('stop at first red; in-flight records preserved')
                    break
                code = child.poll()
                if code is not None:
                    item['handle'].close()
                    d = classify(raw, code, names)
                    if a.mode == 'plant':
                        d['good'] = d['complete'] and code == 1 and set(d['red']) == names and not d['wrong_answer']
                    elif a.mode == 'baseline':
                        d['good'] = d['complete'] and code in (0, 1) and not d['wrong_answer']
                    d.update(run=item['run'], log=str(item['log']), traces=traces)
                    records.append(d)
                    print('RUN ' + json.dumps(d), flush=True)
                    del active[pid]
                    if a.mode == 'proof' and not d['good']:
                        first_red = d
                        stop_reason = 'red' if d['red'] else 'invalid run'
                        end_active('stop after failed tool result')
                        break
            if time.monotonic()-begin-heartbeat >= 60:
                print(f'HEARTBEAT elapsed={int(time.monotonic()-begin)} started={started} complete={sum(r["complete"] for r in records)} active={len(active)} stop={stop_reason}', flush=True)
                heartbeat = time.monotonic()-begin
            if active:
                time.sleep(0.2)
        alive = all(x.poll() is None for x in loads)
        summary = {'mode': a.mode, 'first_run': a.first_run, 'requested': count, 'started': started,
                   'completed': sum(r['complete'] and 'cancelled' not in r for r in records),
                   'stop_reason': stop_reason, 'first_red': first_red, 'load_alive_through_end': alive,
                   'elapsed': time.monotonic()-begin, 'records': records}
        summary['good'] = (stop_reason is None and len(records) == count and
                           all(r['good'] for r in records) and alive)
        path = a.records / f'{a.mode}-summary.json'
        path.write_text(json.dumps(summary, indent=2)+'\n')
        print('CHUNK_RESULT ' + json.dumps(summary), flush=True)
        return 0 if summary['good'] else 1
    finally:
        if active:
            end_active('controller cleanup')
        for child in loads:
            if child.poll() is None:
                child.terminate()
            child.wait()
        lr.reap_adopted()


if __name__ == '__main__':
    sys.exit(main())
