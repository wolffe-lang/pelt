trap 'echo outer' TERM
(trap 'echo sub' TERM; /bin/sh -c 'kill -TERM $PPID')
/bin/sh -c 'kill -TERM $PPID'
echo after
