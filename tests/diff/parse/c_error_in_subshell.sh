(eval 'if then'; echo no) 2>/dev/null; echo "st=$?"
x=$(: ${u?unset} 2>/dev/null; echo no); echo "st=$? [$x]"
echo survived
