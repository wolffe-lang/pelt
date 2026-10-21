# sh19 #34: 2,000 turns of `f | :`: a shape pelt runs in-process today
f() { :; }
i=0
while [ "$i" -lt 2000 ]; do
    f | :
    i=$((i + 1))
done
echo "$i"
