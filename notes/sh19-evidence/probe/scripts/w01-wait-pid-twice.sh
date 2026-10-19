(exit 3) & p=$!
wait $p; echo "first=$?"
wait $p; echo "second=$?"
env true & q=$!
wait $q; echo "prog-first=$?"
wait $q; echo "prog-second=$?"
