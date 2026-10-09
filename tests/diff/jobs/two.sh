sleep 0 &
a=$!
/bin/sh -c 'exit 5' &
b=$!
wait $a
echo $?
wait $b
echo $?
