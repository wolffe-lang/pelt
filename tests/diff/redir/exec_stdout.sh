exec 4>&1
exec >f
echo hidden
exec 1>&4 4>&-
echo back
cat f
