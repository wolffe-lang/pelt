for i in 1 2; do (exit $i); done; echo $?
for i in 1; do true; done; echo $?
