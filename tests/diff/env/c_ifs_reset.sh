IFS=: ../sh -c 'printf "%s" "$IFS" | od -An -tx1 | tr -d "[:space:]"; echo; x="a:b c"; set -- $x; echo $#'
