unset R
unset a b c d e f y
y=$((a=5)); echo "a=$a y=$y"
echo $((b=5)) "b=$b"
/usr/bin/printf '%s\n' $((c=5)) "c=$c"
d=$((e=5)) /usr/bin/env > envout; grep '^d=' envout; grep -c '^e=' envout
echo "d=${d-unset} e=$e"
: $((f=5)) > out; echo "f=$f"; cat out
echo done
