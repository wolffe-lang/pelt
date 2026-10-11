exec 3>o3
exec /bin/sh -c 'echo via3 >&3; cat o3'
