set -- -x
getopts a o 2>/dev/null; echo "$o ${OPTARG-unset}"
OPTIND=1; getopts :a o; echo "$o ${OPTARG-unset}"
OPTIND=1; getopts a o 2>&1 | wc -l | tr -d ' '
