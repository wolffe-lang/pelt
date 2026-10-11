sleep 0 & a=$!
sleep 0 & b=$!
[ "$a" != "$b" ] && echo differ
kill -0 $b 2>/dev/null; wait; echo done
