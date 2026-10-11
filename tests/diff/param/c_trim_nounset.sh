set -u
(unset u; echo ${u#a}; echo not-reached) 2>/dev/null; echo "st=$?"
(unset u; echo ${u%%a}; echo not-reached) 2>/dev/null; echo "st=$?"
