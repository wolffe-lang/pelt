/bin/sh -c 'exit 4' &
wait $!
echo $?
