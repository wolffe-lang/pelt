trap ':' NOSUCHSIG 2>/dev/null; echo "st=$?"
trap ':' 999 2>/dev/null; echo "st=$?"
echo survived
