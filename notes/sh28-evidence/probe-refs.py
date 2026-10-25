from pathlib import Path
import json
import sys
import termios
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools'))
import lib_session as ls
S = ROOT/'notes/sh28-evidence/probes'
S.mkdir(exist_ok=True)
refs = [(['dash','-i','+m'], 'dash'), (['bash','--posix','-i','+m'],'bash'), ([str(ROOT/'target/native/pelt'),'-i','+m'],'pelt')]
cases = {
 'quit': [r'\k echo kept\x1c\r'],
 'eol': ['stty eol @', r'\k echo term@\r'],
 'eol2': ['stty eol2 %', r'\k echo term%\r'],
 'flow': [r'\k echo kept\x13\x11\r'],
 'rprnt': [r'\k echo kept\x12\x07\r'],
 'discard': [r'\k echo kept\x0f\r'],
}
for case, steps in (cases.items() if '--fish-only' not in sys.argv else []):
    keys=S/(case+'.keys')
    keys.write_text('\n'.join(steps+['exit'])+'\n')
    for command,name in refs:
        a = ls.run(command, str(keys), {'env':r'PS1=$\s'})
        b = ls.run(command, str(keys), {'env':r'PS1=$\s'})
        assert ls.stdout_and_exit(a) == ls.stdout_and_exit(b), (name,case,'unstable')
        (S/(case+'-'+name+'.tr')).write_text('\n'.join(a)+'\n')
        print(case, name, ls.stdout_and_exit(a), flush=True)
for key in ['VEOL','VEOL2','VREPRINT','VDISCARD','VSWTC']:
    print('termios',key,getattr(termios,key,None), flush=True)
# Fish draws UI to stdout in lib_session's arrangement. Record command
# effects in a file, independently of those redisplay bytes and their timing.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from witness import Shell
import tempfile
for case, steps in {
    'fish-pageup':[b'out oldest\r', b'out newest\r', b'\x1b[5~\r'],
    'fish-pageup-active':[b'out oldest\r',b'out newest\r',b'\x10\x1b[5~\r'],
    'fish-pagedown':[b'out prior\r', b'out draft\x10\x1b[6~\r'],
    'fish-last-arg':[b'out older\r', b'out newer\r', b'out \x1b.\r'],
}.items():
    repeats=[]
    for repeat in range(2):
        with tempfile.TemporaryDirectory(prefix='sh28-fish.') as directory:
            home=Path(directory)
            result=home/'effects'
            init="function fish_prompt; printf '$ '; end; set -g fish_greeting; function out; printf '%s\\n' $argv >> " + str(result) + "; end"
            sh=Shell('fish', home, fullargv=['fish','--no-config','-i','-C',init], tty_out=True)
            try:
                for step in steps:
                    before={k:len(v) for k,v in sh.data.items()}
                    sh.type(step)
                    sh.until(lambda:any(b'$ ' in sh.data[k][before[k]:] for k in before))
                effects=result.read_text() if result.exists() else ''
                repeats.append(effects)
                (S/(case+'-'+str(repeat)+'.json')).write_text(json.dumps({k:v.decode('utf-8','backslashreplace') for k,v in sh.data.items()},indent=2)+'\n')
            finally:
                sh.close()
    assert repeats[0]==repeats[1],(case,repeats)
    (S/(case+'.effects')).write_text(repeats[0])
    print(case,repr(repeats[0]),flush=True)
