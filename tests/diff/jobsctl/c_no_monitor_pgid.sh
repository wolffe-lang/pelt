sh -c 'ps -o pgid= -p $$ | tr -d " "' > bgpgid &
wait
me=$(ps -o pgid= -p $(sh -c 'echo $PPID') | tr -d ' ')
[ "$(cat bgpgid)" = "$me" ] && echo same-group
