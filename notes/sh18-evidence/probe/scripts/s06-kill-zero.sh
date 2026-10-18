trap 'echo got-term' TERM
sleep 5 &
kill 0
echo after st=$?
wait
echo waited=$?
