set -u
(unset u; echo ${#u}; echo not-reached) 2>/dev/null; echo "st=$?"
