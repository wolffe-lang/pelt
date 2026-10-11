set -- -z
while getopts ab: o -a -b val; do echo "$o ${OPTARG-none}"; done
