# `trap` takes a condition as a signal number as well as a name (XCU
# 2.15 trap; XSI for the numbers other than 0, and every script from
# automake's helpers to configure writes `trap … 1 2 13 15`). Setting
# an action for 13 (PIPE) or 14 (ALRM) is not an error, and `trap`
# lists it by name.
trap 'echo caught' 1 2 13 15
echo "set: $?"
trap '' 14
echo "ignore: $?"
trap >listed
sort listed
trap - 13 14
echo "reset: $?"
trap 'echo bye' 0
