trap '' INT
/bin/sh -c 'kill -INT $PPID'
echo alive=$?
