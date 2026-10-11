x=1; f() { echo outer; }
( x=2; cd /; set -f; f() { echo inner; }; exit 3 ); echo "$? $x"; f
case $- in *f*) echo f-leaked;; *) echo f-kept;; esac
[ "$PWD" != / ] && echo cwd-kept
