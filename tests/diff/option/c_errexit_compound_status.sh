set -e
if false; then :; fi
for i in 1; do false && true; done
case x in x) false || false;; esac && true
echo after-ignored
{ false && true; }
echo after-brace
