readonly R=1
unset a b c d e f y
y=${a=word}; echo "a=$a y=$y"
echo ${b=word} "b=$b"
/usr/bin/printf '%s\n' ${c=word} "c=$c"
d=${e=word} /usr/bin/env > envout; grep '^d=' envout; grep -c '^e=' envout
echo "d=${d-unset} e=$e"
: ${f=word} > out; echo "f=$f"; cat out
echo done
