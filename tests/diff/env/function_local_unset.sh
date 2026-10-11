export A=1
f() { local A; unset A; env | grep -c '^A='; }
f
env | grep -c '^A='
