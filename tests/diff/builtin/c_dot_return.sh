printf 'echo in\nreturn 4\necho not-reached\n' > lib
. ./lib; echo "st=$?"
f() { . ./lib; echo "func-continues $?"; }; f
