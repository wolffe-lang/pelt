trap 'echo exit-trap' EXIT
/bin/sh -c 'kill -TERM $PPID'
echo not-reached
