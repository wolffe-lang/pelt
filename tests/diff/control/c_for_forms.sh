set -- 'a b' c
for i do echo "[$i]"; done
for i
do echo "<$i>"; done
for i; do echo "{$i}"; done
false; for i in; do echo no; done; echo "st=$?"
