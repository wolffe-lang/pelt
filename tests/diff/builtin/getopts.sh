set -- -a -b val -cd rest
while getopts ab:cd o; do echo "$o ${OPTARG-}"; done
echo $OPTIND
shift $((OPTIND-1))
echo $@
