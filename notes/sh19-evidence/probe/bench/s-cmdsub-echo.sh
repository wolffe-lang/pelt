# sh19 #34: 2,000 turns of `x=$(echo y)`: a shape pelt runs in-process today
i=0
while [ "$i" -lt 2000 ]; do
    x=$(echo y)
    i=$((i + 1))
done
echo "$i"
