(exit 3) & p=$!; wait $p; echo $?; wait $p; echo $?
env sh -c "exit 5" & q=$!; wait $q; echo $?; wait $q; echo $?
