(exit 5) & p=$!
i=0
while [ $i -lt 3000 ]; do true & i=$((i+1)); done
wait $p; echo "first-of-3001=$?"
env sh -c 'exit 6' & q=$!
i=0
while [ $i -lt 300 ]; do env true & i=$((i+1)); done
wait $q; echo "prog-first-of-301=$?"
