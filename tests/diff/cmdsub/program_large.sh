x=$(i=0; while [ $i -lt 3000 ]; do echo $i; i=$((i+1)); done | tail -n 1)
echo $x
y=$(cat /dev/null; printf '%s\n' a b | wc -l)
echo $y
