set -o pipefail
false | true; echo $?
(exit 3) | (exit 4) | true; echo $?
true | true; echo $?
! false | true; echo $?
set +o pipefail
false | true; echo $?
