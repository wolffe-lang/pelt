W=$PWD
mkdir child "my dir"
child; echo "child st=$? ${PWD#$W}"
cd "$W"
"my dir"; echo "space st=$? ${PWD#$W}"
cd "$W"
d=child
$d; echo "var st=$? ${PWD#$W}"
cd "$W"
