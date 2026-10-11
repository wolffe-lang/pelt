echo '$HOME * ~ $(echo x)' | { read -r x; echo "$x"; }
IFS=,; echo 'a,b c' | { read x y; echo "[$x][$y]"; }
