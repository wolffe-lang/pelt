sleep 1 &
fg; echo "fg=$?"
bg; echo "bg=$?"
jobs -x 2>&1 >/dev/null; echo "jobsx=$?"
wait
