f() { OPTIND=1; while getopts xy: o; do echo "f:$o ${OPTARG-}"; done; }
f -x -y v; set -- -q; OPTIND=1; getopts q o; echo "main:$o"
