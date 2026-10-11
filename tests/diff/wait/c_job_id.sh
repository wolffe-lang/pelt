(exit 3) &
wait %1; echo "st=$?"
(exit 4) & wait %%; echo "st=$?"
wait %9 2>/dev/null; echo "missing=$?"
