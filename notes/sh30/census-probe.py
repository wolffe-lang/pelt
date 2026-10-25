"""Count filesystem syscalls in the owned shell, not the driving Python."""
from pathlib import Path
import sys,tempfile,time
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from lib_shadow import Shell
with tempfile.TemporaryDirectory(prefix='sh30-census-') as d:
 home=Path(d);trace=home/'trace'
 argv=['strace','-f','-o',str(trace),'-e','trace=newfstatat,statx,getdents64',str(ROOT/'target/release/pelt'),'-i','+m','-o','highlight']
 sh=Shell('',home,fullargv=argv,tty_out=True,cols=80)
 def settle():
  end=time.monotonic()+.15
  while time.monotonic()<end:sh.pump(.001)
 try:
  settle();sh.type(b'\x0c');settle()
  before=trace.read_text().splitlines()
  sh.type(b'echo '+b'x'*75);settle()
  for i in range(100):sh.type(b'\x7fx');settle()
  after=trace.read_text().splitlines()
  delta=after[len(before):]
  print('prompt initialization filesystem calls:',len(before))
  print('80 typed characters + 200 edit keys filesystem calls:',len(delta))
  print('\n'.join(delta))
  assert not delta,delta
 finally:sh.close()
