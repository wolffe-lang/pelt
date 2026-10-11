HOME=$PWD; n=1
echo a > ~/t$n; echo b > "t $((n+1))"; echo c > $(echo t3)
cat t1 't 2' t3
