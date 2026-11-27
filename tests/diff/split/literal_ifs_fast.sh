IFS=:
printf '[%s]\n' a:b c:d
for w in x:y z; do printf '<%s>\n' "$w"; done
v=p:q; printf '(%s)\n' $v
IFS=a
printf '[%s]\n' banana
