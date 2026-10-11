set -e
false | true
echo $(false) ok
x=$(false; echo y) || true
echo reached
false | false
echo not-reached
