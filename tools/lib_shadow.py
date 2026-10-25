"""Owned-pty and Linux idle counters, extracted from the sh28 witness.
Reusable fixture code; never inspects or signals unrelated processes.
"""
import os, json, ctypes, pty, select, subprocess, sys, termios, time
from pathlib import Path
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
