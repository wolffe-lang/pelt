# Control for the once_ rows (pelt#156): without set -C a command that
# is not found still creates its redirection's file, status 127.
no_such_utility_for_this_case >f
echo "status $?"
test -f f && echo "f exists"
