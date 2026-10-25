from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
import lib_session as ls
S=ROOT/'notes/sh28-evidence/probes'
for name,key in {
 'words_end_2':r'\k echo A B C D\e2\et\r',
 'words_mid_2':r'\k echo A B C D\x01\ef\ef\e2\et\r',
 'words_mid_negative':r'\k echo A B C D\x01\ef\ef\e-\et!\r',
 'words_mid_negative2':r'\k echo A B C D\x01\ef\ef\ef\e-2\et!\r',
 'words_end_too_far':r'\k echo A B C D\e9\et\r',
 'words_mid_too_far':r'\k echo A B C D\x01\ef\ef\e9\et\r',
 'chars_end_too_far':r'\k echo abcd\e9\x14\r',
 'chars_mid_2':r'\k echo abcd\x02\x02\e2\x14\r',
}.items():
    keys=S/(name+'.keys');keys.write_text('exec 2>&0\n'+key+'\nexit\n')
    meta={'env':r'PS1=$\s','compare':'stdout'}
    a=ls.run(ls.SECOND,str(keys),meta); b=ls.run(ls.SECOND,str(keys),meta)
    assert ls.stdout_and_exit(a)==ls.stdout_and_exit(b)
    (S/(name+'-bash.tr')).write_text('\n'.join(a)+'\n')
    print(name,ls.stdout_and_exit(a),flush=True)
