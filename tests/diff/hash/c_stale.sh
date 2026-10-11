mkdir a b; printf '#!/bin/sh\necho a\n' > a/prog; printf '#!/bin/sh\necho b\n' > b/prog; chmod +x a/prog b/prog
PATH=$PWD/a:$PWD/b:$PATH; prog; rm a/prog; prog
