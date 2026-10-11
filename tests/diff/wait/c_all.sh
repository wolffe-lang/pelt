(sleep 1; : > a) & (sleep 1; : > b) & (exit 3) &
wait; echo "st=$?"; ls
