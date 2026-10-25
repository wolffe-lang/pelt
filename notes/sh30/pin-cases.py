"""Pin owned screens only after independent output/text/mode assertions."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
import lib_session as ls
expected=json.loads((ROOT/'notes/sh30/expected.json').read_text())
for name in sys.argv[1:] or expected:
 spec=expected[name]; keys=str(ROOT/'tests/session'/(name+'.keys'));meta=ls.read_meta(keys[:-5]+'.meta')
 got=ls.run(ls.argv_for(str(ROOT/'target/native/pelt'),meta,True),keys,meta)
 assert not any(row.startswith('out ') for row in got),(name,got)
 assert got[-1]==f'exit 0 at step {spec["steps"]}',(name,got)
 assert ls.last_mode is True,(name,'terminal mode')
 visible='\n'.join('\n'.join(rows) for rows in ls.last_screens)
 assert spec['visible'] in visible,(name,spec,visible)
 if name=='sh30_substitution':assert 'not-run\n' not in visible
 Path(keys[:-5]+'.tr').write_text('\n'.join(got)+'\n')
 ls.write_screen(keys[:-5]+'.screen',ls.last_screens,'1')
 print('PIN',name,flush=True)
