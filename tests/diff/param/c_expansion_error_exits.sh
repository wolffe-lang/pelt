(echo ${x!y}; echo not-reached) 2>/dev/null; echo "st=$?"
(set -u; echo $nope; echo not-reached) 2>/dev/null; echo "st=$?"
(echo $((1+)); echo not-reached) 2>/dev/null; echo "st=$?"
