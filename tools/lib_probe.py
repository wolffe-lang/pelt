"""Owned probe descriptor regressions; no reference implementation source.

The C child observes descriptors before its first open (no interpreter startup
that could repair them). The direct rig adds a test entry to a disposable copy
of pelt's module, exercising the identity fallback even on Linux.
"""
from pathlib import Path
import json
import os
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CHILD = r'''
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>
int main(int argc, char **argv) {
    int a = fcntl(0, F_GETFL), b = fcntl(2, F_GETFL);
    struct stat sa, sb;
    int na = fstat(0, &sa) == 0 && S_ISCHR(sa.st_mode);
    int nb = fstat(2, &sb) == 0 && S_ISCHR(sb.st_mode);
    int fd = open(getenv("PELT_PROBE_LOG"), O_WRONLY|O_CREAT|O_APPEND, 0600);
    if (fd < 0) return 90;
    const char *name = strrchr(argv[0], '/'); name = name ? name+1 : argv[0];
    char row[512];
    int n = snprintf(row, sizeof row,
        "{\"name\":\"%s\",\"in\":%d,\"err\":%d,\"first\":%d,\"char0\":%d,\"char2\":%d}\n",
        name, a < 0 ? -1 : a & O_ACCMODE, b < 0 ? -1 : b & O_ACCMODE, fd, na, nb);
    if (write(fd, row, n) != n) return 91;
    close(fd);
    if (!strcmp(name, "hostname")) puts("box.example");
    else if (argc > 1 && !strcmp(argv[1], "--help")) puts("  --alpha  Probe option");
    else if (!strcmp(name, "den")) puts("?? owned-file");
    else puts("0");
    return 0;
}
'''
RIG = '''
pub fn probe_fixture(exe: str, kind: str) -> str {
    if kind == "identity" { return program_says(exe, []) }
    if kind == "prompt" {
        let (_ok, value) = prompt_probe(exe, [], os_clock_ns() + 50000000)
        return value
    }
    var e = editor_state(new_sh("probe"), "", Query {
        cols: 80, rows: 24, fixed: 0, col0: 0, cpr: 0, pend: "",
    }, [])
    completion_help(mut e, exe)
}
'''
MAIN = '''//! member: false
use sh
fn main() {
    let args = env_args()
    // Warm process/signal bookkeeping before the descriptor baseline.
    let _warm = sh.probe_fixture(args[0], args[1])
    print("READY")
    let _go = read_line() else ""
    var i = 0
    while i < 64 {
        let _value = sh.probe_fixture(args[0], args[1])
        i += 1
    }
    print("DONE")
    let _end = read_line() else ""
}
'''
# Linux-only fault injection changes our process's open calls, not /dev/null
# or the host. Child execs remove LD_PRELOAD, so a false spawn is recorded.
FAULT = r'''
#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <fcntl.h>
#include <stdarg.h>
#include <stdlib.h>
#include <string.h>
static int call_open(const char *p, int f, mode_t m, const char *symbol) {
    int (*real_open)(const char *, int, ...) = dlsym(RTLD_NEXT, symbol);
    const char *fail = getenv("PELT_NULL_FAIL");
    if (fail && !strcmp(p, "/dev/null") &&
        ((!strcmp(fail,"in") && (f&O_ACCMODE)==O_RDONLY) ||
         (!strcmp(fail,"err") && (f&O_ACCMODE)==O_WRONLY))) {
        errno = EACCES; return -1;
    }
    return real_open(p, f, m);
}
int open(const char *p, int f, ...) {
    mode_t m=0; if (f&O_CREAT) { va_list a; va_start(a,f); m=va_arg(a,int); va_end(a); }
    return call_open(p,f,m,"open");
}
int open64(const char *p, int f, ...) {
    mode_t m=0; if (f&O_CREAT) { va_list a; va_start(a,f); m=va_arg(a,int); va_end(a); }
    return call_open(p,f,m,"open64");
}
'''


def rows(log):
    return [json.loads(line) for line in log.read_text().splitlines()]


