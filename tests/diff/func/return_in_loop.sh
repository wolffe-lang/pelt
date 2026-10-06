f() { for i in 1 2 3; do [ $i = 2 ] && return $i; echo $i; done; }
f
echo $?
