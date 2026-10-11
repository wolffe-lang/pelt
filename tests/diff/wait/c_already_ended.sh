(exit 7) & p=$!; (exit 8) & q=$!; sleep 1; wait $q; echo $?; wait $p; echo $?
