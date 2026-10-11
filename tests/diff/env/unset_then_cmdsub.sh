export A=1
unset A
x=$(env | grep -c '^A=')
echo "[$x]"
