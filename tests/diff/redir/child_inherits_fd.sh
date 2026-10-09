exec 3>f
/bin/sh -c 'echo child >&3'
exec 3>&-
cat f
