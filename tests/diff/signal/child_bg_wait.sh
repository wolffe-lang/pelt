/bin/sh -c 'kill -TERM $$' &
wait $!
echo $?
