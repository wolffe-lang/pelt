# sh20: 2,000 turns of `x=$( :; : )`: a substitution of two commands, forked since sh20
i=0
while [ "$i" -lt 2000 ]; do
    x=$( :; : )
    i=$((i + 1))
done
echo "$i"
