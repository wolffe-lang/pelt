trap 'echo caught' QUIT
/bin/sh -c 'kill -QUIT $PPID'
echo after=$?
