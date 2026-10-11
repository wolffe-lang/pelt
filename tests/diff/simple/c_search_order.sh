echo() { command echo "function echo: $*"; }
echo a
cat() { command echo function-cat; }; cat /dev/null
unset -f echo cat
mkdir bin; printf '#!/bin/sh\necho path-true\n' > bin/true; chmod +x bin/true
PATH=$PWD/bin:$PATH; true; echo "st=$?"
