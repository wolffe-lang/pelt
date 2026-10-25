"""Controlled script RSS/THP observations in owned child processes only."""
from pathlib import Path
import ctypes, json, os, select, subprocess, sys, tempfile, time
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
import lib_shadow
import runpy
shape=runpy.run_path(str(ROOT/'tools/shape-rss'))
libc=ctypes.CDLL(None,use_errno=True)
def no_thp():
    if libc.prctl(41,1,0,0,0) != 0 or libc.prctl(42,0,0,0,0) != 1:
        raise OSError('child THP disable failed')

def live(binary,n,disabled):
    with tempfile.TemporaryDirectory(prefix='sh30-rss-live-') as d:
        script=Path(d)/'shape.sh'
        script.write_text(shape['PRELUDE']+'true\n'*n+'echo READY\nread token\necho done\n')
        p=subprocess.Popen([str(binary),str(script)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                           env=shape['ENV'],cwd=d,preexec_fn=no_thp if disabled else None)
        try:
            if not select.select([p.stdout],[],[],30)[0]:raise AssertionError('no READY')
            assert p.stdout.readline()==b'READY\n'
            snap=lib_shadow.idle_snapshot(p.pid)
            out,err=p.communicate(b'continue\n',timeout=10)
            assert p.returncode==0 and out==b'done\n' and err==b'',(out,err,p.returncode)
            return snap
        finally:
            if p.poll() is None:p.kill();p.wait()

mode=sys.argv[1]
arms=[('trunk',ROOT.parent/'rss-trunk/target/native/pelt'),('colour',ROOT/'target/native/pelt')]
if mode=='repeat':
    for rep in range(30):
        for name,binary in arms if rep%2==0 else reversed(arms):
            with tempfile.TemporaryDirectory(prefix='sh30-rss-repeat-') as d:
                rows=[shape['run_file'](str(binary),'script','true',n,d) for n in [10000,20000]]
                assert all(row[1] for row in rows),rows
                growth=rows[1][0]-rows[0][0]
                print(json.dumps(dict(rep=rep,arm=name,kb=[r[0] for r in rows],growth_kb=growth,over_bar=growth>2000)),flush=True)
elif mode=='series':
    for disabled in (False,True):
        for name,binary in arms:
            with tempfile.TemporaryDirectory(prefix='sh30-rss-series-') as d:
                script=Path(d)/'shape.sh'
                script.write_text(shape['PRELUDE']+''.join('true\n'*10000+f'echo READY{k}\nread token\n' for k in range(1,11))+'echo done\n')
                p=subprocess.Popen([str(binary),str(script)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                   env=shape['ENV'],cwd=d,preexec_fn=no_thp if disabled else None)
                try:
                    rows=[]
                    for k in range(1,11):
                        assert select.select([p.stdout],[],[],30)[0],'no series marker'
                        assert p.stdout.readline()==f'READY{k}\n'.encode()
                        rows.append(lib_shadow.idle_snapshot(p.pid))
                        p.stdin.write(b'continue\n');p.stdin.flush()
                    out,err=p.communicate(timeout=10)
                    assert p.returncode==0 and out==b'done\n' and err==b''
                    print(json.dumps(dict(arm=name,disabled=disabled,rows=rows)),flush=True)
                finally:
                    if p.poll() is None:p.kill();p.wait()
elif mode=='live':
    for disabled in (False,True):
        for rep in range(3):
            for name,binary in arms:
                rows=[live(binary,n,disabled) for n in [10000,20000,100000,200000]]
                print(json.dumps(dict(rep=rep,arm=name,disabled=disabled,rows=rows)),flush=True)
