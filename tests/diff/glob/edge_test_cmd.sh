touch '[' ']' x
[ -f x ] && echo yes
[ -f nope ] || echo no
echo [ -f x ]
i=0
while [ $i -lt 3 ]; do i=$((i+1)); done
echo $i
