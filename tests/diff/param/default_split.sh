unset x
set -- ${x:-a b} "${x:-c d}"
echo $#
