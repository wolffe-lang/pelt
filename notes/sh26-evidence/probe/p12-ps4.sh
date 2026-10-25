# item 5 (pelt#17): what PS4 is subjected to
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
