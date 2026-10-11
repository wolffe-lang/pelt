f() { :; }
command -V ls >/dev/null; echo "ls=$?"
command -V f >/dev/null; echo "f=$?"
command -V cd >/dev/null; echo "cd=$?"
command -V if >/dev/null; echo "if=$?"
command -V nonexistent-xyz >/dev/null 2>&1; echo "missing=$?"
