set -- outer
f() { set -- inner; echo $1; }
f x
echo $1
