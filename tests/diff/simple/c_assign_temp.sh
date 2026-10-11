x=outer
x=inner sh -c 'echo $x'; echo $x
unset n; n=1 env | grep '^n='; echo "${n-unset}"
