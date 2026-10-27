mkdir -p first/wolf-sh33-dir last/wolf-sh33-dir
PATH=$PWD/first:$PWD/last wolf-sh33-dir
printf 'direct:%s\n' "$?"
PATH=$PWD/first command wolf-sh33-dir
printf 'command:%s\n' "$?"
(PATH=$PWD/first; exec wolf-sh33-dir)
printf 'exec:%s\n' "$?"
printf '#!/bin/sh\necho later\n' > last/wolf-sh33-ok
chmod +x last/wolf-sh33-ok
mkdir first/wolf-sh33-ok
PATH=$PWD/first:$PWD/last wolf-sh33-ok
PATH=$PWD/first command -v wolf-sh33-dir
printf 'lookup:%s\n' "$?"
