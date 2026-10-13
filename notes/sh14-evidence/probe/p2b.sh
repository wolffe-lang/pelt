# what trap prints for each, in the shell itself (not $(...))
for c in HUP INT QUIT ILL TRAP ABRT BUS FPE KILL USR1 SEGV USR2 PIPE ALRM TERM STKFLT CHLD CONT STOP TSTP TTIN TTOU URG XCPU XFSZ VTALRM PROF WINCH IO PWR SYS 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 63 64 65; do
  trap ':' "$c" 2>/dev/null; st=$?; trap > t.out; echo "[$c] st=$st -> $(cat t.out)"; trap - "$c" 2>/dev/null
done
echo "--- order"
trap 'a' TERM; trap 'b' HUP; trap 'c' USR1; trap 'd' EXIT; trap 'e' WINCH; trap '' INT; trap 'f' 14
trap
trap - TERM HUP USR1 EXIT WINCH INT ALRM
echo "--- reset forms"
trap 'x' USR1; trap USR1; trap; echo "st=$?"
trap 'x' USR1; trap 10; trap; echo "st=$?"
trap 'x' USR1; trap - ; trap; echo "st=$?"; trap - USR1
trap 'x' USR1; trap -- - USR1; trap; echo "st=$?"
trap 1 2 2>&1; trap; echo "st=$?"; trap - 2
trap -x 2>&1; echo "st=$?"
trap 'x' NOSUCH 2>/dev/null; echo "bad=$?"
trap 'x' USR1 NOSUCH USR2 2>/dev/null; echo "mixed=$?"; trap; trap - USR1 USR2
echo still here
