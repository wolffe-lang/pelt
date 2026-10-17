readonly r=1
getopts a r -a 2>/dev/null; echo "st=$? OPTIND=$OPTIND"
getopts a 1bad -a 2>/dev/null; echo "bad=$?"
(getopts a r -a; echo "in=$?") 2>/dev/null; echo "subshell=$?"
