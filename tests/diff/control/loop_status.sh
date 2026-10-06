for x in a; do false; done
echo $?
while false; do :; done
echo $?
