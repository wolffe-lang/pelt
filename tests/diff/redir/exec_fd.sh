exec 3>f
echo one >&3
echo two >&3
exec 3>&-
cat f
