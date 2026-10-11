x=1; f() { echo func; }; set -- a b; set -f
( echo "$x $# $1"; f; case $- in *f*) echo f;; esac )
echo "$(echo "$x $#"; f)"
