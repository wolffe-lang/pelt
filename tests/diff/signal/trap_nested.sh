# A trapped signal that comes while another trap's action runs has its
# action run inside it, after the command it came during (dash).
trap 'echo a; /bin/sh -c "kill -USR2 \$PPID"; echo b' USR1
trap 'echo c' USR2
/bin/sh -c 'kill -USR1 $PPID'
echo d
