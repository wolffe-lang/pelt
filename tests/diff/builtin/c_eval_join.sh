eval echo a 'b;' echo c
eval 'x=1' 'y=2'; echo "$x $y"
eval "f() { echo defined; }"; f
cmd='echo "$z"'; z=late; eval $cmd
