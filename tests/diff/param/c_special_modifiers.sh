set -- a b
echo ${#:-x} ${?:-x} ${0:+zero} ${1:-x} ${3:-three} ${3-} "${1:+one}"
false; echo ${?#0}
