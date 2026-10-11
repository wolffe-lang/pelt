(: < /nonexistent; echo not-reached) 2>/dev/null; echo "st=$?"
(exec < /nonexistent; echo not-reached) 2>/dev/null; echo "st=$?"
(export X=1 > /nonexistent/x; echo not-reached) 2>/dev/null; echo "st=$?"
