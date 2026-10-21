# sh19 #34: 2,000 turns of `{ :; } & wait`: a shape pelt runs in-process today
i=0
while [ "$i" -lt 2000 ]; do
    { :; } & wait
    i=$((i + 1))
done
echo "$i"
