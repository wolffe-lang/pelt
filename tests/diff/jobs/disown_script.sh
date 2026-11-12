sleep 1 & disown
wait; echo "wait=$?"
disown; echo "none=$?"
disown %4; echo "bad=$?"
disown -x; echo "opt=$?"
