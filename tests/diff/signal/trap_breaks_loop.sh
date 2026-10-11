trap 'echo t; break' TERM
/bin/sh -c 'sleep 0.3; kill -TERM $PPID' &
while :; do :; done
echo out
