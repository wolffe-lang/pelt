{ echo a; echo b; } >f
cat f
if true; then echo c; fi >>f
cat f
for i in 1 2; do echo $i; done | cat
