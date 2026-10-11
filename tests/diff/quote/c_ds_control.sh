printf '%s' $'\cA\cZ\c[' | od -An -tx1 | tr -d '[:space:]'; echo
