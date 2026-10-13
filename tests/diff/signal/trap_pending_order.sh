# Signals that are waiting together run their actions in the order of
# the signals' numbers, not the order they were sent in (dash).
trap 'echo T' TERM; trap 'echo H' HUP; trap 'echo A' ALRM; trap 'echo W' WINCH
trap 'echo Q' QUIT; trap 'echo P' PIPE
/bin/sh -c 'kill -TERM $PPID; kill -WINCH $PPID; kill -PIPE $PPID; kill -HUP $PPID; kill -ALRM $PPID; kill -QUIT $PPID'
echo done
