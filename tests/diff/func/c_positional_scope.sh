set -- a b c
f() { echo "$# $1 $0"; set -- x; shift; }
f p q; echo "$# $1"
