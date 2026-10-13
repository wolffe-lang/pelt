# A program the shell starts or becomes begins with a caught signal at
# its default and an ignored one ignored (XCU 2.12; XSH exec).
trap 'echo parent' USR1
trap '' USR2
../sh -c '/bin/sh -c "kill -USR2 \$PPID"; echo ignored-in-child'
../sh -c 'exec ../sh -c "/bin/sh -c \"kill -USR2 \\\$PPID\"; echo ignored-after-exec"'
../sh -c '/bin/sh -c "kill -USR1 \$PPID"; sleep 1; echo wrongly-alive' 2>/dev/null
[ $? -gt 128 ] && echo default-in-child
(exec ../sh -c '/bin/sh -c "kill -USR1 \$PPID"; sleep 1; echo wrongly-alive') 2>/dev/null
[ $? -gt 128 ] && echo default-after-exec
echo end
