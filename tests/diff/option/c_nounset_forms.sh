set -u
set --
echo "$@" "$*" $# ${u-default} ${u:+x} "${1-none}"
(echo $1; echo no) 2>/dev/null; echo "st=$?"
(echo ${u}; echo no) 2>/dev/null; echo "st=$?"
e=; echo "[$e]"
