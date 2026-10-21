W=$PWD
mkdir jdir
command_not_found_handle() { echo "handler [$*]"; return 0; }
jdir; echo "dir st=$? ${PWD#$W}"
cd "$W"
fuzzy x; echo "fuzzy st=$? ${PWD#$W}"
./jdir; echo "slashed st=$? ${PWD#$W}"
cd "$W"
