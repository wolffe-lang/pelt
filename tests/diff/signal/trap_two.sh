trap 'echo t' TERM
trap 'echo h' HUP
/bin/sh -c 'kill -HUP $PPID; kill -TERM $PPID'
echo after
