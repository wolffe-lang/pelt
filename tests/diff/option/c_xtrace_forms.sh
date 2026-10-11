x='a b'
set -x
echo $x "$x" 2>&1
y=1 2>&1
y=2 true
for i in 1; do :; done
set +x
( set -x; : "$x"; z=$x; [ a = a ]; ) 2>&1 | sed 's/^+* *//'
