trap 'echo t; n=1' TERM
n=0
/bin/sh -c 'kill -TERM $PPID'
while [ $n = 0 ]; do :; done
echo out
