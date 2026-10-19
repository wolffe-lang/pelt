(exit 5) & p=$!
(exit 6) & (exit 7) &
sleep 0.3
wait $p; echo "kept=$?"
