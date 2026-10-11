for how in '' '-s HUP' '-HUP' '-9' '-s KILL' '-TERM' '-15' '-s 15'; do
  sleep 5 & p=$!; kill $how $p; wait $p; echo "[$how] $?"
done
