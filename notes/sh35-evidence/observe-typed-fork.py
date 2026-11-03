#!/usr/bin/env python3
"""Observe f423b34's unchanged typed-fork row; bounded loaded/quiet chunks."""
import argparse
from collections import deque
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import select
import subprocess
import sys
import time

p = argparse.ArgumentParser()
p.add_argument('mode', choices=('loaded', 'quiet', 'one'))
p.add_argument('records', type=Path)
p.add_argument('--run', type=int, default=1)
p.add_argument('--runs', type=int, default=64)
a = p.parse_args()
a.records.mkdir(parents=True, exist_ok=True)
root = Path('/work')
loader = importlib.machinery.SourceFileLoader('observed_shape', str(root / 'tools/shape-rss'))
spec = importlib.util.spec_from_loader(loader.name, loader)
shape = importlib.util.module_from_spec(spec)
loader.exec_module(shape)
text = next(r[2] for r in shape.SHAPES if r[0] == 'typed-fork-subshell')
N = 10000


def proc(pid):
    base = Path('/proc') / str(pid)
    out = {'pid': pid}
    for f in ('status', 'stat', 'wchan', 'syscall', 'schedstat'):
        try:
            out[f] = (base / f).read_text()[:20000]
        except OSError as e:
            out[f] = str(e)
    try:
        out['threads'] = []
        for task in sorted((base / 'task').iterdir()):
            row = {'tid': int(task.name)}
            for f in ('status', 'wchan', 'syscall', 'schedstat', 'children'):
                try:
                    row[f] = (task / f).read_text()[:20000]
                except OSError as e:
                    row[f] = str(e)
            out['threads'].append(row)
    except OSError as e:
        out['threads_error'] = str(e)
    return out


