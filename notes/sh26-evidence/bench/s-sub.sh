# sh19 #34: 2,000 turns of `( : )`: a shape pelt runs in-process today
i=0
while [ "$i" -lt 2000 ]; do
    ( : )
    i=$((i + 1))
done
echo "$i"
