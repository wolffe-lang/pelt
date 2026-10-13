trap '' CHLD
/bin/sh -c 'exit 3'; echo "st=$?"
sleep 0.1 & wait $!; echo "bg=$?"
x=$(/bin/sh -c 'echo out; exit 4'); echo "cs=$? $x"
/bin/sh -c 'exit 5' | /bin/sh -c 'exit 6'; echo "pipe=$?"
grep SigIgn /proc/self/status
trap - CHLD
grep SigIgn /proc/self/status
trap '' CONT WINCH URG
grep SigIgn /proc/self/status
/bin/sh -c 'exit 7'; echo "st=$?"
trap
