set --
for i in "$@"; do echo never; done
set -- "$@"; echo $#
set -- x"$@"; echo $#
