# sh14: the shape of automake's timestamp-resolution check (two files written one after the
# other; is the second newer by `ls -t`?), in this lane's own words, one try. Prints 1 when the
# second file is already newer at the first look (configure would print 0.1), 2 when not (0.2).
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
