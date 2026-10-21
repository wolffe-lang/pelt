W=$PWD
mkdir a b
cd a b; echo "cd-two st=$? ${PWD#$W}"
cd "$W"
cd -- a b; echo "cd-dd-two st=$? ${PWD#$W}"
cd "$W"
