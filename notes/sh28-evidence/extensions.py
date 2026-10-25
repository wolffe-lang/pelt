"""Own extension cases: independent expectations, two recordings and mode checks."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
import lib_session as ls
CASES={
 'bindings_basic':(['bindings'],lambda out:b'yank-last-arg\n' in out and b'stty quit\t1c\tterminal-character\n' in out),
 'bindings_actions':(['bindings -l'],lambda out:b'upcase-word\n' in out and b'character-search-backward\n' in out and b'yank-last-arg\n' in out),
 'bindings_featureoff':(['set +o friendly_keys','bindings -l'],lambda out:b'yank-pop\n' not in out and b'accept-line\n' in out),
 'bindings_disabled':(['set +o emacs','bindings'],lambda out:out==b'mode\t-\tdisabled\n'),
 'bindings_readonly':(['bindings add','echo $?'],lambda out:out==b'2\n'),
 'kill_ring_cap':([r'\k '+''.join('k'+str(i)+r'\x15\x01' for i in range(12))+r'echo \x19'+r'\ey'*10+r'\r'],lambda out:out==b'k11\n'),
}
for name,(commands,check) in CASES.items():
    base=ROOT/'tests/session'/('sh28_'+name)
    keys=base.with_suffix('.keys')
    keys.write_text('\n'.join(['exec 2>&0']+commands+['exit'])+'\n')
    meta={'env':r'PS1=$\s','pelt_args':'-i -o friendly','compare':'stdout','tr_by':'hand','screen':'2','screen_by':'hand',
        'why':'pelt-owned read-only bindings / bounded 10-entry kill-ring extension; independent assertions in notes/sh28-evidence/extensions.py and witness.py; key inputs bash 5.3.20-2, dash 0.5.13.4-1.1, fish 4.9.3-1; Arch image id 3ed18d5c7b242c675807f875e43eabf11bdf87f9eebd875fce9e9b1d1bf7297f digest sha256:8185e444e45ba166146b244b41f1cba2d7d91f3eddce533a839cc9591e0fa785'}
    pelt=str(ROOT/'target/native/pelt')
    a=ls.run(ls.argv_for(pelt,meta,True),str(keys),meta)
    screen=ls.last_screens
    mode=ls.last_mode
    b=ls.run(ls.argv_for(pelt,meta,True),str(keys),meta)
    assert a==b and screen==ls.last_screens and mode is True and ls.last_mode is True,name
    import json
    out=b''.join(json.loads(line[4:]).encode() for line in a if line.startswith('out '))
    assert check(out),(name,out)
    assert a[-1].startswith('exit 0 '),(name,a)
    ls.write_meta(str(base)+'.meta',meta)
    base.with_suffix('.tr').write_text('\n'.join(a)+'\n')
    ls.write_screen(str(base)+'.screen',screen,'2')
    print('ok extension',name,flush=True)
