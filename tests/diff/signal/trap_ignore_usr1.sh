trap '' USR1
/bin/sh -c 'kill -USR1 $PPID'
echo alive=$?
