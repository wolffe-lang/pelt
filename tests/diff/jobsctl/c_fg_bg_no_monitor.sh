sleep 1 &
fg 2>/dev/null; echo "fg=$?" | sed 's/fg=[1-9][0-9]*/fg=fails/'
bg 2>/dev/null; echo "bg=$?" | sed 's/bg=[1-9][0-9]*/bg=fails/'
wait
