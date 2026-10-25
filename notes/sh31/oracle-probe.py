"""Fresh HOME pty behavior only; never read an implementation's source."""
import fcntl, json, os, pty, select, struct, subprocess, sys, tempfile, termios, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
import lib_session as ls
OUT=ROOT/'notes/sh31/oracle'; OUT.mkdir(exist_ok=True)
cases=[
 ('fish','abbr-space',80,"abbr --add zz 'echo expanded'",[b'zz',b' ',b'argument',b'\r']),
 ('fish','abbr-enter',80,"abbr --add zz 'echo expanded'",[b'zz',b'\r']),
 ('fish','abbr-position',80,"abbr --add zz 'echo expanded'",[b'echo zz ',b'\x15  zz ',b'\x15echo x; zz ']),
 ('fish','abbr-quoted',80,"abbr --add zz 'echo expanded'",[b"'zz' ",b'\x15"zz" ',b'\x15z\\z ']),
 ('fish','abbr-undo',80,"abbr --add zz 'echo expanded'",[b'zz ',b'\x1f',b'\x03']),
 ('fish','abbr-empty',80,"abbr --add zz ''",[b'zz ',b'\r']),
]
for cols in (24,40,80,120):
 init="function zz; end; complete -c zz -f; " + '; '.join("complete -c zz -a '"+word+"' -d '"+desc+"'" for word,desc in [('alpha','First choice'),('beta','Second choice'),('gamma','Third choice'),('delta','Fourth choice'),('epsilon','Fifth choice'),('zeta','Sixth choice')])
 cases.append(('fish','pager-'+str(cols),cols,init,[b'zz ',b'\t',b'\t',b'\x1b[Z',b'\x1b[B',b'\r',b'\x1b']))
for name,steps in [
 ('previous',[b'echo first last\r',b'!!\r',b'history 3\r']),
 ('last-word',[b"echo one 'two three'\r",b'echo !$\r',b'history 3\r']),
 ('quotes',[b'echo old last\r',b"echo '!!'\r",b'echo "!!"\r']),
 ('escape-comment',[b'echo old last\r',b'echo \\!! # !!\r']),
 ('missing',[b'!!\r',b'\x15echo !$\r']),
 ('redir',[b'echo one > output\r',b'echo !$\r']),
 ('comment-word',[b'echo one # last comment\r',b'echo !$\r'])]:
 cases.append(('bash',name,80,'',steps))
for shell,name,cols,init,steps in cases:
 with tempfile.TemporaryDirectory(prefix='sh31-oracle-') as temp:
  home=Path(temp); snap=home/'snapshot'
  env=dict(PATH='/usr/bin:/bin',HOME=temp,LC_ALL='C.UTF-8',TERM='xterm-256color',PS1='$ ',HISTFILE=str(home/'history'))
  if shell=='fish':
   setup="function fish_prompt; printf '$ '; end; set -g fish_greeting; "+init+"; bind ctrl-o 'printf \"%s\\n\" (commandline) (commandline --cursor) > "+str(snap)+"'"
   argv=['fish','--no-config','-i','-C',setup]
  else: argv=['bash','--noprofile','--norc','-i']
  master,slave=pty.openpty(); fcntl.ioctl(slave,termios.TIOCSWINSZ,struct.pack('HHHH',24,cols,0,0))
  p=subprocess.Popen(argv,stdin=slave,stdout=slave,stderr=slave,env=env,cwd=home,start_new_session=True,preexec_fn=ls._ctty);os.close(slave)
  screen=ls.Screen(cols,24)
  def drain(seconds=.2):
   data=b''; end=time.monotonic()+seconds
   while time.monotonic()<end:
    if select.select([master],[],[],.01)[0]:
     try: chunk=os.read(master,65536)
     except OSError: break
     data+=chunk;screen.feed(chunk)
     if b'\x1b[0c' in chunk:os.write(master,b'\x1b[?1;2c')
     if screen.reply:os.write(master,screen.reply);screen.reply=b''
   return data
  rows=[dict(kind='start',raw=drain(.5).hex())]
  for keys in steps:
   os.write(master,keys);raw=drain()
   snapshot=None
   if shell=='fish':
    os.write(master,b'\x0f');drain(.05)
    if snap.exists(): snapshot=snap.read_text()
   rows.append(dict(input=keys.hex(),raw=raw.hex(),buffer=snapshot,screen=screen.snapshot(0)))
  (OUT/(shell+'-'+name+'.json')).write_text(json.dumps(dict(shell=shell,name=name,cols=cols,rows=rows),indent=2)+'\n')
  print(shell,name,[(bytes.fromhex(r['input']),r['buffer'] if shell=='fish' else bytes.fromhex(r['raw'])) for r in rows[1:]],flush=True)
  os.write(master,b'\x03');drain(.2);os.write(master,b'\x15exit\r');drain(.2);p.wait(timeout=5);os.close(master)