def witness(binary, ready, step):
    failures = []

    def check(name, ok, detail):
        print(('ok ' if ok else 'FAIL ') + name + ' ' + str(detail), flush=True)
        if not ok:
            failures.append(name)

    def descriptors(name, reports):
        check(name, bool(reports) and all(
            r['in'] == os.O_RDONLY and r['err'] == os.O_WRONLY and
            r['first'] >= 3 and r['char0'] and r['char2'] for r in reports), reports)

    with tempfile.TemporaryDirectory(prefix='sh36-probes-') as temp:
        home = Path(temp)
        bindir = home / 'bin'
        bindir.mkdir()
        source = home / 'child.c'
        source.write_text(CHILD)
        subprocess.run(['cc', '-Wall', '-Wextra', '-Werror', str(source), '-o', str(bindir/'den')], check=True)
        for name in ('hostname', 'probe', 'identity'):
            shutil.copy2(bindir/'den', bindir/name)
        log = home / 'report'
        log.touch()
        env = dict(os.environ, PELT_PROBE_LOG=str(log))
        # Warm owned executables, then clear their reports before the session.
        for file in bindir.iterdir():
            subprocess.run([str(file)], env=env, check=True, capture_output=True)
        log.write_text('')
        sh = ready(binary, home, env={'PATH':str(bindir)+':/usr/bin:/bin',
                                     'HOSTNAME':None, 'PELT_PROBE_LOG':str(log)})
        try:
            report = rows(log)
            for name in ('den', 'hostname'):
                descriptors('probe-' + name + '-fds', [r for r in report if r['name'] == name])
            check('probe-vcs-output', b'[vcs:1]' in sh.data['tty'], 'stdout pipe retained')
            step(sh, b'probe --')
            before = len(rows(log))
            step(sh, b'\t')
            descriptors('probe-help-fds', [r for r in rows(log)[before:] if r['name'] == 'probe'])
            step(sh, b'\x07\x15')
        finally:
            assert sh.close()
        for redirect, fd in [('2>&-', 'err'), ('<&-', 'in')]:
            log.write_text('')
            p = subprocess.run([str(binary), '-c', str(bindir/'probe')+' '+redirect],
                               env=env, capture_output=True, timeout=10)
            report = rows(log)
            check('probe-user-close-'+fd, p.returncode == 0 and len(report)==1 and
                  report[0][fd] == -1 and report[0]['first'] == (2 if fd=='err' else 0), report)

        # Build from an exact copy of the committed module, adding only an
        # internal test entry. No production symbol is exposed for the rig.
        src = home / 'src'
        shutil.copytree(ROOT/'src/sh', src/'sh')
        (src/'sh/probe_fixture.lu').write_text(RIG)
        (src/'probe.lu').write_text(MAIN)
        rig = home / 'rig'
        wolf = os.environ.get('WOLF_BIN', str(ROOT/'.wolf-bin/wolf'))
        command = [wolf, 'build', '--deny-warnings', str(src/'probe.lu'), '-o', str(rig)]
        if binary.parent.name == 'release':
            command.append('--release')
        subprocess.run(command, check=True)
        fault = home/'fault.so'
        if os.uname().sysname == 'Linux':
            (home/'fault.c').write_text(FAULT)
            subprocess.run(['cc','-shared','-fPIC',str(home/'fault.c'),'-ldl','-o',str(fault)], check=True)

        def run_rig(kind, exe, extra=None):
            log.write_text('')
            p = subprocess.Popen([str(rig),str(exe),kind], env=dict(env, **(extra or {})),
                                 stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                assert p.stdout.readline() == b'READY\n'
                fdpath = Path('/proc')/str(p.pid)/'fd'
                baseline = len(list(fdpath.iterdir())) if fdpath.exists() else None
                p.stdin.write(b'go\n'); p.stdin.flush()
                assert p.stdout.readline() == b'DONE\n'
                after = len(list(fdpath.iterdir())) if baseline is not None else None
                p.stdin.write(b'end\n'); p.stdin.flush()
                _, err = p.communicate(timeout=10)
                assert p.returncode == 0, err
                if baseline is not None:
                    check('probe-'+kind+'-cleanup', baseline==after, (baseline,after,extra))
                else:
                    print('SKIP probe-'+kind+'-fd-count Linux proc counters unavailable', flush=True)
                return rows(log)
            finally:
                if p.poll() is None:
                    p.kill(); p.wait()
        for kind in ('identity','prompt','help'):
            report = run_rig(kind, bindir/'identity')
            descriptors('probe-'+kind+'-direct-fds', report)
            check('probe-'+kind+'-repeated', len(report)==65, len(report))
            report = run_rig(kind, home/'missing')
            check('probe-'+kind+'-spawn-failure', not report, report)
            if fault.exists():
                for fail in ('in','err'):
                    report = run_rig(kind, bindir/'identity',
                                     {'LD_PRELOAD':str(fault), 'PELT_NULL_FAIL':fail})
                    check('probe-'+kind+'-null-failure-'+fail, not report, report[:2])
            else:
                print('SKIP probe-'+kind+'-null-failure Linux open interposition unavailable',flush=True)
    assert not failures, failures
