printf '%s' $'\"\'\\' | od -An -tx1 | tr -d '[:space:]'; echo
printf '%s' $'\a\b\e\f\n\r\t\v' | od -An -tx1 | tr -d '[:space:]'; echo
