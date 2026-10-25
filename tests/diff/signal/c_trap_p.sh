trap 'echo i' INT
trap -p INT > o; sed 's/SIG//' o
trap -p TERM > o; sed 's/SIG//' o
trap -p > o; grep -c -E 'INT|TERM' o | tr -d ' '
