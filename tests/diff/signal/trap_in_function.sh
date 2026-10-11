f() { trap 'echo t' TERM; }
f
/bin/sh -c 'kill -TERM $PPID'
echo after
