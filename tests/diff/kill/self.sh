# `kill` on the shell itself: a trapped signal's action runs before the
# next command, an ignored one does nothing, signal 0 only asks, and
# what the shell wrote before a signal that ends it is not lost.
trap 'echo got-usr1' USR1
kill -USR1 $$; echo "after=$?"
trap '' USR2
kill -s USR2 $$; echo "ignored=$?"
kill -0 $$ && echo zero-ok
../sh -c 'echo before; kill $$; echo not-reached'; echo "term: $(kill -l $?)"
../sh -c 'echo before; kill -s INT $$; echo not-reached'; echo "int: $(kill -l $?)"
../sh -c 'trap "echo bye" EXIT; kill $$; echo not-reached'; echo "no-exit-trap: $(kill -l $?)"
../sh -c 'trap "echo bye" EXIT; trap "exit 3" TERM; kill $$; echo not-reached'; echo "trap-exit: $?"
