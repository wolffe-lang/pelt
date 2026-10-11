printf 'a,b,c' | { read -d , x; echo "[$x]"; read -d , y; echo "[$y]"; }
printf 'one\ntwo\0rest' | { read -r -d '' x; echo "[$x]"; }
