set -o pipefail
(exit 3) | true | (exit 5) | true; echo $?
(exit 3) | (exit 5) | (exit 0); echo $?
true | (exit 7); echo $?
(exit 2) | true; echo $?
true | true | true; echo $?
