test ! x; echo $?
test x -a ''; echo $?
test x -o ''; echo $?
test \( a = a \); echo $?
test ! a = b; echo $?
