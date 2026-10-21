# sh20: 2,000 turns of `( :; : )`: a subshell of two commands, forked since sh20
i=0
while [ "$i" -lt 2000 ]; do
    ( :; : )
    i=$((i + 1))
done
echo "$i"
