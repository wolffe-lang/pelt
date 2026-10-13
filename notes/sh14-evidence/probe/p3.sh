# every catchable signal: trap fires on kill to self
for s in HUP INT QUIT USR1 USR2 PIPE ALRM TERM ABRT CONT WINCH URG VTALRM PROF XCPU XFSZ CHLD TSTP TTIN TTOU ILL TRAP BUS FPE SEGV SYS IO PWR STKFLT; do
  trap "echo got-$s" $s 2>/dev/null || { echo "notrap-$s"; continue; }
  kill -s $s $$; echo "after-$s st=$?"
  trap - $s
done
echo "--- ignore then send"
for s in HUP INT QUIT USR1 USR2 PIPE ALRM TERM ABRT WINCH URG VTALRM PROF XCPU XFSZ TSTP TTIN TTOU; do
  trap '' $s; kill -s $s $$; echo "ign-$s alive"; trap - $s
done
echo "--- default deaths (child shells)"
for s in HUP INT QUIT USR1 USR2 PIPE ALRM TERM ABRT VTALRM PROF XCPU XFSZ KILL ILL TRAP BUS FPE SEGV SYS; do
  /usr/bin/dash -c "kill -s $s \$\$; echo survived" 2>/dev/null; echo "$s -> $?"
done
echo "--- defaults that do nothing"
for s in CONT WINCH URG CHLD; do
  /usr/bin/dash -c "kill -s $s \$\$; echo survived-$s"; echo "$s -> $?"
done
echo "--- order of two pending"
trap 'echo T' TERM; trap 'echo H' HUP; trap 'echo U1' USR1; trap 'echo U2' USR2; trap 'echo A' ALRM; trap 'echo W' WINCH
/bin/sh -c 'kill -TERM $PPID; kill -WINCH $PPID; kill -USR2 $PPID; kill -HUP $PPID; kill -ALRM $PPID; kill -USR1 $PPID'
echo done
