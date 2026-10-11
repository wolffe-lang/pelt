trap 'echo by-number' 15 2
/bin/sh -c 'kill -TERM $PPID'
/bin/sh -c 'kill -INT $PPID'
echo after
