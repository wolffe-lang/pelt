printf 'x\ny z\n' >f
while read l; do echo "[$l]"; done <f
