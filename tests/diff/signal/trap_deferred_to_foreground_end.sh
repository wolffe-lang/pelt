trap 'echo t' TERM
/bin/sh -c 'sleep 0.3; kill -TERM $PPID' &
sleep 1
echo after
