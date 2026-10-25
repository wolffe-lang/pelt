# pelt#28: a bad option to trap ends a script, status 2, in dash's words
# after the shell's own prefix; `trap -- -x` sets an action
(trap -x 'echo t' INT; echo not-reached) 2>&1 | sed 's/^.*trap: //'
(trap -xy 'echo t' INT) 2>/dev/null; echo "st=$?"
(trap -- -x INT; echo "dd st=$?")
