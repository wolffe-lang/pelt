echo hello >f
exec 3<>f
read x <&3
echo "$x"
exec 3>&-
: <>g
[ -f g ] && echo made
