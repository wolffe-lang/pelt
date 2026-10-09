ls ./nosuch_x 2>&1 >f | wc -l | tr -d ' '
wc -c <f | tr -d ' '
