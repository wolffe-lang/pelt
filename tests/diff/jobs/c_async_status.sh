false & echo "st=$?"; wait
(exit 3) & wait $!; echo "waited=$?"
