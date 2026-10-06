IFS=:
x='a:b::c:'
set -- $x
echo $#
for a; do echo "[$a]"; done
