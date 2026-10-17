set -eo pipefail
if false | true; then echo yes; else echo no; fi
false | true || echo or
! false | true
echo tested
false | true
echo not-reached
