false; f() { (exit 7); }; echo $?
f; echo $?
g() { :; }; false; g; echo $?
