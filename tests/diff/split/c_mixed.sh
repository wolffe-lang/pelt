IFS=' :'
x='a : b  :  : c'; set -- $x; echo "$# [$1][$2][$3][$4]"
y=' : a'; set -- $y; echo "$# [$1][$2]"
