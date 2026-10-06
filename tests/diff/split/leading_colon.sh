IFS=:
x='::a::'
set -- $x
echo $#
for a; do echo "[$a]"; done
