# jobs and kill %n in a script
sleep 5 & sleep 6 &
kill %1; echo "k1=$?"; kill %2; echo "k2=$?"; wait; echo "w=$?"
sleep 5 & kill %%; echo "kcur=$?"; wait
sleep 5 & kill %+; echo "kplus=$?"; wait
sleep 5 & sleep 6 & kill %-; echo "kminus=$?"; kill %+; wait
sleep 5 & kill %sleep; echo "kname=$?"; wait
sleep 5 & kill %?lee; echo "ksub=$?"; wait
sleep 5 & kill %3 2>/dev/null; echo "kbad=$?"; kill %1 2>/dev/null; echo "k1again=$?"; kill $!; wait
true & wait; kill %1 2>/dev/null; echo "done-job=$?"
sleep 5 & a=$!; sleep 5 & b=$!; kill -s KILL %1 %2; wait $a; echo $?; wait $b; echo $?
sleep 5 & p=$!; kill -0 %1; echo "zero=$?"; kill %1; wait %1; echo "wj=$?"
(exit 3) & wait %1; echo "st=$?"
