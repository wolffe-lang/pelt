command . /nonexistent/file 2>/dev/null; echo "st=$?"
command set -o nosuchoption 2>/dev/null; echo "st=$?"
command exec 3</nonexistent 2>/dev/null; echo "st=$?"
echo survived
