i=0
while true; do i=$((i+1)); [ $i -eq 5 ] && break; done
echo $i
