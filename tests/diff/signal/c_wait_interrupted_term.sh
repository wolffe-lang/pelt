trap 'echo trapped' TERM
sleep 3 &
( sleep 1; kill -TERM $$ ) &
wait $!; s=$?
[ $s -gt 128 ] && echo "wait-above-128"
kill $! 2>/dev/null
