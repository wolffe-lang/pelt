# pelt#17, XCU 2.5.3 PS4: expanded before each trace line as a
# double-quoted word is (parameters, arithmetic, command substitution,
# LINENO), the substitution not traced; empty is no prefix, and so is
# unset (dash)
exec 2>&1
n=1
PS4='${n}-$((n+1))-$(echo c)-${u:-dflt}> '
set -x
: one
set +x
PS4='[$LINENO] '
set -x
: two
set +x
PS4=''
set -x
: three
set +x
unset PS4
set -x
: four
set +x
