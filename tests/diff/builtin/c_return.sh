f() { return 3; }; f; echo $?
g() { false; return; }; g; echo $?
h() { true; return; }; h; echo $?
k() { return 255; }; k; echo $?
