mkdir bin; printf '#!/bin/sh\n' > bin/myprog; chmod +x bin/myprog
PATH=$PWD/bin:$PATH
type myprog | grep -c "bin/myprog"
