W=$PWD
mkdir sub
(sub; echo "in sub ${PWD#$W}"); echo "after sub ${PWD#$W}"
cd "$W"
sub | cat; echo "pipe ${PWD#$W}"
cd "$W"
FOO=bar sub; echo "assign st=$? FOO=${FOO-unset} ${PWD#$W}"
cd "$W"
sub >out 2>err; echo "redir st=$? ${PWD#$W}"
cd "$W"
echo "files: [$(cat out 2>/dev/null)] [$(cat err 2>/dev/null)]"
sub; echo "old=${OLDPWD#$W} pwd=${PWD#$W}"
cd -; echo "back st=$? ${PWD#$W}"
