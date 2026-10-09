{ exec 3>f; } 2>/dev/null
echo kept >&3
exec 3>&-
cat f
