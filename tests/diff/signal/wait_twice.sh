sleep 5 &
kill -KILL $!
wait $!
echo $?
wait $!
echo $?
