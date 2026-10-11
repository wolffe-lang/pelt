cat <&3 3<<E
on three
E
while read l; do echo "[$l]"; done <<E
a
b
E
