# pelt#65: $'...' quotes side by side are one word, so a character's
# UTF-8 bytes may be spelled across them (a three-byte character spelled
# in octal is left out: dash 0.5.13.4 dies of SIGSEGV on $'\342\202\254',
# sh26 probe/p27)
printf '%s' $'\303'$'\251' | od -An -tx1 | tr -d ' \n'; echo
printf '%s' x$'\303'$'\251'y | od -An -tx1 | tr -d ' \n'; echo
v=$'\303'$'\251'; printf '%s' "$v" | od -An -tx1 | tr -d ' \n'; echo
