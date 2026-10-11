trap 'echo caught' TERM
/bin/sh -c 'kill -TERM $PPID'
echo after=$?
