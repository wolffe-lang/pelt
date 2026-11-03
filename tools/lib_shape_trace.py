"""Bounded, failure-only diagnostics for a shell row's original IO/deadline."""
from collections import deque
import json
import os
from pathlib import Path
import select
import subprocess
import sys
import time

import lib_reap as lr


def process_snapshot(pid):
    out = {"pid": pid}
    base = Path('/proc') / str(pid)
    if base.exists():
        for key in ('status', 'stat', 'wchan', 'syscall', 'schedstat'):
            try:
                out[key] = (base / key).read_text()[:16384]
            except OSError as e:
                out[key] = str(e)
        try:
            tasks = sorted((base / 'task').iterdir())
            out['thread_count'] = len(tasks)
            out['threads'] = []
            for task in tasks[:32]:
                row = {'tid': int(task.name)}
                for key in ('status', 'wchan', 'syscall', 'schedstat', 'children'):
                    try:
                        row[key] = (task / key).read_text()[:16384]
                    except OSError as e:
                        row[key] = str(e)
                out['threads'].append(row)
        except OSError as e:
            out['threads_error'] = str(e)
    elif not sys.platform.startswith('linux'):
        try:
            p = subprocess.run(['ps', '-p', str(pid), '-o', 'pid=,ppid=,pgid=,stat=,comm='],
                               capture_output=True, text=True, timeout=2)
            out['ps'] = p.stdout.strip()
        except (OSError, subprocess.TimeoutExpired) as e:
            out['ps_error'] = str(e)
    else:
        out['absent'] = True
    return out


class ShapeTrace:
    def __init__(self, path=None, label='', capacity=96):
        self.path = Path(path) if path else None
        self.events = deque(maxlen=capacity)
        self.data = {'label': label, 'event_capacity': capacity, 'deadline_seconds': 10}
        self.process = None

    def event(self, kind, **fields):
        if self.path is not None:
            self.events.append({'kind': kind, 'wall': time.time(),
                                'mono': time.monotonic(), **fields})

    def attach(self, p):
        self.process = p
        self.data['pelt_pid'] = p.pid

    def write(self, fd, data):
        start = time.monotonic()
        count = os.write(fd, data)
        self.event('write', fd=fd, data=repr(data[:1024]), requested=len(data),
                   written=count, elapsed=time.monotonic()-start)
        if self.path is not None:
            self.data['last_write'] = {'fd': fd, 'data': repr(data), 'requested': len(data),
                                       'written': count, 'wall': time.time(), 'mono': time.monotonic()}
        return count

    def read(self, fd, count):
        start = time.monotonic()
        try:
            data = os.read(fd, count)
        except OSError as e:
            self.event('read_error', fd=fd, error=str(e), elapsed=time.monotonic()-start)
            raise
        self.event('read', fd=fd, data=repr(data[:1024]), bytes=len(data),
                   elapsed=time.monotonic()-start)
        return data

    def select(self, fds, timeout, deadline=None):
        start_m, start_w = time.monotonic(), time.time()
        ready = select.select(fds, [], [], timeout)[0]
        self.event('select', fds=[f.fileno() if hasattr(f, 'fileno') else f for f in fds],
                   ready=[f.fileno() if hasattr(f, 'fileno') else f for f in ready], requested_timeout=timeout,
                   elapsed_mono=time.monotonic()-start_m, elapsed_wall=time.time()-start_w,
                   prompt_deadline_wall=deadline)
        return ready

    def failure(self, reason, p, roles, buffers, turn=None, rows=None, *, publish=True, read_pending=True):
        if self.path is None or 'before_cleanup' in self.data:
            return
        before = {'reason': reason, 'wall': time.time(), 'mono': time.monotonic(),
                  'turn': turn, 'rows_kib': rows, 'poll': p.poll(),
                  'pelt': process_snapshot(p.pid), 'rig': process_snapshot(os.getpid()),
                  'buffers': {k: {'bytes': len(v), 'tail': repr(v[-8192:])}
                              for k, v in buffers.items() if isinstance(v, bytes)},
                  'fd_roles': roles, 'pending_after_failure': []}
        try:
            table = lr._table()
            below = sorted(lr._below({p.pid}, table) - {p.pid})
            before['child_count'] = len(below)
            before['children'] = [process_snapshot(pid) for pid in below[:64]]
        except OSError as e:
            before['children_error'] = str(e)
        # The verdict is already failure. Reading queued bytes now is
        # forensic only: it never changes the False return or deadline.
        self.data['failed'] = publish
        try:
            readable = [fd for role, fd in roles.items() if role != 'stdin']
            ready = select.select(readable, [], [], 0)[0] if read_pending else []
            for fd in ready:
                try:
                    data = os.read(fd, 65536)
                    before['pending_after_failure'].append({'fd': fd, 'data': repr(data), 'bytes': len(data)})
                except OSError as e:
                    before['pending_after_failure'].append({'fd': fd, 'error': str(e)})
        except (OSError, ValueError) as e:
            before['pending_error'] = str(e)
        self.data['before_cleanup'] = before
        if publish:
            self.emit(reason)

    def finish(self, p):
        self.data['returncode_after_cleanup'] = p.returncode
        if self.data.get('failed'):
            self.emit(self.data['before_cleanup']['reason'])

    def emit(self, reason, **result):
        if self.path is None:
            return None
        payload = {**self.data, 'reason': reason, 'result': result, 'events': list(self.events)}
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            temporary = self.path.with_name(self.path.name + f'.tmp-{os.getpid()}')
            temporary.write_text(json.dumps(payload, indent=2) + '\n')
            temporary.replace(self.path)
            return str(self.path)
        except OSError as e:
            print(f'shape-rss: trace write failed: {e}', file=sys.stderr)
            return None
