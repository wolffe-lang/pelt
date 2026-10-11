wait 1; echo $?
(exit 3) & p=$!; wait $p; wait $p; echo "second=$?"
