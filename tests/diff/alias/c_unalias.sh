alias a=1 b=2 c=3
unalias a; alias a 2>/dev/null; echo "st=$?"
unalias nope 2>/dev/null; echo "st=$?"
unalias -a; alias | wc -l | tr -d ' '
