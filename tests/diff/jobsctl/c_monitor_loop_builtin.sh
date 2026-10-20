# set -m in a script: a loop's jobs that are built-ins (dash runs each in
# a subshell; pelt runs it itself) are told after the loop like any other,
# not one complete command later (dash, black-box:
# notes/sh22-evidence/refs/setm-base/m02; pelt#41)
exec 2>&1
set -m
i=0
while [ $i -lt 3 ]; do
  true &
  wait $!
  echo "turn $i"
  i=$((i+1))
done
echo "the loop has ended"
echo "the next command"
