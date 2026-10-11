[ -c /dev/null ]; echo "c=$?"; [ -b /dev/null ]; echo "b=$?"; [ -p /dev/null ]; echo "p=$?"; [ -S /dev/null ]; echo "S=$?"
: > f; chmod u+s f; [ -u f ]; echo "u=$?"; chmod 2755 f 2>/dev/null; [ -g f ]; echo "g=$?"
[ -t 0 ] </dev/null; echo "t=$?"; [ -t 9 ]; echo "t9=$?"
