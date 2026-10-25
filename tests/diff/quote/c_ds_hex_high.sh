# pelt#65, XCU 2.2.4: $'\xHH' yields that byte, any byte but NUL
printf '%s' $'\xff' | od -An -tx1 | tr -d ' \n'; echo
printf '%s' $'\xe9' | od -An -tx1 | tr -d ' \n'; echo
