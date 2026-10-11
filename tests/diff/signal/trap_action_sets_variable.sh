trap 'got=yes' TERM
/bin/sh -c 'kill -TERM $PPID'
echo "got=$got"
