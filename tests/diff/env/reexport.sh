export A=1
unset A
A=2
env | grep -c '^A='
export A
env | grep '^A='
