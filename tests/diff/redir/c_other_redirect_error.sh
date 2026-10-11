{ echo no; } < /nonexistent; echo "st=$?"
if true; then echo no; fi > /nonexistent/x; echo "st=$?"
f() { echo no; }; f < /nonexistent; echo "st=$?"
echo no > /nonexistent/x; echo "st=$?"
while false; do :; done < /nonexistent; echo "st=$?"
echo survived
