(alias q='echo Q'); q 2>/dev/null; echo "subshell=$?"
x=$(alias q='echo Q'); q 2>/dev/null; echo "cmdsub=$?"
alias r='echo R'
(unalias r); r
alias hi='echo hello'
command hi 2>/dev/null; echo "command=$?"
../sh -c 'hi' 2>/dev/null; echo "child=$?"
