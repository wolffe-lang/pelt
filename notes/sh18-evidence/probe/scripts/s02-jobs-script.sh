sleep 2 & p=$!
echo "--jobs"; jobs
echo "--pipe"; jobs | cat
echo "--sub"; (jobs)
echo "--cmdsub"; x=$(jobs); echo "[$x]"
echo "--l"; jobs -l | sed "s/$p/PID/"
echo "--p"; [ "$(jobs -p)" = "$p" ] && echo pid
echo "--pct"; jobs %1; jobs %sl; jobs %?2
kill $p; wait
echo "--after"; jobs
echo end
