HOME=/h
x=a:~/b; y=a:b~; z=a~b
printf '%s\n' "$x" "$y" "$z"
export w=p:~:q
printf '%s\n' "$w"
printf '[%s]\n' a:~/b
