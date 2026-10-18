set -m
sleep 2 & p=$!
echo "--jobs"; jobs
echo "--pipe"; jobs | cat
echo "--l"; jobs -l | sed "s/$p/PID/"
kill %1
sleep 0.3
echo "--after kill"; jobs
echo end
