# bench/param.sh — 200,000 turns of expansion and arithmetic with no
# external command: what the shell itself costs per simple command.
x=usr/local/lib/pelt/share
i=0
n=0
while [ "$i" -lt 200000 ]; do
    y=${x#*/}
    z=${x%/*}
    n=$((n + ${#y} + ${#z}))
    case $y in
    local/*) n=$((n + 1)) ;;
    *) n=$((n - 1)) ;;
    esac
    i=$((i + 1))
done
echo "$n"
