echo 0123456789 > f
exec 3<>f; read -r x <&3; echo "$x"; echo abc >&3; exec 3>&-
printf 'ab' 1<>f; cat f
: <>newf; ls newf
