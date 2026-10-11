f() { trap 'true; return' USR2; (exit 7); /bin/sh -c 'kill -USR2 $PPID'; echo not-reached; }
f; echo "st=$?"
