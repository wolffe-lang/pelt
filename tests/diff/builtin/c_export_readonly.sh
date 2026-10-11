readonly r=1
(export r=2; echo no) 2>/dev/null; echo "st=$?"
export r; sh -c 'echo $r'
