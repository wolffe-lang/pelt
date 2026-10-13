D=/usr/bin/dash
echo "--- -i via stdin, TERM default at start"
printf 'trap "echo trapped-i" TERM\nkill -TERM $$\necho after-i\n' | $D -i 2>/dev/null
echo "--- -i via stdin, TERM, USR1 ignored at start"
trap '' TERM USR1
printf 'trap "echo trapped-i" TERM\nkill -TERM $$\necho after-i\ntrap "echo u1" USR1\nkill -USR1 $$\necho after-u1\ntrap\n' | $D -i 2>/dev/null
echo "--- -i, INT ignored at start"
trap '' INT QUIT
printf 'trap "echo trapped-int" INT\nkill -INT $$\necho after-int\ntrap - INT\nkill -INT $$\necho after-reset\n' | $D -i 2>/dev/null
trap - TERM USR1 INT QUIT
echo "--- kill misc"
sleep 5 & p=$!
kill -s TERM $p $p; echo "twice=$?"; wait $p; echo "w=$?"
kill $p 2>/dev/null; echo "reaped=$?"
kill -l 0 2>/dev/null; echo "l0=$?"
kill -l -- 15 2>&1; echo "l--=$?"
kill -l x 2>/dev/null; echo "lx=$?"
kill -- 2>/dev/null; echo "dd-none=$?"
kill -s 2>/dev/null TERM; echo "s-nopid=$?"
kill -9 2>/dev/null; echo "9-nopid=$?"
kill -l -s 2>/dev/null; echo "l-s=$?"
$D -c "kill -sTERM \$\$; echo no"; echo "sTERM=$?"
echo "--- kill self default in script: exit status by parent"
$D -c 'kill $$; echo no'; echo "st=$?"
$D -c 'kill -s INT $$; echo no'; echo "st=$?"
$D -c 'trap "" INT; kill -s INT $$; echo yes'; echo "st=$?"
$D -c 'kill -0 $$ && echo zero-ok; kill -s 0 $$ && echo s0-ok'
echo "--- trap action sees \$? and exit in action"
$D -c 'trap "echo in=\$?; exit 7" USR1; (exit 3); kill -USR1 $$; echo no'; echo "st=$?"
$D -c 'trap "echo in=\$?" USR1; (exit 3); kill -USR1 $$; echo "after=$?"'
$D -c 'trap "echo a; kill -USR2 \$\$; echo b" USR1; trap "echo c" USR2; kill -USR1 $$; echo d'
$D -c 'trap "trap - USR1; echo once" USR1; kill -USR1 $$; echo mid; (kill -USR1 $$; echo no) ; echo "st=$?"' 2>/dev/null
echo "--- EXIT trap on signal death / trap exit"
$D -c 'trap "echo bye" EXIT; kill -TERM $$; echo no'; echo "st=$?"
$D -c 'trap "echo bye" EXIT; trap "exit 3" TERM; kill -TERM $$; echo no'; echo "st=$?"
echo "--- in function, loop"
$D -c 'trap "echo t; break" USR1; for i in 1 2 3; do echo $i; kill -USR1 $$; done; echo end'
$D -c 'f() { kill -USR1 $$; echo in-f; }; trap "echo t; return 5" USR1; f; echo "st=$?"'
echo "--- kill pid lists + bad"
sleep 5 & a=$!
kill $a abc 2>/dev/null; echo "st=$?"; wait $a; echo "w=$?"
sleep 5 & a=$!
kill abc $a 2>/dev/null; echo "st=$?"; kill $a 2>/dev/null; wait $a; echo "w=$?"
echo end
