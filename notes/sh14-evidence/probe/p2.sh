# trap forms
echo "--- trap -l"; trap -l 2>&1 | head -3; echo "st=$?"
echo "--- trap -p"; trap -p 2>&1 | head -3; echo "st=$?"
echo "--- names"
for c in HUP SIGHUP hup sighup SigHup INT QUIT ILL TRAP ABRT IOT BUS FPE KILL USR1 SEGV USR2 PIPE ALRM TERM STKFLT CHLD CLD CONT STOP TSTP TTIN TTOU URG XCPU XFSZ VTALRM PROF WINCH IO POLL PWR SYS RTMIN RTMAX EXIT exit SIGEXIT ERR DEBUG RETURN 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 63 64 65 100 -1 1x '' ' 1' 01 +1; do
  (trap ':' "$c" 2>/dev/null; echo "[$c] st=$? -> $(trap)") 
done
