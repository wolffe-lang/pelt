mkdir -p d/e
command set -o autocd 2>/dev/null
d/e; echo "slash st=$? ${PWD##*/}"
d; echo "bare st=$? ${PWD##*/}"
"$PWD/d/"; echo "abs st=$? ${PWD##*/}"
../sh -c 'command set -o autocd 2>/dev/null; d/e; echo "c st=$? ${PWD##*/}"'
../sh -c 'command set -o autocd 2>/dev/null; d; echo "c bare st=$? ${PWD##*/}"'
