printf '#!/bin/sh\necho here\n' > prog; chmod +x prog
PATH=:/usr/bin:/bin; prog
PATH=/usr/bin:/bin:; prog
PATH=/usr/bin::/bin; prog
