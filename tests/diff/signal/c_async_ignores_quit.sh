sh -c 'kill -QUIT $$; echo survived-quit; kill -INT $$; echo survived-int' &
wait; echo "st=$?"
