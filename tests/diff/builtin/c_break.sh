for i in 1 2 3; do for j in a b; do [ $j = b ] && break; echo $i$j; done; done
for i in 1 2 3; do for j in a b; do break 2; done; done; echo "i=$i"
for i in 1 2; do while :; do break 5; done; echo no; done; echo out
while :; do break; done; echo $?
