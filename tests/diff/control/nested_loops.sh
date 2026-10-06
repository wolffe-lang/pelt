for i in 1 2 3; do
  for j in 1 2 3; do
    [ $j -gt $i ] && break
    echo $i$j
  done
done
