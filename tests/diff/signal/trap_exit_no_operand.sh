trap 'exit' TERM
/bin/sh -c 'kill -TERM $PPID; exit 6'
echo not-reached
