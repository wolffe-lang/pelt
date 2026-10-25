# item 2 (pelt#63): the argv a #!-less file's shell is given, plain and exec
printf 'printf "%%s|" "$0" "$@"; echo; tr "\\000" "|" </proc/$$/cmdline; echo\n' > who; chmod +x who
./who a 'b c'
(exec ./who d)
PATH=$PWD:$PATH; who e
