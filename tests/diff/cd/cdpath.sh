mkdir -p d/e
CDPATH=d
cd e >/dev/null
echo $?
echo "${PWD##*/}"
