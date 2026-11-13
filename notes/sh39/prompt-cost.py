#!/usr/bin/env python3
"""Compare two prompt binaries in identical den repositories; 15 measured turns.
Usage: prompt-cost.py DEN BEFORE AFTER WORKDIR [SIZES...]
The initial prompt and next prompt are reported separately from steady state.
"""
import fcntl, importlib.machinery, importlib.util, json, os, pty, re, select, statistics, struct, subprocess, sys, termios, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
loader=importlib.machinery.SourceFileLoader('den_cost',str(ROOT/'notes/sh38/den-cost.py'))
spec=importlib.util.spec_from_loader(loader.name,loader);old=importlib.util.module_from_spec(spec);loader.exec_module(old)


def prompts(binary,cwd,env):
    master,slave=pty.openpty();fcntl.ioctl(slave,termios.TIOCSWINSZ,struct.pack('HHHH',30,160,0,0))
    def pre():fcntl.ioctl(0,termios.TIOCSCTTY,0)
    start=time.perf_counter()
    p=subprocess.Popen(['pelt','-i'],executable=binary,stdin=slave,stdout=slave,stderr=slave,cwd=cwd,env=env,start_new_session=True,preexec_fn=pre)
    os.close(slave)
    marker=b'# ' if os.geteuid()==0 else b'> '
    def prompt():
        out=b'';deadline=time.monotonic()+10
        while time.monotonic()<deadline:
            if select.select([master],[],[],.01)[0]:
                try:data=os.read(master,65536)
                except OSError:break
                out+=data
                if b'\x1b[6n' in data:os.write(master,b'\x1b[1;1R')
                if re.search(re.escape(marker)+rb'(\x1b\[0m)*$',out):return out
        raise RuntimeError('prompt deadline '+repr(out))
    times=[];kinds=[]
    def collect(start):
        raw=prompt();times.append((time.perf_counter()-start)*1000)
        kinds.append('stale' if b'\x1b[0;2m [vcs:' in raw else 'fresh' if b'[vcs:' in raw else 'none')
    try:
        collect(start)
        for _ in range(16):
            # Echoed command text never contains the friendly prompt marker.
            start=time.perf_counter();os.write(master,b'true\r');collect(start)
        os.write(master,b'exit\r');p.wait(timeout=5)
    finally:
        if p.poll() is None:p.kill();p.wait()
        os.close(master)
    return dict(first_two_ms=times[:2],median_ms=statistics.median(times[2:]),max_ms=max(times[2:]),kinds=kinds[2:])


def main():
    den,before,after,work=map(lambda x:str(Path(x).resolve()),sys.argv[1:5])
    sizes=list(map(int,sys.argv[5:])) or [10,100,400,2000,3000,5000,10000,20000]
    root=Path(work);root.mkdir(parents=True,exist_ok=True);home=root/'home';home.mkdir(exist_ok=True)
    bindir=root/'bin';bindir.mkdir(exist_ok=True)
    if not (bindir/'den').exists():(bindir/'den').symlink_to(den)
    base=dict(HOME=str(home),TMPDIR=os.environ['TMPDIR'],LC_ALL='C.UTF-8',TERM='xterm-256color',USER='tester',HOSTNAME='box')
    with_den=dict(base,PATH=str(bindir)+':/usr/bin:/bin');without=dict(base,PATH='/usr/bin:/bin')
    for n in sizes:
        cwd=old.make_repo(den,work,n,with_den)
        status,rows=old.status_cost(den,cwd,with_den)
        value=dict(files=n,status_median_ms=statistics.median(status),status_max_ms=max(status),rows=rows)
        value['before']=prompts(before,cwd,with_den)
        value['after']=prompts(after,cwd,with_den)
        value['baseline_before']=prompts(before,cwd,without)
        value['baseline_after']=prompts(after,cwd,without)
        print(json.dumps(value,sort_keys=True),flush=True)

if __name__=='__main__':main()
