echo '(exit 3)' > a; : > b; echo '# only a comment' > c
. ./a; echo $?
false; . ./b; echo $?
false; . ./c; echo $?
