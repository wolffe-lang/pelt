export A=1
unset A
env | grep -c '^A='
