W=$PWD
mkdir child other
child a b; echo "two st=$? ${PWD#$W}"
cd "$W"
child a; echo "one st=$? ${PWD#$W}"
cd "$W"
child other; echo "dir-word st=$? ${PWD#$W}"
cd "$W"
./child x; echo "slashed st=$? ${PWD#$W}"
cd "$W"
child -P; echo "option st=$? ${PWD#$W}"
cd "$W"
