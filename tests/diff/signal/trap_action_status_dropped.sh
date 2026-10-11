trap 'false' TERM
true
/bin/sh -c 'kill -TERM $PPID'
echo $?
