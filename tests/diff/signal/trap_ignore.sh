trap '' TERM
/bin/sh -c 'kill -TERM $PPID'
echo alive=$?
