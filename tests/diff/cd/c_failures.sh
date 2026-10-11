: > file; before=$PWD
cd nonexistent 2>/dev/null; echo "st=$?"
cd file 2>/dev/null; echo "st=$?"
cd a b 2>/dev/null; echo "st=$?"
[ "$PWD" = "$before" ] && echo unchanged
