W=$PWD
mkdir -p d/e
d/e; echo "slash st=$? ${PWD#$W}"
d; echo "bare st=$? ${PWD#$W}"
"$W/d/"; echo "abs st=$? ${PWD#$W}"
