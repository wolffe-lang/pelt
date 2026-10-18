set -m
sh -c 'ps -o pgid=,tpgid= -p $$' &
wait
echo "\$-=$-"
