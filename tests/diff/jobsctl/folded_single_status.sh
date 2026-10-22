# Folding must preserve a waited background status, without taking away
# the foreground pipeline's per-process status reader (pelt#46).
exec 2>/dev/null
set -m
true | sh -c 'exit 7'
echo pipeline=$?
i=0
while [ $i -lt 3 ]; do
  sh -c 'exit 9' & wait $!
  echo wait=$?
  jobs -l >f
  wc -l <f | tr -d ' '
  i=$((i+1))
done
rm -f f
