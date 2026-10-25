"""Raw terminal echo and screen after quit, measured independently once more."""
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
import lib_session as ls
keys=ROOT/'notes/sh28-evidence/probes/quit.keys'
feed=ls.Screen.feed
for cmd,name in [(ls.ORACLE,'dash'),(ls.SECOND,'bash')]:
    raw=[]
    def tap(self,data):
        raw.append(data.hex())
        return feed(self,data)
    ls.Screen.feed=tap
    tr=ls.run(cmd,str(keys),{'env':r'PS1=$\s'})
    ls.Screen.feed=feed
    path=ROOT/'notes/sh28-evidence/probes'/('quit-raw-'+name+'.json')
    path.write_text(json.dumps({'chunks_hex':raw,'transcript':tr,'screens':ls.last_screens},indent=2)+'\n')
    print(name,'raw',repr(bytes.fromhex(''.join(raw))),flush=True)
    print(name,'screens',ls.last_screens,flush=True)
