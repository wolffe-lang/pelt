f() { :; }; alias a='echo x'
type f >/dev/null; echo "f=$?"
type cd >/dev/null; echo "cd=$?"
type ls >/dev/null; echo "ls=$?"
type if >/dev/null; echo "if=$?"
type a >/dev/null; echo "a=$?"
type nonexistent-xyz >/dev/null 2>&1; echo "missing=$?"
type ls f nonexistent-xyz 2>/dev/null | wc -l | tr -d ' '
