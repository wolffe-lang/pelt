"""External pty witnesses: real terminal gates, bindings, empty history, cost.
Run inside ctr.sh only; every child belongs to this container. No signals
are sent except SIGKILL to the exact still-live child pid during cleanup.
"""
import os
import json
import ctypes
from pathlib import Path
import pty
import select
import statistics
import subprocess
import sys
import tempfile
import termios
import time
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools'))
import lib_session as ls

def ctty_without_thp():
    """Child-only setting, inherited by pelt across exec (prctl(2const))."""
    ls._ctty()
    prctl = ctypes.CDLL(None, use_errno=True).prctl
    prctl.argtypes = [ctypes.c_int] + [ctypes.c_ulong] * 4
    prctl.restype = ctypes.c_int
    # Linux ABI values independently decoded in thp-prctl-trace.log.
    if prctl(41, 1, 0, 0, 0) != 0:
        raise OSError(ctypes.get_errno(), 'PR_SET_THP_DISABLE failed')
    if prctl(42, 0, 0, 0, 0) != 1:
        raise RuntimeError('PR_GET_THP_DISABLE did not confirm complete disable')


class Shell:
    def __init__(self, binary, home, args=(), tty_err=True, history=None, fullargv=None, tty_out=False, disable_thp=False):
        self.master, slave = pty.openpty()
        self.mode = ls._lmode(slave)
        env = dict(PATH='/usr/bin:/bin', HOME=str(home), LC_ALL='C', PS1='$ ', TERM='xterm', COLUMNS='1000')
        env['HISTFILE'] = str(home/('history-' + str(time.monotonic_ns())))
        if history:
            env.update(HISTFILE=str(history), HISTSIZE='32767')
        self.p = subprocess.Popen(fullargv or [str(binary), '-i', '+m', *args], stdin=slave,
            stderr=slave if tty_err else subprocess.PIPE, stdout=slave if tty_out else subprocess.PIPE,
            env=env, cwd=home, start_new_session=True, preexec_fn=ctty_without_thp if disable_thp else ls._ctty)
        os.close(slave)
        self.fds = {self.master: 'tty'}
        if not tty_out:
            self.fds[self.p.stdout.fileno()] = 'out'
        if not tty_err:
            self.fds[self.p.stderr.fileno()] = 'err'
        self.data = dict(tty=b'', out=b'', err=b'')
        self.screen = ls.Screen(1000, 24)
        self.until(lambda: any(b'$ ' in data for data in self.data.values()))
    def pump(self, timeout=.01):
        for fd in select.select(list(self.fds), [], [], timeout)[0]:
            try:
                data = os.read(fd, 65536)
            except OSError:
                data = b''
            if not data:
                self.fds.pop(fd, None)
                continue
            name = self.fds[fd]
            self.data[name] += data
            if name == 'tty':
                self.screen.feed(data)
                if self.screen.reply:
                    os.write(self.master, self.screen.reply)
                    self.screen.reply = b''
    def until(self, predicate, timeout=15):
        end = time.monotonic() + timeout
        while not predicate():
            if time.monotonic() >= end:
                raise AssertionError(f'timeout pid={self.p.pid}: {self.data!r}')
            self.pump(.001)
    def type(self, data):
        os.write(self.master, data)
    def command(self, data):
        before = len(self.data['tty'])
        self.type(data)
        self.until(lambda: b'$ ' in self.data['tty'][before:] or self.p.poll() is not None)
    def close(self):
        if self.p.poll() is None:
            self.type(b'\x15exit\r')
            end = time.monotonic() + 3
            while self.p.poll() is None and time.monotonic() < end:
                self.pump(.01)
        if self.p.poll() is None:
            os.kill(self.p.pid, 9)
        self.p.wait()
        self.pump(0)
        restored = ls.term_lmode(self.master, self.master) == self.mode
        os.close(self.master)
        return restored


def contexts(pid):
    result = 0
    for task in Path(f'/proc/{pid}/task').iterdir():
        for row in (task/'status').read_text().splitlines():
            if row.startswith(('voluntary_ctxt_switches:', 'nonvoluntary_ctxt_switches:')):
                result += int(row.split()[1])
    return result


