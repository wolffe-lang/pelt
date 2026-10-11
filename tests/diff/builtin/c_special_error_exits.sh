(set -o nosuchoption; echo not-reached) 2>/dev/null; echo "st=$?"
(. /nonexistent/file; echo not-reached) 2>/dev/null; echo "st=$?"
(readonly r=1; r=2; echo not-reached) 2>/dev/null; echo "st=$?"
(break 0; echo not-reached-or-reached) 2>/dev/null; echo "st=$?"
