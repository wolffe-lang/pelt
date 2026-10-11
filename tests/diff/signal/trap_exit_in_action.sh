trap 'echo bye; exit 3' TERM
/bin/sh -c 'kill -TERM $PPID'
echo not-reached