def gates(binary, home):
    for name, args, tty_err, want in [
        ('on', ['-o','friendly'], True, b'ba\n'),
        ('default-off', [], True, b'ab\n'),
        ('no-stderr-tty', ['-o','friendly'], False, b'ab\n'),
        ('posix-hard-disable', ['--posix','-o','friendly'], True, b'ab\n'),
        ('feature-off', ['-o','friendly','+o','friendly_keys'], True, b'ab\n'),
    ]:
        shell = Shell(binary, home, args, tty_err)
        try:
            shell.type(b'echo ab\x14\r')
            shell.until(lambda: b'\n' in shell.data['out'])
            assert shell.data['out'] == want, (name, shell.data)
            print('ok gate', name, repr(want), flush=True)
        finally:
            assert shell.close(), 'mode not restored'
    # A pipe is input bytes, never editor commands, even with -i requested.
    source = b"printf '%s\\n' ab\x14\nexit\n"
    for args in [[], ['-i']]:
        got = subprocess.run([str(binary), *args, '-o','friendly'], input=source, capture_output=True, timeout=5)
        ref = subprocess.run(['dash', *args], input=source, capture_output=True, timeout=5)
        assert (got.stdout, got.returncode) == (ref.stdout, ref.returncode)
    got = subprocess.run([str(binary), '-o','friendly','-c','type bindings'], capture_output=True, timeout=5)
    assert got.returncode != 0 and b'builtin' not in got.stdout
    print('ok gates script, pipe, -c builtin absence', flush=True)


def interactive(binary, home):
    shell = Shell(binary, home, ['-o','friendly'])
    try:
        # No command has yet entered history: require a bell and no insertion.
        old = len(shell.data['tty'])
        shell.type(b'\x1b.')
        shell.until(lambda: b'\x07' in shell.data['tty'][old:])
        shell.command(b'echo empty\r')
        assert shell.data['out'] == b'empty\n'
        shell.data['out'] = b''
        shell.command(b'bindings\r')
        assert b'M-. / M-_\tESC . / ESC _\tyank-last-arg\n' in shell.data['out']
        assert b'stty intr\t03\tterminal-character\n' in shell.data['out']
        shell.data['out'] = b''
        shell.command(b'bindings -l\r')
        assert b'yank-last-arg\n' in shell.data['out']
        shell.data['out'] = b''
        shell.command(b'stty intr "^X"\r')
        shell.command(b'bindings\r')
        assert b'stty intr\t18\tterminal-character\n' in shell.data['out']
        shell.command(b'stty intr "^C"\r')
        for name, prefix in [('CSI', b'\x1b['), ('SS3', b'\x1bO'), ('C-x', b'\x18'), ('numeric', b'\x1b3'), ('find', b'\x1d')]:
            print('probe abort prefix', name, flush=True)
            seen = len(shell.data['tty'])
            shell.type(prefix + b'\x07')
            shell.until(lambda: b'\x07' in shell.data['tty'][seen:])
        shell.data['out'] = b''
        seen = len(shell.data['tty'])
        shell.type(b'echo kept\x12')
        shell.until(lambda: b"(search '" in shell.data['tty'][seen:])
        seen = len(shell.data['tty'])
        shell.type(b'\x07')
        shell.until(lambda: b'\x07' in shell.data['tty'][seen:])
        shell.command(b'\r')
        assert shell.data['out'] == b'kept\n', shell.data['out']
        print('ok abort bells in CSI, SS3, C-x, numeric, find and search', flush=True)
        shell.command(b'set -o vi\r')
        shell.data['out'] = b''
        shell.command(b'bindings\r')
        assert b'vi-yank-argument\n' in shell.data['out'] and b'\tyank-pop\n' not in shell.data['out']
        print('ok empty history bell; live bindings, actions, remapped stty, vi', flush=True)
    finally:
        assert shell.close(), 'mode not restored'


