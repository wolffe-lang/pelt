(set -o pipefail; false | true; echo "in $?"); false | true; echo "out $?"
f() { set -o pipefail; }; f; false | true; echo "function $?"
set +o pipefail
x=$(set -o pipefail; false | true; echo "sub $?"); echo "$x"; false | true; echo "after $?"
