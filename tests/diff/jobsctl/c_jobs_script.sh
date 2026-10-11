sleep 2 & p=$!
jobs | grep -c sleep
[ "$(jobs -p)" = "$p" ] && echo pid-matches
kill $p; wait
jobs | wc -l | tr -d ' '
