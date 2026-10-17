alias a='echo ' b='B ' c='C'
a b c
alias e='echo ' w='WORD'
e 'w' w
e >/dev/stdout w
alias t='echo	'
t w
alias en='env '
en X=1 w 2>/dev/null | grep -c WORD || true
