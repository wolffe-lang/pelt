(exit 3) & p=$!; wait $p; echo $?; (exit 4) & wait $p; echo $?
env sh -c "exit 5" & q=$!; wait $q; echo $?; env true & wait $q; echo $?
wait; echo $?
