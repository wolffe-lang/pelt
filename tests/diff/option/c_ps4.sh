x=tag
PS4='$x> '
set -x
echo traced 2>&1
set +x
( set -x; : word ) 2>&1 | sed 's/[0-9]//g'
