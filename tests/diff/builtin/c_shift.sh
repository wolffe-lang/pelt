set -- a b c d e
shift; echo "$# $1"; shift 2; echo "$# $1"; shift 0; echo "$# $1"; shift 2; echo $#
