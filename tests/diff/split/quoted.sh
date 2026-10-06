x='a b'
set -- "$x" "$x$x"
echo $#
