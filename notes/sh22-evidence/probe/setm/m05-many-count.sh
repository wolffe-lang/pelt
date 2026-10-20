# set -m in a script: a loop of 500 jobs nobody waits for; how many
# does the table hold at the loop's end, and after the next command?
set -m
i=0
while [ $i -lt 500 ]; do
  sh -c 'exit 0' &
  i=$((i+1))
done
sleep 1
echo "remembered at the loop's end: $(jobs -p | grep -c .)" >&2
echo "remembered a command later: $(jobs -p | grep -c .)" >&2
