# set -m in a script: what `jobs` shows inside the loop, each turn
set -m
i=0
while [ $i -lt 3 ]; do
  sh -c "exit $i" &
  sleep 0.3
  echo "turn $i: jobs says:" >&2
  jobs >&2
  i=$((i+1))
done
echo "after the loop, jobs says:" >&2
jobs >&2
echo "end" >&2
