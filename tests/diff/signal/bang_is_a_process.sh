sleep 5 &
p=$!
kill -0 $p && echo live
kill $p
wait $p
echo $?
