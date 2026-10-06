unset x
echo ${x=one} $x
x=
echo ${x=two} [$x] ${x:=three} $x
