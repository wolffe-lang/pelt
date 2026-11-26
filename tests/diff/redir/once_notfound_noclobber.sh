# A simple command's redirections are performed once, even when the
# command search then finds nothing (XCU 2.9.1): under set -C the file
# the redirection created is not refused afterwards as one that already
# exists, and the status is the not-found 127 (pelt#156).
set -C
no_such_utility_for_this_case >f
echo "status $?"
test -f f && echo "f exists"
