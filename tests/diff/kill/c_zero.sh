sleep 2 & p=$!
kill -0 $p; echo "alive=$?"
kill $p; wait $p 2>/dev/null
kill -0 $p 2>/dev/null; echo "dead=$?"
