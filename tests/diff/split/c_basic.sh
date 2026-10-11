x='a b	c
d'; set -- $x; echo $#
set -- a\ b "c d"; echo $#
