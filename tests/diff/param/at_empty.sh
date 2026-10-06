set --
for a in "$@"; do echo x; done
set -- "$@"
echo $#
