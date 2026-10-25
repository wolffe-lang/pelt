# pelt#65, XCU 2.2.4: $'\ooo' yields that byte, any byte but NUL; a
# byte that is not UTF-8 is data like any other
printf '%s' $'\377' | od -An -tx1 | tr -d ' \n'; echo
printf '%s' a$'\377'b | od -An -tx1 | tr -d ' \n'; echo
x=$'\200'; printf '%s' "$x" | od -An -tx1 | tr -d ' \n'; echo