def idle_snapshot(pid):
    status = {}
    for row in Path(f'/proc/{pid}/status').read_text().splitlines():
        name, _, value = row.partition(':')
        if name in ('RssAnon', 'RssFile', 'RssShmem', 'VmRSS', 'Threads', 'THP_enabled'):
            status[name] = value.strip()
    rollup = {}
    for row in Path(f'/proc/{pid}/smaps_rollup').read_text().splitlines():
        name, _, value = row.partition(':')
        if name in ('Rss', 'Anonymous', 'AnonHugePages', 'Pss_Anon', 'Pss_File', 'Pss_Shmem'):
            rollup[name] = value.strip()
    stat = Path(f'/proc/{pid}/stat').read_text().split(') ', 1)[1].split()
    return {
        'pid': pid,
        'page_size_bytes': os.sysconf('SC_PAGE_SIZE'),
        'statm_resident_pages': int(Path(f'/proc/{pid}/statm').read_text().split()[1]),
        'status': status,
        'smaps_rollup': rollup,
        'contexts': contexts(pid),
        'cpu_ticks': int(stat[11]) + int(stat[12]),
        'minor_faults': int(stat[7]),
        'major_faults': int(stat[9]),
        'thp_enabled': Path('/sys/kernel/mm/transparent_hugepage/enabled').read_text().strip(),
    }


def cost(binary, home):
    history = home/'large-history'
    history.write_text(''.join(': z'+str(i)+'\n' for i in range(32767)))
    disable_thp = '--allow-thp' not in sys.argv[2:]
    shell = Shell(binary, home, ['-o','friendly'], history=history, disable_thp=disable_thp)
    try:
        ready = len(shell.data['tty'])
        shell.type(b'\x07')
        shell.until(lambda: b'\x07' in shell.data['tty'][ready:])
        for _ in range(10):
            shell.pump(.01)
        snap_before = idle_snapshot(shell.p.pid)
        print('idle before '+json.dumps(snap_before, sort_keys=True), flush=True)
        before = snap_before['contexts']
        rss = snap_before['statm_resident_pages']
        time.sleep(10)
        snap_after = idle_snapshot(shell.p.pid)
        print('idle after '+json.dumps(snap_after, sort_keys=True), flush=True)
        after = snap_after['contexts']
        rss2 = snap_after['statm_resident_pages']
        if disable_thp:
            assert snap_before['status']['THP_enabled'] == snap_after['status']['THP_enabled'] == '0'
            assert snap_before['smaps_rollup']['AnonHugePages'] == snap_after['smaps_rollup']['AnonHugePages'] == '0 kB'
        assert snap_before['thp_enabled'] == snap_after['thp_enabled'], 'host THP controls changed during sample'
        assert after == before, ('idle context switches', before, after)
        for counter in ('cpu_ticks', 'minor_faults', 'major_faults'):
            assert snap_before[counter] == snap_after[counter], ('idle process work', counter, snap_before[counter], snap_after[counter])
        assert snap_before['status']['RssAnon'] == snap_after['status']['RssAnon'], 'idle RssAnon changed'
        assert snap_before['smaps_rollup']['Anonymous'] == snap_after['smaps_rollup']['Anonymous'], 'idle accurate anonymous RSS changed'
        assert rss == rss2, ('idle total resident pages changed', rss, rss2)
        print(f'ok friendly idle 10s: contexts {after-before}, RSS pages {rss}->{rss2}, RssAnon {snap_before["status"]["RssAnon"]}->{snap_after["status"]["RssAnon"]}, child THP disabled={disable_thp}', flush=True)
        samples=[]
        for i in range(101):
            old = len(shell.data['tty'])
            shell.type(b'\x15echo ')
            shell.until(lambda: shell.data['tty'][old:].endswith(b'echo '))
            old = len(shell.data['tty'])
            start = time.perf_counter_ns()
            shell.type(b'\x1b.')
            shell.until(lambda: b'z32766' in shell.data['tty'][old:])
            samples.append((time.perf_counter_ns()-start)/1e6)
        median=statistics.median(samples[1:])
        p99=sorted(samples[1:])[98]
        print(f'last-arg 32767 entries: median {median:.6f} ms, p99 {p99:.6f} ms, 100 samples after warmup', flush=True)
        assert median < 1, median
    finally:
        assert shell.close(), 'mode not restored'

if __name__ == '__main__':
    binary = Path(sys.argv[1]).resolve()
    with tempfile.TemporaryDirectory(prefix='sh28-witness.') as directory:
        home = Path(directory)
        if '--cost-only' not in sys.argv[2:]:
            gates(binary, home)
            interactive(binary, home)
        cost(binary, home)
