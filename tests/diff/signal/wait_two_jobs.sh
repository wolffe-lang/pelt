/bin/sh -c 'exit 3' &
a=$!
/bin/sh -c 'exit 4' &
b=$!
wait $b
echo $?
wait $a
echo $?
