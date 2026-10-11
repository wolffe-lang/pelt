(set -o nosuchoption 2>/dev/null; echo no) ; echo "st=$?"
(. /nonexistent/file 2>/dev/null; echo no); echo "st=$?"
