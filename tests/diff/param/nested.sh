unset x y
echo ${x:-${y:-z}}
y=w
echo ${x:-${y:-z}}
