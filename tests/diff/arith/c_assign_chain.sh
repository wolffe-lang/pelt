# Assignment is right-associative and is an expression: a chain sets
# every name to the same value, and an assignment inside a larger
# expression yields the value it stored.
echo $((a=b=c=3)) $a $b $c
echo $((a+=b*=2)) $a $b
echo $((d=(a=1)+(b=2))) $a $b $d
echo $((e=0?1:2)) $e $((f=(g=5)>4)) $f $g
