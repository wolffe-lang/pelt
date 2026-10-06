f() { return 3; }
f
echo $?
g() { false; return; }
g
echo $?
