"""Independent output expectations; pin deterministic pelt-owned UI separately."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[2]
S=ROOT/'tests/session'
sys.path.insert(0,str(ROOT/'tools'))
import lib_session as ls
cases={}
def add(name,steps,outputs,extra='',files=None):
 assert len(steps)==len(outputs)
 cases['sh29_'+name]=(['exec 2>&0']+steps+['exit'],['']+outputs+[''],extra,files)
def standard(name,tail,want='prefix\n',extra=''):
 add(name,['echo prefix_suffix',r'\k echo prefix',tail],['prefix_suffix\n','',want],extra)
for name,key in [('right',r'\e[C'),('ss3right',r'\eOC'),('end',r'\e[F'),('ss3end',r'\eOF'),('end4',r'\e[4~'),('end8',r'\e[8~'),('ce',r'\x05'),('cf',r'\x06')]:
 standard('accept_'+name,r'\k '+key+r'\r','prefix_suffix\n')
standard('never_typed',r'\k \r')
standard('undo_accept',r'\k \e[C\x1f\r')
standard('undo_shadow',r'\k \x1f'+'echo clean'+r'\r','clean\n')
standard('kill_ring',r'\k \x15\x19\r')
standard('clear_cu',r'\k \x15echo clean\r','clean\n')
standard('clear_cc',r'\k \x03echo clean\r','clean\n')
standard('clear_quit',r'\k \x1cecho clean\r','clean\n')
standard('clear_cl',r'\k \x0c\r')
standard('midline_right',r'\k \x02\x06\r')
standard('midline_end',r'\k \x01\x05\r')
standard('delete',r'\k \x7f\r','prefi\n')
standard('edit',r'\k Z\r','prefixZ\n')
standard('tab',r'\k \t\r')
add('toggle_off',['echo prefix_suffix',r'\k echo prefix',r'\k \x15set +o suggest\r',r'\k echo prefix',r'\k \e[C\r'],['prefix_suffix\n','','','','prefix\n'])
add('friendly_off',['echo prefix_suffix',r'\k echo prefix',r'\k \x15set +o friendly\r',r'\k echo prefix',r'\k \e[C\r'],['prefix_suffix\n','','','','prefix\n'])
standard('feature_off',r'\k \e[C\r','prefix\n','args=-o friendly +o suggest -o histsearch')
standard('umbrella_off',r'\k \e[C\r','prefix\n','args=+o friendly -o suggest -o histsearch')
standard('posix_off',r'\k \e[C\r','prefix\n','args=--posix -o friendly -o suggest -o histsearch')
standard('keys_off',r'\k \e[C\r','prefix_suffix\n','args=-o friendly +o friendly_keys -o suggest -o histsearch')
standard('color_linux',r'\k \r','prefix\n','env=PS1=$\\s TERM=linux')
standard('color_rgb',r'\k \r','prefix\n','env=PS1=$\\s TERM=xterm-256color COLORTERM=truecolor')
standard('edge',r'\k \e[C\r','prefix_suffix\n','cols=16')
add('empty',['echo previous',r'\k \e[Cecho clean\r'],['previous\n','clean\n'])
for name,key,want in [('alt_word',r'\ef','alpha\n'),('ctrl_token',r'\e[1;5C','alpha-beta/gamma\n')]:
 add(name,['echo alpha-beta/gamma delta',r'\k echo al',r'\k '+key+r'\r'],['alpha-beta/gamma delta\n','',want])
add('recent',['echo prefix_old','echo prefix_new',r'\k echo prefix_',r'\k \e[C\r'],['prefix_old\n','prefix_new\n','','prefix_new\n'])
add('no_word_fallback',['echo alpha beta_suffix',r'\k echo beta',r'\k \e[C\r'],['alpha beta_suffix\n','','beta\n'])
add('unicode',['echo 界界界',r'\k echo 界',r'\k \e[C\r'],['界界界\n','','界界界\n'],'cols=12')
add('combining',['echo ábc',r'\k echo a',r'\k \e[C\r'],['ábc\n','','ábc\n'])
add('file_one',[r'\k echo ./uni',r'\k \e[C\r'],['','./unique-file\n'],files={'w/unique-file':''})
add('file_many',[r'\k echo ./sha',r'\k \e[C\r'],['','./shared-one\n'],files={'w/shared-one':'','w/shared-two':''})
add('file_quote',[r'\k echo ./uni',r'\k \e[C\r'],['','./unique file\n'],files={'w/unique file':''})
add('file_dir',[r'\k echo ./uni',r'\k \e[C\r'],['','./unique-dir/\n'],files={'w/unique-dir/child':''})
add('command',[r'\k pri',r'\k \e[C ok\\n\r'],['','okn'],'env=PS1=$\\s PATH=/nonexistent')
for name,key,want in [('up',r'\e[A','alpha2\n'),('cp',r'\x10','alpha2\n'),('twice',r'\e[A\e[A','alpha1\n'),('down',r'\e[A\e[A\e[B','alpha2\n'),('restore',r'\e[A\e[B','al\n'),('plain',r'\x15\e[A','alpha2\n'),('pageup',r'\e[5~',''),('pagedown',r'\e[A\e[6~','al\n')]:
 add('history_'+name,['echo alpha1','echo beta','echo alpha2',r'\k echo al',r'\k '+key+r'\r'],['alpha1\n','beta\n','alpha2\n','',want])
for name,keys,want in [('enter',r'\r','alpha2\n'),('down',r'\e[B\r','alpha1\n'),('cycle',r'\x12\r','alpha1\n'),('escape',r'\e','al\n'),('cc',r'\x03','al\n'),('cg',r'\x07','al\n')]:
 add('pager_'+name,['echo alpha1','echo beta','echo alpha2',r'\k echo al',r'\k \x12',r'\k '+keys,r'\k \r'],['alpha1\n','beta\n','alpha2\n','','','',want])
add('pager_filter',['echo alpha','echo beta',r'\k \x12',r'\k alpha',r'\k \r',r'\k \r'],['alpha\n','beta\n','','','','alpha\n'])
add('pager_nomatch',['echo alpha',r'\k echo draft',r'\k \x12zzzz',r'\k \r',r'\k \r'],['alpha\n','','','','draft\n'])
add('pager_undo',['echo alpha',r'\k echo al',r'\k \x12\r',r'\k \x1f\r'],['alpha\n','','','al\n'])
add('bang',[r'\k !!',r'\k \e[C\x15echo clean\r'],['','clean\n'])
add('bang_history',['! true',r'\k !',r'\k \e[C\r','true'],['','','',''])
add('history_off',['echo alpha','echo beta',r'\k echo al',r'\k \e[A\r'],['alpha\n','beta\n','','beta\n'],'args=-o friendly -o suggest +o histsearch')
add('isearch_off',['echo alpha',r'\k \x12alpha\r'],['alpha\n','alpha\n'],'args=-o friendly +o histsearch')
for name,(steps,outputs,extra,files) in cases.items():
 (S/(name+'.keys')).write_text('\n'.join(steps)+'\n')
 meta=dict(args='-o friendly -o suggest -o histsearch',env=r'PS1=$\s TERM=xterm-256color',tr_by='hand',screen='1',screen_by='hand',why='sh29 fish black-box behavior; independently specified stdout; pelt-owned display bytes, never inferred buffer contents')
 for row in extra.splitlines():
  if row: k,v=row.split('=',1);meta[k]=v
 ls.write_meta(str(S/(name+'.meta')),meta)
 if files:
  for rel,content in files.items():
   p=S/(name+'.files')/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content)
(ROOT/'notes/sh29/expected.json').write_text(json.dumps({name:data[1] for name,data in cases.items()},ensure_ascii=False,indent=2)+'\n')
print(len(cases),'cases')
