# Every signal POSIX lets a program catch can be trapped (XCU 2.12):
# the action runs when a child sends it, and the shell goes on.
for s in HUP INT QUIT USR1 USR2 PIPE ALRM TERM ABRT CONT WINCH URG VTALRM PROF XCPU XFSZ TSTP TTIN TTOU; do
  trap "echo got-$s" $s
  /bin/sh -c "kill -s $s \$PPID"; echo "after-$s $?"
  trap - $s
done
