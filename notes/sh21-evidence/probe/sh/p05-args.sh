# the words: $1 the name, then the arguments, expanded
command_not_found_handle() { printf '[%s]' "$#" "$@"; echo; }
x='two words'; set -- p q
nosuch "$x" $x "$@" '*' ${unset-dflt}
"no such" a
