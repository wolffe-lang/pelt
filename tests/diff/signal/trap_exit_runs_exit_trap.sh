trap 'echo exit-trap' EXIT
trap 'exit 5' TERM
/bin/sh -c 'kill -TERM $PPID'
echo not-reached
