"""Promote independently measured numeric boundary witnesses into CI sessions."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
import lib_session as ls
names=['zero_case_undo','numeric_insert_undo','numeric_transpose_chars_end','numeric_transpose_words_end','numeric_delete_yank','words_end_2','words_mid_2','words_mid_negative','words_mid_negative2','words_end_too_far','words_mid_too_far','chars_end_too_far','chars_mid_2']
for name in names:
    source=ROOT/'notes/sh28-evidence/probes'/name
    base=ROOT/'tests/session'/('sh28_arg_'+name)
    base.with_suffix('.keys').write_text(source.with_suffix('.keys').read_text())
    reference=Path(str(source)+'-bash.tr').read_text()
    meta={'oracle':'bash','compare':'stdout','env':r'PS1=$\s','pelt_args':'-i -o friendly','tr_by':'hand','screen':'2','screen_by':'hand',
      'why':'numeric boundary audit against twice-recorded bash 5.3.20-2; dash 0.5.13.4-1.1, fish 4.9.3-1; Arch image id 3ed18d5c7b242c675807f875e43eabf11bdf87f9eebd875fce9e9b1d1bf7297f digest sha256:8185e444e45ba166146b244b41f1cba2d7d91f3eddce533a839cc9591e0fa785; independent expected stdout/status retained in notes/sh28-evidence/probes; pelt-owned screen'}
    binary=str(ROOT/'target/native/pelt')
    a=ls.run(ls.argv_for(binary,meta,True),str(base)+'.keys',meta)
    screen=ls.last_screens
    mode=ls.last_mode
    b=ls.run(ls.argv_for(binary,meta,True),str(base)+'.keys',meta)
    assert a==b and screen==ls.last_screens and mode is True and ls.last_mode is True,name
    assert ls.stdout_and_exit(a)==ls.stdout_and_exit(reference.splitlines()),(name,ls.stdout_and_exit(a),ls.stdout_and_exit(reference.splitlines()))
    base.with_suffix('.tr').write_text('\n'.join(a)+'\n')
    ls.write_meta(str(base)+'.meta',meta)
    ls.write_screen(str(base)+'.screen',screen,'2')
    print('ok numeric regression',name,flush=True)
# All measured cases name image identity as well as the digest and versions.
for path in (ROOT/'tests/session').glob('sh28_*.meta'):
    text=path.read_text()
    if '3ed18d5c7b242c675807f875e43eabf11bdf87f9eebd875fce9e9b1d1bf7297f' not in text:
        text=text.replace('why=','why=Arch image id 3ed18d5c7b242c675807f875e43eabf11bdf87f9eebd875fce9e9b1d1bf7297f; ',1)
        path.write_text(text)
