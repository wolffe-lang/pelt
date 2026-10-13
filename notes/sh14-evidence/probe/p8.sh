sleep 5 & a=$!
kill abc $a 2>/dev/null; echo "st=$?"; kill -0 $a 2>/dev/null; echo "alive-after-bad-first=$?"; kill $a 2>/dev/null; wait $a 2>/dev/null
sleep 5 & a=$!
kill 999999999 $a 2>/dev/null; echo "st=$?"; kill -0 $a 2>/dev/null; echo "alive-after-missing-first=$?"; kill $a 2>/dev/null; wait $a 2>/dev/null
sleep 5 & a=$!
kill -stop $a 2>/dev/null; echo "lower-stop=$?"
kill -segv $a 2>/dev/null; echo "lower-segv=$?"
kill -STOP $a 2>/dev/null; echo "upper-STOP=$?"; kill -CONT $a; kill -sys $a 2>/dev/null; echo "lower-sys=$?"
kill -9 $a 2>/dev/null; wait $a 2>/dev/null; echo "w=$?"
sleep 5 & a=$!
kill -s stop $a; echo "s-stop=$?"; kill -s cont $a; echo "s-cont=$?"; kill -KILL $a; wait $a 2>/dev/null
kill -0 0x10 2>/dev/null; echo "hex=$?"
kill -0 -- $$; echo "dd=$?"
kill -0 -$$ 2>/dev/null; echo "neg-no-dd=$?"
kill -l 15 extra junk; echo "st=$?"
kill -l -9 2>/dev/null; echo "l-neg=$?"
kill -s TERM -l 2>/dev/null; echo "s-then-l=$?"
kill -l 143 >/dev/null; echo "st=$?"
