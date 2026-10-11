: > old; sleep 1; : > new; ln old same
[ old -ef same ]; echo "ef=$?"; [ old -ef new ]; echo "ef2=$?"
[ new -nt old ]; echo "nt=$?"; [ old -nt new ]; echo "nt2=$?"; [ old -ot new ]; echo "ot=$?"
[ new -nt missing ]; echo "nt-missing=$?"; [ missing -ot new ]; echo "ot-missing=$?"
