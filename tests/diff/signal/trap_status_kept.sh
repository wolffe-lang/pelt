trap 'echo in=$?' TERM
/bin/sh -c 'kill -TERM $PPID; exit 7'
echo after=$?
