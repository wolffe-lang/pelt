"""Numeric command/undo boundary audit, independently against readline."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
import lib_session as ls
S=ROOT/'notes/sh28-evidence/probes'
for name,key in {
 'zero_case_undo': r'\k echo abc\e0\eu\x1f\r',
 'numeric_insert_undo':r'\k echo \e3x\x1f\r',
 'numeric_transpose_chars_end':r'\k echo abc\e2\x14\r',
 'numeric_transpose_words_end':r'\k echo one two three\e2\et\r',
 'numeric_delete_yank':r'\k echo abcde\e3\x7f \x19\r',
}.items():
    keys=S/(name+'.keys');keys.write_text('exec 2>&0\n'+key+'\nexit\n')
    meta={'env':r'PS1=$\s','compare':'stdout'}
    a=ls.run(ls.SECOND,str(keys),meta)
    b=ls.run(ls.SECOND,str(keys),meta)
    assert ls.stdout_and_exit(a)==ls.stdout_and_exit(b),(name,'unstable')
    got=ls.run([str(ROOT/'target/native/pelt'),'-i','+m','-o','friendly'],str(keys),meta)
    (S/(name+'-bash.tr')).write_text('\n'.join(a)+'\n')
    (S/(name+'-pelt-before.tr')).write_text('\n'.join(got)+'\n')
    print(name,'MATCH' if ls.stdout_and_exit(a)==ls.stdout_and_exit(got) else 'DIFF',flush=True)
    print('bash',ls.stdout_and_exit(a),flush=True)
    print('pelt',ls.stdout_and_exit(got),flush=True)
