"""Typed inputs and independent visible-text expectations, not fish goldens."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[2];S=ROOT/'tests/session'
sys.path.insert(0,str(ROOT/'tools'))
import lib_session as ls
cases={}
def add(name,steps,visible,extra='',files=None):
 cases['sh30_'+name]=(['exec 1>&0 2>&0']+steps+[r'\k \x07\x05\x15','exit 0'],visible,extra,files)
for name,text in [('command','echo'),('unknown','zz_sh30_absent'),('argument','echo argument'),('reserved','if true; then echo x; fi'),('quote',"echo 'hello'"),('double_quote','echo "hello $HOME"'),('variable','echo $HOME'),('braced','echo ${HOME}'),('arithmetic','echo $((2+3))'),('substitution','echo $(echo not-run > side-effect)'),('redirection','echo > output'),('comment','echo word # comment'),('operator','echo | cat'),('bang','!!'),('bang_last','!$'),('unicode','echo 界界'),('combining','echo ábc')]:
 add(name,[r'\k '+text],text)
for name,text in [('open_single',"echo 'hello"),('open_double','echo "hello'),('open_if','if true; then echo x'),('open_subshell','(echo x'),('open_pipeline','echo |'),('open_parameter','echo ${HOME'),('open_substitution','echo $(true'),('open_arithmetic','echo $((1+')]:
 add(name,[r'\k '+text],text)
for name,extra in [('linux','env=PS1=$\\s TERM=linux'),('rgb','env=PS1=$\\s TERM=xterm-256color COLORTERM=truecolor PELT_COLORS=argument=#123456'),('indexed','env=PS1=$\\s TERM=xterm-256color PELT_COLORS=argument=idx244'),('malformed','env=PS1=$\\s TERM=xterm-256color PELT_COLORS=command=green:argument=idx999')]:
 add(name,[r'\k echo colour'], 'echo colour',extra)
add('error',[r'\k echo )',r'\k \r'],'^')
add('error_unicode',[r'\k echo 界 )',r'\k \r'],'^')
add('resize',[r'\k echo '+('x'*40),r'\size 16 24',r'\size 80 24'],'echo '+('x'*40))
add('resize_midline',[r'\k echo '+('x'*40)+r'\x01\x06\x06',r'\size 16 24',r'\size 80 24'],'echo '+('x'*40))
add('shadow',['set -o suggest -o friendly','echo prefix_suffix',r'\k echo prefix'],'echo prefix_suffix')
add('shadow_enter',['set -o suggest -o friendly','echo prefix_suffix',r'\k echo prefix',r'\k \r'],'prefix')
add('undo',['set -o friendly',r'\k echo kept',r'\k \x15\x1f'],'echo kept')
add('kill_yank',['set -o friendly',r'\k echo kept',r'\k \x15\x19'],'echo kept')
add('pager',['set -o friendly -o histsearch','echo alpha','echo beta',r'\k echo al',r'\k \x12'],'history: echo al')
add('pager_restore',['set -o friendly -o histsearch','echo alpha',r'\k echo al',r'\k \x12',r'\k \x07'],'echo al')
add('completion',[r'\k echo ./shared',r'\k \t\t'],'shared-one',files={'w/shared-one':'','w/shared-two':''})
add('highlight_off',['set +o highlight',r'\k echo plain'],'echo plain')
add('umbrella_off',['set -o friendly','set +o friendly',r'\k echo plain'],'echo plain')
add('independent',[r'\k echo independent'],'echo independent','args=+o friendly -o highlight')
add('posix',[r'\k echo plain'],'echo plain','args=--posix -o highlight')
# Dumb is cooked: no editing control bytes as standalone draft cleanup.
cases['sh30_dumb']=(['exec 1>&0 2>&0','echo plain','exit 0'],'plain','env=PS1=$\\s TERM=dumb',None)
for name,(steps,visible,extra,files) in cases.items():
 (S/(name+'.keys')).write_text('\n'.join(steps)+'\n')
 meta=dict(args='-o highlight',env=r'PS1=$\s TERM=xterm-256color',tr_by='hand',screen='1',screen_by='hand',why='sh30 independent typed text and no-execution expectations; pelt-owned screen; raw SGR checked by colour-witness')
 for row in extra.splitlines():
  if row:k,v=row.split('=',1);meta[k]=v
 ls.write_meta(str(S/(name+'.meta')),meta)
 if files:
  for rel,content in files.items():
   p=S/(name+'.files')/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content)
(ROOT/'notes/sh30/expected.json').write_text(json.dumps({name:dict(steps=len(data[0]),visible=data[1]) for name,data in cases.items()},ensure_ascii=False,indent=2)+'\n')
print(len(cases),'cases')
