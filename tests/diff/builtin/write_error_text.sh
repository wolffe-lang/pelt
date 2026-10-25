# pelt#28: a built-in's write that fails for a reason other than EPIPE
# (a closed standard output, a descriptor open only for reading): status
# 1, and dash's words after the shell's own prefix; a redirection to a
# closed descriptor is the redirection's error, status 2
t() { { eval "$1"; echo "st=$?"; } 2>&1 | sed 's/^.*: \([a-z]*: [a-z]*: I\/O error\)$/\1/; s/^.*: \(3: Bad file descriptor\)$/\1/'; }
t 'echo hi >&-'
t 'printf "x\n" >&-'
t 'pwd >&-'
exec 4</dev/null
t 'echo hi >&4'
t 'printf "x\n" >&4'
t 'echo hi >&3'
