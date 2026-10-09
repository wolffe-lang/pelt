printf 'a\nb\n' >f
exec 5<f
read x <&5
read y <&5
exec 5<&-
echo $x $y
