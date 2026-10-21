W=$PWD
mkdir -p elsewhere/kid elsewhere/only kid
CDPATH=$W/elsewhere
kid; echo "kid st=$? ${PWD#$W}"
cd "$W"
only; echo "only st=$? ${PWD#$W}"
cd "$W"
unset CDPATH
