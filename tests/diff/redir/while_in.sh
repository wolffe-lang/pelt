printf '1\n2\n' >f
while read n; do echo n$n; done <f
echo done
