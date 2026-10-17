alias f='g'
f() { echo infunc; }
g
fn() { late; }
alias late='echo late'
fn 2>/dev/null || echo "st=$?"
