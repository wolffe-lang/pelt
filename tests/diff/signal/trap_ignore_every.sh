# And ignored: with `trap '' SIG` the signal does nothing to the shell.
for s in HUP INT QUIT USR1 USR2 PIPE ALRM TERM ABRT WINCH URG VTALRM PROF XCPU XFSZ TSTP TTIN TTOU; do
  trap '' $s
  /bin/sh -c "kill -s $s \$PPID"; echo "ignored-$s $?"
  trap - $s
done
