x=old
x=new y=$x z=$y; echo "$x $y $z"
x=old
x=new /usr/bin/printf '%s\n' "$x"
unset p q; p=1 q=$p /usr/bin/env > envout; grep '^p=' envout; grep '^q=' envout
echo "${p-unset} ${q-unset}"
echo done
