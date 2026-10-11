x='a:b c'
IFS=:; set -- $x; echo $#
IFS=' '; set -- $x; echo $#
IFS=: eval 'set -- $x'; echo $#
