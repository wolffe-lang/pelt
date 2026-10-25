# item 2 (pelt#61): the reason a slashed command cannot run, by errno
echo x > f; ./f/x; echo "enotdir st=$?"
ln -s loop1 loop2; ln -s loop2 loop1; ./loop1; echo "eloop st=$?"
ln -s nowhere dangle; ./dangle; echo "dangling st=$?"
long=$(printf '%0300d' 0); ./$long; echo "enametoolong st=$?"
printf '#!/bin/sh\necho ran\n' > busy; chmod +x busy; exec 5>>busy; ./busy; echo "etxtbsy st=$?"; exec 5>&-
printf '#!/nonexistent/interp\necho ran\n' > badi; chmod +x badi; ./badi; echo "bad-interp st=$?"
mkdir -p dd; PATH=$PWD/dd:$PATH; mkdir dd/sub; sub; echo "dir-on-path st=$?"
chmod 0 dd 2>/dev/null; ./dd/sub; echo "eacces-dir st=$?"; chmod 755 dd
