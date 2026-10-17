mkdir a b; printf '#!/bin/sh\necho b\n' > b/prog; chmod +x b/prog
PATH=$PWD/a:$PWD/b:$PATH; prog; printf '#!/bin/sh\necho a\n' > a/prog; chmod +x a/prog; prog
hash -r; prog
printf '#!/bin/sh\necho c\n' > b/q; chmod +x b/q; q; chmod -x b/q; q 2>/dev/null; echo "noexec=$?"
