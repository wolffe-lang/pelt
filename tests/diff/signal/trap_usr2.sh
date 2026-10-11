trap 'echo caught' USR2
/bin/sh -c 'kill -USR2 $PPID'
echo after=$?
