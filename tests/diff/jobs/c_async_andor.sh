true && { sleep 0; echo bg; } & wait
false || echo alt & wait
false && echo no & wait; echo "st=$?"
