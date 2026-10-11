(exit 3) & a=$!; (exit 4) & b=$!
wait $a; echo $?; wait $b; echo $?
(exit 5) & a=$!; (exit 6) & b=$!; wait $a $b; echo $?
