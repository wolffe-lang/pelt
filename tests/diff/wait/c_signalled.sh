sleep 5 & p=$!; kill -TERM $p; wait $p; echo $?
sleep 5 & p=$!; kill -KILL $p; wait $p; echo $?
