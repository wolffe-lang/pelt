set -a; unset q x
x=$((q=7)) /usr/bin/env > envout; grep '^q=' envout; grep '^x=' envout
unset q x; x=$((q=8)) /usr/bin/env | grep '^[qx]=' | sort
set +a; export E=1
y=$((E=2)) /usr/bin/env > envout; grep '^E=' envout
echo "E=$E q=$q"
echo done
