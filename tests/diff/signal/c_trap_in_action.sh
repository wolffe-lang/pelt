trap 'echo first; trap "echo second" USR2' USR2
/bin/sh -c 'kill -USR2 $PPID'; /bin/sh -c 'kill -USR2 $PPID'; echo end
