"""Pin UI only after independently specified output and terminal-mode checks."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
import lib_session as ls
expected=json.loads((ROOT/'notes/sh29/expected.json').read_text())
selected=sys.argv[1:] or list(expected)
for name in selected:
 keys=str(ROOT/'tests/session'/(name+'.keys')); meta=ls.read_meta(keys[:-5]+'.meta')
 a=ls.run(ls.argv_for(str(ROOT/'target/native/pelt'),meta,True),keys,meta)
 screens=ls.last_screens
 out=[]
 for row in a:
  if row.startswith('step '): out.append('')
  elif row.startswith('out '): out[-1]=json.loads(row[4:])
 want=['']+expected[name]
 if out!=want or a[-1]!=f'exit 0 at step {len(want)-1}' or ls.last_mode is not True:
  print('FAIL',name,'out',repr(out),'want',repr(want),'transcript',a,'mode',ls.last_mode,flush=True);sys.exit(1)
 # Explicit intermediate screens prove the ghost is visible before never-enter.
 if name=='sh29_never_typed':
  assert any('prefix_suffix' in row for row in screens[3]),screens[3]
  assert 'cursor 0 13' in screens[3],screens[3]
 Path(keys[:-5]+'.tr').write_text('\n'.join(a)+'\n')
 ls.write_screen(keys[:-5]+'.screen',screens,'1')
 print('PIN',name,flush=True)
