false; : ; echo $?
: ${x:=set-by-colon} $(echo side >&2) 2>&1; echo $x
: -- -x --help; echo $?
