/bin/sh -c 'kill -INT $$; echo survived' &
wait $!
echo $?
