x='echo a; echo b'
eval "$x"
eval 'y=3'
echo $y
eval
echo $?
