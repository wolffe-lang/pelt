echo "$'a\tb'"
unset u; echo ${u-$'a\tb'} | od -An -c | tr -s ' '
echo "${u-$'x'}"
cat <<$'E'
body $HOME
E
cat <<E
$'a\tb'
E
set -- $''; echo $#
set -- $'' x; echo $#
echo $'`echo no`' $'$(echo no)'
echo $'~'
x=1; echo a$'$x'b
v='a*b'; echo ${v#$'a*'}; echo ${v%$'*b'}
export e=$'a b'; ../sh -c 'echo "$e"'
: > ab; echo $'a'*; echo $'*'
x=$'it\'s'; echo "$x"
x=$'a\nb'; echo "$x"
echo "$(echo $'c\td')" | od -An -c | tr -s ' '
