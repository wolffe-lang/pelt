(exit 4) & p=$!
wait; echo "all=$?"
wait $p; echo "after-all=$?"
