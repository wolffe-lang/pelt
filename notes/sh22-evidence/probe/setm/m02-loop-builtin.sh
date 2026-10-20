# set -m in a script, the job a built-in (dash forks it)
set -m
i=0
while [ $i -lt 3 ]; do
  true &
  sleep 0.3
  echo "iteration $i ends" >&2
  i=$((i+1))
done
echo "the loop has ended" >&2
sleep 0.3
echo "the next command" >&2
