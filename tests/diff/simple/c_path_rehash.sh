mkdir a b; printf '#!/bin/sh\necho from-a\n' > a/prog; printf '#!/bin/sh\necho from-b\n' > b/prog
chmod +x a/prog b/prog
OLD=$PATH
PATH=$PWD/a:$OLD; prog
PATH=$PWD/b:$OLD; prog
rm b/prog; PATH=$PWD/b:$PWD/a:$OLD; prog
