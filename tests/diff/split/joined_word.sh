x=' a '
set -- x${x}y
echo $#
for a; do echo "[$a]"; done
