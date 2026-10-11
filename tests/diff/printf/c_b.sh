printf '%b|' 'a\tb' 'c\0101d' 'e\\f' | od -An -tx1 | tr -d '[:space:]'; echo
printf '%b' 'stop\chere' 'and this'; echo
printf '%5b|%-5b|%.2b|\n' ab cd efgh
