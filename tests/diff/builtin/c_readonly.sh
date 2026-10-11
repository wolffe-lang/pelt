readonly a=1; b=2; readonly b
(a=3; echo no) 2>/dev/null; echo "st=$?"
(unset b; echo "continued $?") 2>/dev/null; echo "st=$?"
echo "$a $b"
