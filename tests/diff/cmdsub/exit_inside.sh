x=$(echo a; exit 4; echo b)
echo $? $x
