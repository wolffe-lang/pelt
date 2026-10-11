(trap 'echo sub' TERM; /bin/sh -c 'kill -TERM $PPID'; echo in)
echo out