def one():
    ring = deque(maxlen=96)
    state = {'run': a.run, 'n': N, 'text': text, 'sent_lines': 0}
    original_read, original_write = os.read, os.write
    original_select, original_popen = select.select, subprocess.Popen
    original_end = shape.lr.end_tree
    target = {}
    expected_line = (text + '; i=$((i+1))\n').encode()
    trace_path = a.records / f'run-{a.run:03}.trace.json'

    def event(kind, **data):
        row = {'kind': kind, 'mono': time.monotonic(), 'wall': time.time(), **data}
        ring.append(row)
        return row

    def launch(*args, **kwargs):
        child = original_popen(*args, **kwargs)
        target['p'] = child
        state['pelt_pid'] = child.pid
        (a.records / f'run-{a.run:03}.pelt-pid').write_text(str(child.pid) + '\n')
        return child

    def sent(fd, data):
        before = time.monotonic()
        wrote = original_write(fd, data)
        if data == expected_line:
            state['sent_lines'] += 1
        row = event('write', fd=fd, data=repr(data[:1024]), requested=len(data), written=wrote,
                    elapsed=time.monotonic()-before, line=state['sent_lines'])
        state['last_send'] = row
        return wrote

    def received(fd, count):
        before = time.monotonic()
        try:
            data = original_read(fd, count)
        except OSError as e:
            event('read-error', fd=fd, error=str(e), elapsed=time.monotonic()-before)
            raise
        row = event('read', fd=fd, data=repr(data[:1024]), bytes=len(data), elapsed=time.monotonic()-before)
        if data.endswith(b'$ '):
            state['last_prompt_read'] = row
        if not data and 'exit_observation' not in state and 'p' in target:
            child = target['p']
            observation = proc(child.pid)
            observation['poll'] = child.poll()
            state['exit_observation'] = observation
        return data

    def selected(readers, writers, errors, timeout=None):
        frame = sys._getframe(1)
        deadline = frame.f_locals.get('deadline') if frame.f_code.co_name == 'wait_prompt' else None
        start_m, start_w = time.monotonic(), time.time()
        ready = original_select(readers, writers, errors, timeout)
        row = event('select', readers=list(readers), ready=list(ready[0]), requested_timeout=timeout,
                    elapsed_mono=time.monotonic()-start_m, elapsed_wall=time.time()-start_w,
                    prompt_deadline_wall=deadline)
        state['max_select_elapsed'] = max(state.get('max_select_elapsed', 0), row['elapsed_mono'])
        state['max_wall_mono_difference'] = max(state.get('max_wall_mono_difference', 0), abs(row['elapsed_wall']-row['elapsed_mono']))
        if deadline is not None:
            state['last_prompt_select'] = row
        return ready

    def before_cleanup(pid, before=frozenset()):
        # The row has already decided failure. Observing/draining here
        # cannot turn its False return into True or extend its deadline.
        frame = sys._getframe(1)
        loc = frame.f_locals if frame.f_code.co_name == 'run_typed' else {}
        child = target.get('p')
        snap = {'mono': time.monotonic(), 'wall': time.time(), 'line': loc.get('k'),
                'pre_cleanup_poll': child.poll() if child else None,
                'pelt': proc(pid), 'rig': proc(os.getpid())}
        got = loc.get('got', {})
        snap['rig_buffers'] = {k: {'bytes': len(v), 'tail': repr(v[-8192:])} for k,v in got.items() if isinstance(v, bytes)}
        snap['pending_after_failure'] = []
        fds = [loc[k] for k in ('rout', 'rerr', 'master') if k in loc]
        for fd in original_select(fds, [], [], 0)[0]:
            try:
                data = original_read(fd, 65536)
                snap['pending_after_failure'].append({'fd': fd, 'data': repr(data), 'bytes': len(data)})
            except OSError as e:
                snap['pending_after_failure'].append({'fd': fd, 'error': str(e)})
        state['before_cleanup'] = snap
        trace_path.write_text(json.dumps({**state, 'events': list(ring)}, indent=2) + '\n')
        return original_end(pid, before)

    os.read, os.write, select.select, subprocess.Popen = received, sent, selected, launch
    shape.lr.end_tree = before_cleanup
    start = time.monotonic()
    try:
        rows, good, why = shape.run_typed('/work/target/native/pelt', text, N)
    finally:
        os.read, os.write, select.select, subprocess.Popen = original_read, original_write, original_select, original_popen
        shape.lr.end_tree = original_end
    state['post_return_poll'] = target['p'].poll() if 'p' in target else None
    state['cleanup_called'] = 'before_cleanup' in state
    grew = rows[1] - rows[0]
    memory_ok = grew <= N * 100 // 1024 + 1024
    result = {'run': a.run, 'verdict': 'ok' if good and memory_ok else 'FAIL', 'answer_ok': good,
              'memory_ok': memory_ok, 'rows_kib': rows, 'why': why, 'elapsed': time.monotonic()-start,
              'pelt_pid': state.get('pelt_pid'), 'sent_lines': state['sent_lines'],
              'max_select_elapsed': state.get('max_select_elapsed', 0),
              'max_wall_mono_difference': state.get('max_wall_mono_difference', 0),
              'post_return_poll': state['post_return_poll'], 'cleanup_called': state['cleanup_called']}
    if result['verdict'] != 'ok':
        trace_path.write_text(json.dumps({**state, 'result': result, 'events': list(ring)}, indent=2) + '\n')
        result['trace'] = str(trace_path)
    (a.records / f'run-{a.run:03}.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result), flush=True)
    return 0 if result['verdict'] == 'ok' else 1


def chunk():
    shape.lr.subreaper()
    workers = 4 if a.mode == 'loaded' else 1
    loads, active, results, aborted = [], {}, [], []
    start = time.monotonic()
    next_run, stopped, last_beat = 1, False, -60
    try:
        if a.mode == 'loaded':
            loads = [subprocess.Popen([sys.executable, '-c', 'while True: pass']) for _ in range(4)]
        print(f'CHUNK_START mode={a.mode} max_runs={a.runs} workers={workers} loads={len(loads)} affinity={sorted(os.sched_getaffinity(0))} row_n={N} deadline_seconds=10', flush=True)
        while active or (not stopped and next_run <= a.runs):
            now = time.monotonic()
            if now-start >= 5400:
                stopped = True
            while not stopped and len(active) < workers and next_run <= a.runs:
                log = (a.records / f'run-{next_run:03}.helper.log').open('w')
                child = subprocess.Popen([sys.executable, '-I', __file__, 'one', str(a.records), '--run', str(next_run)], stdout=log, stderr=subprocess.STDOUT)
                active[child.pid] = (child, next_run, now, log)
                next_run += 1
            for pid, (child, number, began, log) in list(active.items()):
                if child.poll() is None and (now-began > 600 or now-start > 6000):
                    before = {p for p in active if p != pid} | {p.pid for p in loads}
                    snapshot = {'run': number, 'reason': 'safety budget, NOT a row verdict', 'helper': proc(pid)}
                    pidfile = a.records / f'run-{number:03}.pelt-pid'
                    if pidfile.exists():
                        snapshot['pelt'] = proc(int(pidfile.read_text()))
                    (a.records / f'run-{number:03}.aborted.json').write_text(json.dumps(snapshot, indent=2) + '\n')
                    shape.lr.end_tree(pid, before)
                    child.wait()
                    aborted.append(number)
                    stopped = True
                code = child.poll()
                if code is not None:
                    log.close()
                    path = a.records / f'run-{number:03}.json'
                    if number not in aborted:
                        if not path.exists():
                            raise RuntimeError(f'helper {number} exited {code} without a row record')
                        record = json.loads(path.read_text())
                        results.append(record)
                        print('ROW ' + json.dumps(record), flush=True)
                        if record['verdict'] != 'ok':
                            stopped = True
                    # Reap/terminate only descendants this chunk adopted
                    # from its finished helper; other helpers/loads excluded.
                    before = {p for p in active if p != pid} | {p.pid for p in loads}
                    shape.lr.end_tree(pid, before)
                    shape.lr.reap_adopted(before)
                    del active[pid]
            if now-start-last_beat >= 60:
                print(f'HEARTBEAT mode={a.mode} elapsed={int(now-start)} complete={len(results)} red={sum(r["verdict"]!="ok" for r in results)} active={len(active)}', flush=True)
                last_beat = now-start
            if active:
                time.sleep(0.2)
        summary = {'mode': a.mode, 'requested': a.runs, 'completed': len(results),
                   'red': [r for r in results if r['verdict'] != 'ok'], 'aborted': aborted,
                   'elapsed': time.monotonic()-start, 'workers': workers, 'loads': len(loads),
                   'load_alive_through_end': all(p.poll() is None for p in loads)}
        (a.records / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
        print('CHUNK_RESULT ' + json.dumps(summary), flush=True)
        return 0 if not summary['red'] and not aborted and summary['completed'] == a.runs and summary['load_alive_through_end'] else 1
    finally:
        for pid, (child, _, _, log) in list(active.items()):
            if child.poll() is None:
                shape.lr.end_tree(pid, {p for p in active if p != pid} | {p.pid for p in loads})
            child.wait()
            log.close()
        for child in loads:
            if child.poll() is None:
                child.terminate()
            child.wait()


if __name__ == '__main__':
    sys.exit(one() if a.mode == 'one' else chunk())
