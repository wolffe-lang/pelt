set -m
sh -c 'kill -STOP $$' & p=$!
sleep 0.3
jobs
kill -CONT $p
wait $p; echo st=$?
