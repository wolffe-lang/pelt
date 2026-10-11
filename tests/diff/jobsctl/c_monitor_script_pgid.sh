set -m 2>/dev/null
sh -c 'ps -o pgid= -p $$ | tr -d " "' > bgpgid &
wait
me=$(ps -o pgid= -p $$ | tr -d ' ')
[ "$(cat bgpgid)" != "$me" ] && echo own-group
