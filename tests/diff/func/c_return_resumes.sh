f() { echo before; return 3; echo not-reached; }
f; echo "after $?"
g() { while :; do return; done; }; false; g; echo $?
