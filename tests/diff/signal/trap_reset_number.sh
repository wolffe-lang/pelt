trap 'echo t' TERM
trap 15
/bin/sh -c 'kill -TERM $PPID'
echo not-reached
