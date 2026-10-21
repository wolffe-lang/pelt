# bench/fork.sh — 2,000 external commands, one at a time: what a shell
# costs to start a program and wait for it.
i=0
while [ "$i" -lt 2000 ]; do
    /bin/true
    i=$((i + 1))
done
