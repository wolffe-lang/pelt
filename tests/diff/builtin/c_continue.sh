for i in 1 2 3; do [ $i = 2 ] && continue; echo $i; done
for i in 1 2; do for j in a b; do continue 2; echo no; done; echo no; done; echo done
i=0; while [ $i -lt 3 ]; do i=$((i+1)); continue; echo no; done; echo $i
i=0; until [ $i -ge 2 ]; do i=$((i+1)); continue 9; done; echo $i
