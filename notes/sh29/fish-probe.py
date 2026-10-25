"""Black-box fish terminal measurements. No implementation files read."""
import json, os, pty, select, struct, subprocess, sys, tempfile, termios, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import lib_session as ls
OUT = ROOT/'notes/sh29/fish'
OUT.mkdir(exist_ok=True)
CASES = {
 'bang': [b'!'],
 'bangbang': [b'!!'],
 'bang-history': [b'! true\r', b'!'],
 'exact': [b'out old_suffix\r', b'out new_suffix\r', b'out '],
 'word-prefix': [b'out alpha beta_suffix\r', b'out beta'],
 'word-prefix-other-command': [b'out alpha beta_suffix\r', b'echo beta'],
 'word-prefix-first': [b'out alpha beta_suffix\r', b'beta'],
 'word-accept-alt': [b'out alpha-beta/gamma delta\r', b'out al', b'\x1bf'],
 'word-accept-ctrl': [b'out alpha-beta/gamma delta\r', b'out al', b'\x1b[1;5C'],
 'accept-right': [b'out suffix\r', b'out ', b'\x1b[C'],
 'accept-end': [b'out suffix\r', b'out ', b'\x1b[F'],
 'accept-ce': [b'out suffix\r', b'out ', b'\x05'],
 'accept-cf': [b'out suffix\r', b'out ', b'\x06'],
 'never-enter': [b'out suffix\r', b'out \r'],
 'clear-cu': [b'out suffix\r', b'out ', b'\x15'],
 'clear-cc': [b'out suffix\r', b'out ', b'\x03'],
 'clear-cl': [b'out suffix\r', b'out ', b'\x0c'],
 'midline': [b'out suffix\r', b'out ', b'\x02'],
 'up-prefix': [b'out alpha1\r', b'out beta\r', b'out alpha2\r', b'out al', b'\x1b[A', b'\x1b[A', b'\x1b[B', b'\x1b[B'],
 'pager-enter': [b'out alpha1\r', b'out beta\r', b'out al', b'\x12', b'\r'],
 'pager-escape': [b'out alpha1\r', b'out beta\r', b'out al', b'\x12', b'\x1b'],
 'pager-cc': [b'out alpha1\r', b'out beta\r', b'out al', b'\x12', b'\x03'],
 'pager-filter': [b'out alpha1\r', b'out beta\r', b'\x12', b'al', b'\x1b[B', b'\x12', b'\r'],
 'file-one': [b'out ./uni'],
 'file-many': [b'out ./sha'],
 'command': [b'fish_'],
 'tab': [b'out alphabet\r', b'out al', b'\t'],
 'edge': [b'out abcdefghijklmnopqrstuvwxyz\r', b'out abcdef'],
}
for term, color in [('xterm-256color',''),('linux',''),('dumb',''),('xterm-256color','truecolor')]:
 for name, steps in CASES.items():
  if term != 'xterm-256color' or color:
   if name not in ('exact', 'edge'): continue
  with tempfile.TemporaryDirectory(prefix='sh29-fish-') as temp:
   home=Path(temp)
   (home/'unique-file').touch(); (home/'shared-one').touch(); (home/'shared-two').touch()
   effects=home/'effects'; snapshot=home/'snapshot'
   init="function fish_prompt; printf '$ '; end; set -g fish_greeting; function out; printf '%s\\n' $argv >> " + str(effects) + "; end; bind ctrl-o 'printf \"%s\\n\" (commandline) (commandline --cursor) > " + str(snapshot) + "'"
   master,slave=pty.openpty()
   width=16 if name=='edge' else 80
   import fcntl
   fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack('HHHH',24,width,0,0))
   env=dict(PATH='/usr/bin:/bin',HOME=temp,LC_ALL='C.UTF-8',TERM=term,COLORTERM=color)
   p=subprocess.Popen(['fish','-i','-C',init],stdin=slave,stdout=slave,stderr=slave,env=env,cwd=temp,start_new_session=True,preexec_fn=ls._ctty)
   os.close(slave)
   screen=ls.Screen(width,24)
   def drain(seconds=.18):
    data=b''; until=time.monotonic()+seconds
    while time.monotonic()<until:
     if select.select([master],[],[],.01)[0]:
      try: chunk=os.read(master,65536)
      except OSError: break
      data+=chunk; screen.feed(chunk)
      if b'\x1b[0c' in chunk: os.write(master,b'\x1b[?1;2c')
      if screen.reply: os.write(master,screen.reply); screen.reply=b''
    return data
   rows=[dict(kind='start',raw=drain(.5).hex())]
   try:
    for step_index,step in enumerate(steps):
     os.write(master,step); raw=drain()
     snapraw=b''
     if step_index == len(steps)-1:
      os.write(master,b'\x0f'); snapraw=drain(.08)
     rows.append(dict(input=step.hex(),raw=raw.hex(),snapshot=snapshot.read_text() if snapshot.exists() else None,probe_raw=snapraw.hex()))
    result=dict(name=name,term=term,colorterm=color,width=width,rows=rows,effects=effects.read_text() if effects.exists() else '')
    target=OUT/(name+'-'+term+('-rgb' if color else '')+'.json')
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(target.name,repr(rows[-1].get('snapshot')),repr(result['effects']),flush=True)
   finally:
    os.write(master,b'\x03exit\r'); drain(.2)
    if p.poll() is None: p.kill()
    p.wait(); os.close(master)
