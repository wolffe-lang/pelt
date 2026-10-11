trap 'echo i' INT
trap -p INT | sed 's/SIG//'
trap -p TERM | sed 's/SIG//'
trap -p | grep -c -E 'INT|TERM' | tr -d ' '
