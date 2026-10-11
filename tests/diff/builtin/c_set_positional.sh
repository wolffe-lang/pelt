set -- a b c; set -- x; echo "$# $1"
set --; echo $#
set -- -x; echo "$1"
set a -b; echo "$# $2"
set -- a b; set -f; echo $#
