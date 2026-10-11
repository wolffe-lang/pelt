sleep 5 & a=$!; sleep 5 & b=$!
kill $a $b; wait $a; echo $?; wait $b; echo $?
sleep 5 & c=$!; kill -s TERM -- $c; wait $c; echo $?
