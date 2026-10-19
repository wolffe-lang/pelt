# sh19 #34: 2,000 turns of `/bin/true`: the control: a program (fork.sh's body)
i=0
while [ "$i" -lt 2000 ]; do
    /bin/true
    i=$((i + 1))
done
echo "$i"
