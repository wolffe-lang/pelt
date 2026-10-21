W=$PWD
mkdir sub
cd() { echo "fn cd [$#] $*"; command cd "$@"; }
sub; echo "bare st=$? ${PWD#$W}"
command cd "$W"
./sub; echo "slash st=$? ${PWD#$W}"
command cd "$W"
unset -f cd
