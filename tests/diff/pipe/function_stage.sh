f() { echo from f; echo again; }
f | cat
f | while read a b; do echo "$b"; done
