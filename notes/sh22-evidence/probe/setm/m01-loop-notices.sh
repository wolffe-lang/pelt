# set -m in a script: when are a loop's jobs reported? (pelt#41)
set -m
i=0
while [ $i -lt 3 ]; do
  sh -c "exit $i" &
  sleep 0.3
  echo "iteration $i ends" >&2
  i=$((i+1))
done
echo "the loop has ended" >&2
sleep 0.3
echo "the next command" >&2
