x=0
echo a | x=1; echo $x
x=2 | cat; echo $x
echo b | { read y; x=3; }; echo "$x[${y-}]"
exit 5 | cat; echo "still=$?"
