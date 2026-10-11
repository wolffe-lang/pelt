trap '/bin/sh -c "echo from-program"' TERM
/bin/sh -c 'kill -TERM $PPID'
echo after
