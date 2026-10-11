trap 'echo caught' INT
/bin/sh -c 'kill -INT $PPID'
echo after=$?
