IFS=
x='a b'; e=
set -- $x; echo $#
set -- $e; echo $#
set -- $e"" $x$e; echo $#
