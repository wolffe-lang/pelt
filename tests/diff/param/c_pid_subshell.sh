a=$$; b=$(echo $$); ( [ "$a" = "$$" ] && echo same1 ); [ "$a" = "$b" ] && echo same2
case $$ in *[!0-9]*|'') echo bad;; *) echo numeric;; esac
