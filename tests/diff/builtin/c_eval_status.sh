eval '(exit 3)'; echo $?
eval 'false; true'; echo $?
(eval 'fi'; echo no) 2>/dev/null; echo "st=$?"
