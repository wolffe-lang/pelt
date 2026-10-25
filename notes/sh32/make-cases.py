"""Independent typed outputs; all old expectations remain immutable."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
import lib_session as ls
S=ROOT/'tests/session';cases={}
def add(name,steps,out='',extra=None,visible=None):
    cases['sh32_'+name]=dict(steps=['cd "$HOME"; exec 3>&1 1>&0 2>&0','cd "$HOME"']+steps+[r'\k \x07\x05\x15','exit 0'],out=out,extra=extra or {},visible=visible)
for cols in (24,39,40,80,200):
    opts={'cols':str(cols)}
    add('home_'+str(cols),['echo HOME >&3'],'HOME\n',opts,'tester@box ~')
    add('right_'+str(cols),['prompt_right() { printf RIGHT; }',r'\k echo kept',r'\k \r','echo DONE >&3'],'DONE\n',opts)
    add('wrap_'+str(cols),['prompt_right() { printf RIGHT; }',r'\k echo '+('x'*(cols+10)),r'\k \x03','echo CANCELED >&3'],'CANCELED\n',opts)
add('status',['false','echo $? >&3'],'1\n',visible='[1]')
add('unicode',["mkdir -p alpha/beta/日本語",'cd alpha/beta/日本語','echo PATH >&3'],'PATH\n',visible='~/a/b/日本語')
add('custom_PS1',["PS1='CUSTOM '",'echo CUSTOM >&3'],'CUSTOM\n',visible='CUSTOM ')
add('empty_PS1',["PS1=''",'echo EMPTY >&3'],'EMPTY\n')
add('default_PS1',["PS1='$ '",'echo DEFAULT >&3'],'DEFAULT\n')
add('unset_PS1',["PS1='CUSTOM '",'unset PS1','echo UNSET >&3'],'UNSET\n')
add('right_resize',['prompt_right() { printf RIGHT; }',r'\k echo resize',r'\k \x01',r'\size 39 24',r'\size 80 24',r'\k \x05\r','echo RESIZED >&3'],'RESIZED\n')
add('right_undo',['prompt_right() { printf RIGHT; }',r'\k echo undo',r'\k \x1f',r'\k echo UNDO >&3\r'],'UNDO\n')
add('right_kill',['prompt_right() { printf RIGHT; }',r'\k echo KILL',r'\k \x17',r'\k \x19',r'\k  >&3\r'],'KILL\n')
add('right_control',[r"prompt_right() { printf '\033[31mBAD\nLINE'; }",r'\k echo safe',r'\k \r'],'',visible='^[[31mBAD^JLINE')
add('right_long',["prompt_right() { printf abcdefghijklmnopqrstuvwxyz0123456789; }",r'\k echo trimmed',r'\k \r'],'',{'cols':'40'},'abcdefghijkl…')
add('right_vi',['prompt_right() { printf RIGHT; }','set -o vi',r'\k echo VI >&3\r'],'VI\n')
add('prompt_off',['set +o prompt_friendly','echo OFF >&3'],'OFF\n')
add('umbrella_off',['set +o friendly','echo OFF >&3'],'OFF\n')
add('colour_off',['set +o highlight','prompt_right() { printf PLAIN; }',r'\k echo PLAIN >&3\r'],'PLAIN\n')
add('right_status',['prompt_right() { false; }','false','echo $? >&3'],'1\n')
add('right_isolation',['v=OLD','prompt_right() { v=NEW; cd /; printf RIGHT; }','echo "$v" >&3'],'OLD\n')
for name,spec in cases.items():
    (S/(name+'.keys')).write_text('\n'.join(spec['steps'])+'\n')
    meta=dict(args='-o friendly',env='USER=tester HOSTNAME=box TERM=xterm-256color',tr_by='hand',screen='1',screen_by='hand',why='sh32 independent stdout assertions; pelt-owned prompt screens; prompt-witness raw laws')
    meta.update(spec['extra']);ls.write_meta(str(S/(name+'.meta')),meta)
(ROOT/'notes/sh32/expected.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n')
print(len(cases),'cases')
