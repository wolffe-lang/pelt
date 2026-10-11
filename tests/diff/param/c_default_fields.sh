unset u
set -- ${u:-a b "c d" 'e f'}; echo $#
set -- "${u:-a b}"; echo $#
