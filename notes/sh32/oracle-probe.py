"""Owned fresh-HOME ptys; only black-box fish outputs."""
import fcntl,json,os,pty,select,struct,subprocess,sys,tempfile,termios,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
import lib_session as ls
OUT=ROOT/'notes/sh32/oracle'; OUT.mkdir(exist_ok=True)
print(subprocess.check_output(['fish','--version']).decode().strip(),flush=True)
for cols in (24,40,80,200):
 with tempfile.TemporaryDirectory(prefix='sh32-fish-') as temp:
  home=Path(temp); path=home/'alpha'/'beta'/'日本語';path.mkdir(parents=True)
  env=dict(PATH='/usr/bin:/bin',HOME=temp,LC_ALL='C.UTF-8',TERM='xterm-256color',USER='mfwolffe')
  master,slave=pty.openpty();fcntl.ioctl(slave,termios.TIOCSWINSZ,struct.pack('HHHH',24,cols,0,0))
  p=subprocess.Popen(['fish','--no-config','-i','-C','set -g fish_greeting'],stdin=slave,stdout=slave,stderr=slave,env=env,cwd=home,start_new_session=True,preexec_fn=ls._ctty);os.close(slave)
  screen=ls.Screen(cols,24)
  def drain(seconds=.5):
   data=b'';end=time.monotonic()+seconds
   while time.monotonic()<end:
    if select.select([master],[],[],.01)[0]:
     try:chunk=os.read(master,65536)
     except OSError:break
     data+=chunk;screen.feed(chunk)
     if b'\x1b[0c' in chunk:os.write(master,b'\x1b[?1;2c')
     if screen.reply:os.write(master,screen.reply);screen.reply=b''
   return data
  rows=[dict(kind='home',raw=drain().hex(),screen=screen.snapshot(0))]
  for kind,keys in [('path',b'cd alpha/beta/'+ '日本語'.encode()+b'\r'),('failure',b'false\r'),('right',b'function fish_right_prompt; printf RIGHT; end\r'),('type',b'echo narrow'),('cancel',b'\x03')]:
   os.write(master,keys);raw=drain();rows.append(dict(kind=kind,input=keys.hex(),raw=raw.hex(),screen=screen.snapshot(0)))
  (OUT/f'fish-{os.getuid()}-{cols}.json').write_text(json.dumps(rows,indent=2)+'\n')
  for r in rows:print(cols,r['kind'],bytes.fromhex(r['raw']),flush=True)
  os.write(master,b'\x15exit\r');drain();p.wait(timeout=5);os.close(master)
