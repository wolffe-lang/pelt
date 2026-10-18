set -m
echo "dash-m=$-"
sh -c 'ps -o pgid= -p $$ | tr -d " "' > bg1 &
wait
sh -c 'ps -o pgid= -p $$ | tr -d " "' > fg1
me=$(ps -o pgid= -p $$ | tr -d ' ')
[ "$(cat bg1)" != "$me" ] && echo bg-own-group
[ "$(cat fg1)" != "$me" ] && echo fg-own-group
grep -E 'SigIgn' /proc/$$/status
set +m
sh -c 'ps -o pgid= -p $$ | tr -d " "' > bg2 &
wait
[ "$(cat bg2)" = "$me" ] && echo bg-shell-group-after-plus-m
