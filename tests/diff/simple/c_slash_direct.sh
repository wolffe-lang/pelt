mkdir d; printf '#!/bin/sh\necho direct\n' > d/prog; chmod +x d/prog
d/prog; ./d/prog; PATH=$PWD/d:$PATH; d/prog
