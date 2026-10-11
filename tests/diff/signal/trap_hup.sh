trap 'echo caught' HUP
/bin/sh -c 'kill -HUP $PPID'
echo after=$?
