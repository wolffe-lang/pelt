HOME='/a b/*'; set -- ~; echo "$# $1"
HOME=; set -- ~; echo $#
