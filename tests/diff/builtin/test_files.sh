touch f
mkdir d
test -f f; echo $?
test -d d; echo $?
test -e f; echo $?
test -e nope; echo $?
test -f d; echo $?
test -s f; echo $?
