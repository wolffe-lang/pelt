# census coin witness: configure-sed's filesystem timestamp-resolution
# check, in this project's own words (sh14's `ts.sh`): two files written
# one after the other; is the second newer by `ls -t` at the first look?
# One try; prints 1 when it is (configure would print 0.1), 2 when it
# is not until the next look (0.2), more when later still. Which of the
# two a shell sees depends on how long it takes between the two writes
# against the filesystem's clock tick: dash itself sees either.
# Run by tools/script-census --coins, N times a shell, in the row's image.
rm -f f.a f.b
: > f.a
ok=true
if $ok
then :
    nap=0.1 loops=20
else
    nap=1 loops=2
fi
try=0
while :; do
  try=$((try + 1))
  echo "stamp $try" > f.b
  set X `ls -t f.a f.b`
  if test "$2" = f.b || test $try -eq $loops; then
    break
  fi
  sleep $nap
done
echo $try
