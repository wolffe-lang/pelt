"""External pty witnesses: real terminal gates, bindings, empty history, cost.
Run inside ctr.sh only; every child belongs to this container. No signals
are sent except SIGKILL to the exact still-live child pid during cleanup.
"""
import os
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

class Shell:
    def __init__(self, binary, home, args=(), tty_err=True, history=None, fullargv=None, tty_out=False):
        self.master, slave = pty.openpty()
        self.mode = ls._lmode(slave)
        env = dict(PATH='/usr/bin:/bin', HOME=str(home), LC_ALL='C', PS1='$ ', TERM='xterm', COLUMNS='1000')
        env['HISTFILE'] = str(home/('history-' + str(time.monotonic_ns())))
        if history:
            env.update(HISTFILE=str(history), HISTSIZE='32767')
        self.p = subprocess.Popen(fullargv or [str(binary), '-i', '+m', *args], stdin=slave,
            stderr=slave if tty_err else subprocess.PIPE, stdout=slave if tty_out else subprocess.PIPE,
            env=env, cwd=home, start_new_session=True, preexec_fn=ls._ctty)
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
        shell.command(b'set -o vi\r')
        shell.data['out'] = b''
        shell.command(b'bindings\r')
        assert b'vi-yank-argument\n' in shell.data['out'] and b'\tyank-pop\n' not in shell.data['out']
        print('ok empty history bell; live bindings, actions, remapped stty, vi', flush=True)
    finally:
        assert shell.close(), 'mode not restored'


def cost(binary, home):
    history = home/'large-history'
    history.write_text(''.join(': z'+str(i)+'\n' for i in range(32767)))
    shell = Shell(binary, home, ['-o','friendly'], history=history)
    try:
        ready = len(shell.data['tty'])
        shell.type(b'\x07')
        shell.until(lambda: b'\x07' in shell.data['tty'][ready:])
        for _ in range(10):
            shell.pump(.01)
        before = contexts(shell.p.pid)
        rss = Path(f'/proc/{shell.p.pid}/statm').read_text().split()[1]
        time.sleep(10)
        after = contexts(shell.p.pid)
        rss2 = Path(f'/proc/{shell.p.pid}/statm').read_text().split()[1]
        assert after - before <= 2 and rss == rss2, (before, after, rss, rss2)
        print(f'ok friendly idle 10s: contexts {after-before}, RSS pages {rss}->{rss2}', flush=True)
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
        gates(binary, home)
        interactive(binary, home)
        cost(binary, home)
