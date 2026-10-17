alias 'a b=c' 2>/dev/null; echo "st=$?"
alias 'a/b=c' 2>/dev/null; echo "st=$?"
alias '=c' 2>/dev/null; echo "st=$?"
alias 'a$b=c' 2>/dev/null; echo "st=$?"
alias 'a=b=c'; alias a
alias e=; alias e; e echo still; echo "st=$?"
alias -p 2>/dev/null; echo "p=$?"
alias -- q=1 2>/dev/null; alias q
unalias 2>/dev/null; echo "none=$?"
alias m=1 n=2; unalias m nope n 2>/dev/null; echo "partial=$?"; alias | grep -c -e "^'m=" -e "^'n="
unalias -z q 2>/dev/null; echo "opt=$?"
alias s='a"b'"'"'c$d\e'; alias s
alias nl='a
b'; alias nl
alias zz=1 aa=2 | sort; alias | sort
