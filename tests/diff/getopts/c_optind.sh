echo "$OPTIND"
set -- -a x -b
getopts ab o; echo "$o $OPTIND"; getopts ab o; echo "st=$? $OPTIND"
OPTIND=1; getopts ab o; echo "$o $OPTIND"
set -- - -a; OPTIND=1; getopts a o; echo "st=$? $OPTIND"
