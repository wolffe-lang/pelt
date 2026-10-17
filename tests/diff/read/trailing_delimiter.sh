echo 'a:b:c::' | { IFS=: read x y z; echo "[$x][$y][$z]"; }
echo 'a:b:c: ' | { IFS=': ' read x y z; echo "[$x][$y][$z]"; }
echo 'a:b:c :' | { IFS=': ' read x y z; echo "[$x][$y][$z]"; }
echo 'a:b' | { IFS=: read x y z; echo "[$x][$y][$z]"; }
echo 'a:' | { IFS=: read x; echo "[$x]"; }
echo 'a::' | { IFS=: read x; echo "[$x]"; }
echo ':' | { IFS=: read x; echo "[$x]"; }
echo 'a,b,' | { IFS=, read x y; echo "[$x][$y]"; }
echo 'a,b,,' | { IFS=, read x y; echo "[$x][$y]"; }
echo 'a\:b:' | { IFS=: read x; echo "[$x]"; }
echo 'a:b\:' | { IFS=: read x y; echo "[$x][$y]"; }
echo 'c d  ' | { read x; echo "[$x]"; }
