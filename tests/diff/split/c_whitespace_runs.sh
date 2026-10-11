x='   a    b   '
set -- $x; echo "$# [$1][$2]"
IFS='	 '; set -- $x; echo $#
