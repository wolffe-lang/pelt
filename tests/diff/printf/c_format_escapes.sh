printf 'a\tb\\c\101\n\0007|\r\v\f\a\b' | od -An -tx1 | tr -d '[:space:]'; echo
