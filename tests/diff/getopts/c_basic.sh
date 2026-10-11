set -- -a -b arg -c rest
while getopts ab:c o; do echo "$o ${OPTARG-none} $OPTIND"; done
echo "end: $o $OPTIND"; shift $((OPTIND-1)); echo "$@"
