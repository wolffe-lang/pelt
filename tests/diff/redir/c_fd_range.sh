exec 3>f3 4>f4 5>f5 6>f6 7>f7 8>f8 9>f9
for n in 3 4 5 6 7 8 9; do eval "echo fd$n >&$n"; done
exec 3>&- 4>&- 5>&- 6>&- 7>&- 8>&- 9>&-
cat f3 f4 f5 f6 f7 f8 f9
