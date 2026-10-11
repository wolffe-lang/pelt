i=0; while [ $i -lt 3 ]; do i=$((i+1)); done; echo "$i $?"
while false; do :; done; echo $?
i=0; while [ $i -lt 2 ]; do i=$((i+1)); (exit $i); done; echo $?
