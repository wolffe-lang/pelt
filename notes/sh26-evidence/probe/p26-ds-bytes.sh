# item 7 (pelt#65): $'\377' and $'\xff' leaving the shell
printf '%s' $'\377' | od -An -tx1
printf '%s' $'\xff' | od -An -tx1
printf '%s' $'\303\251' | od -An -tx1
printf '%s' $'\303'$'\251' | od -An -tx1
printf '%s' a$'\377'b | od -An -tx1
/usr/bin/printf '%s' $'\377' | od -An -tx1
x=$'\377'; printf '%s' "$x" | od -An -tx1
printf '\377' | od -An -tx1
echo "end st=$?"
