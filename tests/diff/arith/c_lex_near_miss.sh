# Longest-match lexing of operators beside their near misses: a sign
# after a comparison or a bit operator, `|=` against `||`, `&=` against
# `&&`, and `==` against an assignment that leaves text over.
echo $((1<-1)) $((1<=-1)) $((2>-1)) $((2>=-1)) $((3&-1)) $((4|-1)) $((5^-1)) $((1- -1)) $((1+ +1))
a=4 b=1
echo $((a|=b)) $a $((a||b)) $((a&=b)) $a $((a&&b)) $((a==1)) $((a!=1))
x=0
(: $((x=1=1))) 2>/dev/null; echo "status $?"
(: $((1=2))) 2>/dev/null; echo "status $?"
(: $((1 < = 2))) 2>/dev/null; echo "status $?"
echo $x
