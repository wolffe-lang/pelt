# The access primaries as the shell running this script answers them
# (XCU test: -r/-w/-x for THIS process), for a user and for root. Run by
# witness.sh inside a container, once per shell and per identity.
: >plain; chmod 644 plain
cp /usr/bin/env prog; chmod 755 prog
: >secret; chmod 000 secret
: >ro; chmod 444 ro
: >gx; chmod 610 gx
: >ox; chmod 601 ox
cp /usr/bin/env xonly; chmod 100 xonly
mkdir dir; mkdir shut; chmod 000 shut
ln -s plain link
for f in plain prog secret ro gx ox xonly dir shut link /usr/bin/env /etc/shadow /s/access.sh; do
    r=n w=n x=n
    test -r "$f" && r=y
    test -w "$f" && w=y
    test -x "$f" && x=y
    echo "$f r=$r w=$w x=$x"
done
mkdir bin1 bin2
cp /usr/bin/env bin1/whoruns; chmod 644 bin1/whoruns
printf '#!/bin/sh\necho bin2\n' >bin2/whoruns; chmod 755 bin2/whoruns
PATH=$PWD/bin1:$PWD/bin2:/usr/bin whoruns
chmod 755 shut
