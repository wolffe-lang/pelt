v=0; : $((v=v+1)); echo "v=$v"
readonly r=1
( : $((r=2)); echo unreached ) 2>/dev/null; echo "st=$? r=$r"
readonly u2
( : ${u2=5}; echo unreached ) 2>/dev/null; echo "st=$?"
v=0; : $((v=v+1)) ${w=3}; echo "v=$v w=$w"
echo done
