unset IFS
x='a	b
c d'; set -- $x; echo $#
echo ' p  q ' | { read a b; echo "[$a][$b]"; }
