# Control for the once_ rows (pelt#156): a command that is not found
# with its output sent to /dev/null, under set -C as well (/dev/null is
# not a regular file, so noclobber does not refuse it).
no_such_utility_for_this_case >/dev/null
echo "status $?"
set -C
no_such_utility_for_this_case >/dev/null
echo "status $?"
