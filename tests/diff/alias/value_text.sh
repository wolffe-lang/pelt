alias nl='echo one
echo two'
nl three
alias s='echo s;'
s echo t
alias p='echo piped |'
p tr a-z A-Z
alias c='echo a # hidden'
c b
alias k='cat'
k <<E
doc
E
alias v='echo $X'
X=late; v
alias loop='for i in 1 2; do'
loop echo $i; done
