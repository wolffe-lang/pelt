# Where no field splitting is done (an assignment's value, a `case`
# word, the word of ${x:-…} in one), $@ and $* join with the first
# character of IFS, quoted or not, and with nothing when IFS is empty
# (XCU 2.5.2 for $*; dash's answer for $@, which POSIX leaves open).
set a b c
IFS=,
x="$@"; echo "[$x]"
x=${y:-$*}; echo "[$x]"
case "$@" in a,b,c) echo joined ;; *) echo apart ;; esac
IFS=
x=$@; echo "[$x]"
