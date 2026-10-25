from pathlib import Path
import sys,tempfile,time
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from lib_shadow import Shell
with tempfile.TemporaryDirectory() as d:
 sh=Shell(ROOT/'target/release/pelt',Path(d),['-o','highlight'],tty_out=True,cols=80)
 try:
  for k in [b'e',b'cho hello',b'\x15',b'echo )',b'\r']:
   old=len(sh.data['tty']);sh.type(k)
   end=time.monotonic()+.2
   while time.monotonic()<end:sh.pump(.001)
   print(repr(k),repr(sh.data['tty'][old:]),flush=True)
 finally:sh.close()
