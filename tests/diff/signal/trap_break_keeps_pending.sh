# An action that leaves a loop with `break` does not lose a second
# signal that was waiting with the first.
trap 'echo one; break' USR1
trap 'echo two' USR2
for i in 1 2 3; do
  echo "turn $i"
  /bin/sh -c 'kill -USR2 $PPID; kill -USR1 $PPID'
done
echo end
