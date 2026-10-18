trap 'echo t' TERM
sleep 2 &
/bin/sh -c 'sleep 0.3; kill -TERM $PPID' &
wait
echo st=$?
wait
echo st2=$?
