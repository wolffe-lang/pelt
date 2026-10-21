W=$PWD
mkdir sub
(exec ./sub); echo "exec st=$? ${PWD#$W}"
cd "$W"
eval ./sub; echo "eval st=$? ${PWD#$W}"
cd "$W"
f() { ./sub; }; f; echo "in-function st=$? ${PWD#$W}"
cd "$W"
x=$(./sub; pwd); echo "cmdsub st=$? [${x#$W}] ${PWD#$W}"
cd "$W"
