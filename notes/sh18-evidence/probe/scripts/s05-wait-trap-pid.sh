trap 'echo t' USR1
sleep 2 & p=$!
/bin/sh -c 'sleep 0.3; kill -USR1 $PPID' &
wait $p
echo st=$?
kill $p
