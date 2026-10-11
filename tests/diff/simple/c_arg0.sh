printf '#!/bin/sh\necho "${0##*/} $# $1"\n' > prog; chmod +x prog
PATH=$PWD:$PATH; prog 'a b' c
./prog ''
