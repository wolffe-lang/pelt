IFS=' :'
x=' :a : b: '
set -- $x
echo $#
for a; do echo "[$a]"; done
