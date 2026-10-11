trap 'echo t' TERM
/bin/sh -c 'kill -TERM $PPID'
/bin/sh -c 'kill -TERM $PPID'
echo after
