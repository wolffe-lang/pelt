# `kill -l`: a number names its signal, an exit status above 128 names
# the signal that ended the command, and only the first operand is
# read (dash). The numbers XCU `kill` fixes: 1 2 3 6 9 14 15.
for n in 1 2 3 6 9 14 15; do kill -l $n; done | tr '\n' ' '; echo
for n in 129 130 131 134 137 142 143; do kill -l $n; done | tr '\n' ' '; echo
kill -l 15 9; echo "st=$?"
kill -l -- 15; echo "st=$?"
for n in 0 128 255 256 257 999 x HUP -1 ''; do kill -l "$n" 2>/dev/null; echo "[$n] $?"; done
# every name POSIX gives a signal is listed
for s in HUP INT QUIT ILL TRAP ABRT BUS FPE KILL USR1 SEGV USR2 PIPE ALRM TERM CHLD CONT STOP TSTP TTIN TTOU URG XCPU XFSZ VTALRM PROF WINCH SYS; do
  kill -l | grep -q -x "$s" || echo "missing $s"
done
echo listed
# and each is a signal `kill -s` takes: sent to a process id no host
# hands out, the answer is "no such process" (1), not "no such signal" (2)
for s in HUP INT QUIT ILL TRAP ABRT BUS FPE KILL USR1 SEGV USR2 PIPE ALRM TERM CHLD CONT STOP TSTP TTIN TTOU URG XCPU XFSZ VTALRM PROF WINCH SYS; do
  kill -s $s 999999999 2>/dev/null; [ $? = 1 ] || echo "refused $s"
  kill -$s 999999999 2>/dev/null; [ $? = 1 ] || echo "refused -$s"
done
kill -s NOSUCH 999999999 2>/dev/null; echo "unknown=$?"
echo taken
