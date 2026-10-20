# the control: m01 without set -m (no notices in a script)
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
