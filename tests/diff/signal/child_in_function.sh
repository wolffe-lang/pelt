f() { /bin/sh -c 'kill -TERM $$'; }
f
echo $?
