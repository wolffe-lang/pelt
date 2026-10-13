# kill -l forms
echo "--- kill -l"; kill -l; echo "st=$?"
echo "--- kill -l nums"; for n in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 64 65; do printf '%s=' $n; kill -l $n 2>&1; echo " st=$?"; done
echo "--- kill -l status"; for n in 128 129 130 137 143 159 160 192 255 256 257 300 385 -1; do printf '%s=' $n; kill -l $n 2>&1; echo " st=$?"; done
echo "--- kill -l names"; for n in HUP SIGHUP hup TERM; do printf '%s=' $n; kill -l $n 2>&1; echo " st=$?"; done
echo "--- kill -l two"; kill -l 1 2 2>&1; echo "st=$?"
echo "--- kill -L"; kill -L 2>&1 | head -3; echo "st=$?"
echo "--- kill none"; kill 2>&1; echo "st=$?"
echo "--- kill -s none"; kill -s 2>&1; echo "st=$?"
echo "--- kill -s TERM none"; kill -s TERM 2>&1; echo "st=$?"
echo "--- kill -n"; sleep 5 & p=$!; kill -n 15 $p 2>&1; echo "st=$?"; kill $p 2>/dev/null; wait $p; echo "w=$?"
echo "--- forms"
for how in '-s SIGTERM' '-s term' '-s Term' '-SIGTERM' '-term' '-s 0' '-0' '-s 9' '-KILL' '-s USR1' '-USR1' '-10' '-s INT' '-INT' '-2' '-s QUIT' '-s ABRT' '-6' '-s ALRM' '-s PIPE' '-s USR2' '-s CONT' '-s STOP' '-s SEGV' '-s BUS' '-s FPE' '-s ILL' '-s TRAP' '-s SYS' '-s XCPU' '-s XFSZ' '-s VTALRM' '-s PROF' '-s WINCH' '-s URG' '-s CHLD' '-s TSTP' '-s TTIN' '-s TTOU' '-s IO' '-s PWR' '-s STKFLT' '-s POLL' '-s RTMIN' '-s 64' '-s 65' '-65' '-s EXIT' '-EXIT' '-s 1x' '-1x' '-s -1' '--' '-- -TERM' '-s TERM --' '-TERM --' '-l --' '-x' '-s TERM -s KILL'; do
  sleep 5 & p=$!; kill $how $p 2>/dev/null; k=$?; kill -9 $p 2>/dev/null; wait $p 2>/dev/null; echo "[$how] kill=$k wait=$?"
done
echo "--- targets"
kill -0 $$; echo "self0=$?"
kill -0 999999999 2>/dev/null; echo "nosuch=$?"
kill -0 99999999999999999999 2>/dev/null; echo "huge=$?"
kill -0 abc 2>/dev/null; echo "abc=$?"
kill -0 1 2>/dev/null; echo "init=$?"
kill -0 '' 2>/dev/null; echo "empty=$?"
kill -0 12x 2>/dev/null; echo "12x=$?"
kill -0 +$$ 2>/dev/null; echo "plus=$?"
kill -0 " $$" 2>/dev/null; echo "space=$?"
kill -0 0$$ 2>/dev/null; echo "zero-lead=$?"
sleep 5 & a=$!
kill -0 $a 999999999 2>/dev/null; echo "mixed=$?"
kill $a; wait $a; echo "w=$?"
kill -0 %1 2>/dev/null; echo "nojob=$?"
kill -0 %5 2>/dev/null; echo "nojob5=$?"
kill -0 % 2>/dev/null; echo "pct=$?"
