echo 'if then' > bad
(. ./bad; echo no) 2>/dev/null; echo "st=$?"
