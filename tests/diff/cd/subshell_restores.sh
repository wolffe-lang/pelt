mkdir s
(cd s)
echo "${PWD##*/}"
p=$(/bin/pwd)
echo "${p##*/}"
x=$(cd /; pwd)
echo $x
echo "${PWD##*/}"
