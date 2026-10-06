unset x
echo ${x-def} ${x:-def}
x=
echo ${x-def} ${x:-def}
x=v
echo ${x-def} ${x:-def}
