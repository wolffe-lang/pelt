# set -m in a script: the jobs a loop starts are told after the loop (its
# complete command) ends, newest first, the ones `wait` answered too, and
# not inside it (dash, black-box: notes/sh22-evidence/refs/setm-base/m07;
# pelt#41). Standard error is standard output here, so the notices are
# compared byte for byte.
exec 2>&1
set -m
i=0
while [ $i -lt 3 ]; do
  sh -c "exit $i" &
  wait $!
  echo "turn $i waited: $?"
  i=$((i+1))
done
echo "the loop has ended"
echo "the next command"
