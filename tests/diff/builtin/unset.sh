x=1 y=2
unset x
echo [${x-u}] [$y]
f() { :; }
unset -f f
f
echo $?
