printf '%s' $'\101\1012\7x' | od -An -tx1 | tr -d '[:space:]'; echo
