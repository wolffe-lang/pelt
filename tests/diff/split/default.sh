x='  a  b	c
d  '
set -- $x
echo $#
for a; do echo "[$a]"; done
