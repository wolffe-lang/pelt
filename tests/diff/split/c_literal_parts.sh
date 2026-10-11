x='b c'
set -- a$x'd e'; echo "$# [$1][$2]"
IFS=:; y='p:q'; set -- a:$y:z; echo "$# [$1][$2]"
