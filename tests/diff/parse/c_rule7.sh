a=1 b=2 echo ok
=x 2>/dev/null; echo "st=$?"
1a=2 2>/dev/null; echo "st=$?"
echo a=1
'a'=3 2>/dev/null; echo "st=$?"
a\=4 2>/dev/null; echo "st=$?"
