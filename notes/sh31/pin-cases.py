"""Assert independently chosen outputs before pinning owned byte/screen rows."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
import lib_session as ls
expected=json.loads((ROOT/'notes/sh31/expected.json').read_text())
bad=0
for name in sys.argv[1:] or expected:
    spec=expected[name]; keys=str(ROOT/'tests/session'/(name+'.keys'));meta=ls.read_meta(keys[:-5]+'.meta')
    got=ls.run(ls.argv_for(str(ROOT/'target/native/pelt'),meta,True),keys,meta)
    out=''.join(json.loads(row[4:]) for row in got if row.startswith('out '))
    try:
        assert out==spec['out'],(name,'stdout',out,spec['out'])
        assert got[-1]==f'exit 0 at step {len(spec["steps"])}',(name,got)
        assert ls.last_mode is True,(name,'terminal mode')
        if spec.get('visible'):
            assert spec['visible'] in '\n'.join('\n'.join(rows) for rows in ls.last_screens),(name,'visible',ls.last_screens)
    except AssertionError as err:
        print('FAIL',err,flush=True);bad+=1;continue
    Path(keys[:-5]+'.tr').write_text('\n'.join(got)+'\n')
    ls.write_screen(keys[:-5]+'.screen',ls.last_screens,'1')
    print('PIN',name,flush=True)
print('PIN FAILURES',bad,flush=True)
sys.exit(bool(bad))
