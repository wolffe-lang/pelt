trap '' HUP
trap - HUP
/bin/sh -c 'kill -HUP $PPID'
echo not-reached
