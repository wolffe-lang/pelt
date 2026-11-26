# Control for the once_ rows (pelt#156): under set -C a command that is
# found creates a new file through > and succeeds.
set -C
true >f
echo "status $?"
test -f f && echo "f exists"
