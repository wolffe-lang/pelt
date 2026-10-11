exec 3>f; echo a >&3; echo b 1>&3; exec 3>&-; cat f
(echo to-err >&2) 2>&1 | cat
echo closed >&- 2>/dev/null; echo "st=$?"
