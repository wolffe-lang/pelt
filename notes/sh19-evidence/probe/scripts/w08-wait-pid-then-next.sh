(exit 3) & p=$!
wait $p; echo "first=$?"
(exit 4) &
wait $p; echo "after-next=$?"
