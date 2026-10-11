x=outer
x=inner echo hi; echo $x
x=inner command eval 'echo $x'; echo $x
IFS=: read a b <<E
p:q
E
echo "$a $b"; printf '%s' "$IFS" | od -An -tx1 | tr -d '[:space:]'; echo
