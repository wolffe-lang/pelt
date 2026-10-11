trap 'echo t' TERM
trap - TERM
/bin/sh -c 'kill -TERM $PPID'
echo not-reached
