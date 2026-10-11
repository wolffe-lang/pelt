set -- -ab -cvalue -- -d
while getopts abc:d o; do echo "$o ${OPTARG-none}"; done; shift $((OPTIND-1)); echo "$@"
