echo ' a  b   c d  ' | { read x y z; echo "[$x][$y][$z]"; }
echo 'only' | { read x y; echo "[$x][$y]"; }
echo '' | { read x y; echo "[$x][$y] $?"; }
echo 'a:b::c:' | { IFS=: read x y z; echo "[$x][$y][$z]"; }
echo 'a:b:c:' | { IFS=: read x y z; echo "[$x][$y][$z]"; }
echo ' a : b ' | { IFS=' :' read x y; echo "[$x][$y]"; }
