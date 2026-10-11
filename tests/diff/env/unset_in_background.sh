export A=1
unset A
/bin/sh -c 'echo "[$A]"' &
wait
