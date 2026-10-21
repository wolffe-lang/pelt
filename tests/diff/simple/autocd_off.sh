mkdir -p d/e child "my dir"
echo 'echo ran' > f
d/e; echo "slash st=$? ${PWD##*/}"
"$PWD/d/"; echo "abs st=$? ${PWD##*/}"
child; echo "bare st=$? ${PWD##*/}"
..; echo "dotdot st=$? ${PWD##*/}"
"my dir"; echo "space st=$? ${PWD##*/}"
./f; echo "file st=$? ${PWD##*/}"
./nope/; echo "nope st=$? ${PWD##*/}"
