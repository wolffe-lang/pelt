readonly r=1
( echo $((r=2)) "r=$r"; echo unreached ) 2>/dev/null; echo "st=$?"
readonly u
( echo ${u=7} "u=$u"; echo unreached ) 2>/dev/null; echo "st=$?"
( /usr/bin/printf '%s\n' $((r+=1)) "$r"; echo unreached ) 2>/dev/null; echo "st=$?"
echo "r=$r"
echo done
