(f() { exit 2; }; f; echo no); echo $?
(for i in 1; do exit 3; done; echo no); echo $?
(eval 'exit 4'; echo no); echo $?
(echo 'exit 5' > x; . ./x; echo no); echo $?
