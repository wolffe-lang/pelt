cd /nonexistent 2>/dev/null; echo "st=$?"
read x </dev/null; echo "st=$?"
test 1 -eq x 2>/dev/null; echo "st=$?"
echo survived
