kill -l 1 2 3 9 15
kill -l 130 143 137
kill -l | tr ' ' '\n' | grep -c -E '^(HUP|INT|QUIT|KILL|TERM|USR1|USR2|PIPE|ALRM|CHLD|CONT|STOP|TSTP)$'
kill -l 999 2>/dev/null; echo "st=$?"
