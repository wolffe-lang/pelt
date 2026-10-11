mkdir bin; printf '#!/bin/sh\necho path-colon\n' > bin/:; chmod +x bin/:
PATH=$PWD/bin:$PATH; : ; echo "st=$?"
