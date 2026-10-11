readonly r=1
(r=2; echo not-reached) 2>/dev/null; echo "st=$?"
(r=2 true; echo not-reached-or-reached) 2>/dev/null; echo "st=$?"
(for r in a; do echo not-reached; done; echo not-reached) 2>/dev/null; echo "st=$?"
