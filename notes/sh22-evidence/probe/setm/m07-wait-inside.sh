# set -m in a script: a loop that waits for each job
set -m
i=0
while [ $i -lt 3 ]; do
  sh -c "exit $i" &
  wait $!
  echo "turn $i waited: $?" >&2
  i=$((i+1))
done
echo "the loop has ended" >&2
echo "the next command" >&2
