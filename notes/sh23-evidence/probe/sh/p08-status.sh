W=$PWD
mkdir -m 000 locked
./locked; echo "locked-slash st=$? ${PWD#$W}"
locked; echo "locked-bare st=$? ${PWD#$W}"
./locked 2>err; echo "locked-redir st=$? ${PWD#$W} err=[$(cat err)]"
chmod 755 locked
mkdir sub
command ./sub; echo "command st=$? ${PWD#$W}"
cd "$W"
command sub; echo "command-bare st=$? ${PWD#$W}"
cd "$W"
