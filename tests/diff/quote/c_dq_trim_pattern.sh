x=abcabc
echo "${x#*b}" "${x##*b}" "${x%b*}" "${x%%b*}"
echo "${x#"*"b}"
