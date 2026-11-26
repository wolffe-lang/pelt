# Control for the once_ rows (pelt#156): under set -C an existing
# regular file is refused before the command is looked for, and keeps
# its contents (XCU 2.7.2).
echo kept >f
set -C
no_such_utility_for_this_case >f
echo "status $?"
cat f
