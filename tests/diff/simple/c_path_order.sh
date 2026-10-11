mkdir a b; printf '#!/bin/sh\necho from-a\n' > a/prog; printf '#!/bin/sh\necho from-b\n' > b/prog
chmod +x b/prog
PATH=$PWD/a:$PWD/b:$PATH prog
chmod +x a/prog; PATH=$PWD/a:$PWD/b:$PATH; prog
