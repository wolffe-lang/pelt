trap 'echo one' TERM
trap 'echo two' TERM
/bin/sh -c 'kill -TERM $PPID'
echo after
