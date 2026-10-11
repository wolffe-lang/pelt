: > f; chmod 000 f
[ -r f ]; echo "r=$?"; [ -w f ]; echo "w=$?"; [ -x f ]; echo "x=$?"
chmod 700 f; [ -r f ] && [ -w f ] && [ -x f ] && echo all
