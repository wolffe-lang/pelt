# Where no field splitting is done — the right side of an assignment,
# a `case` word — an unquoted $* joins the positional parameters with
# the first character of IFS, as "$*" does (XCU 2.5.2). autoconf's
# configure splits the host triplet with IFS=- and rebuilds the OS
# part with `host_os=$*`.
ac_save_IFS=$IFS
triplet=x86_64-pc-linux-gnu
IFS=-
set x $triplet
shift
cpu=$1 vendor=$2
shift; shift
os=$*
IFS=$ac_save_IFS
echo "[$cpu] [$vendor] [$os]"
IFS=:
set a b c
x="$*"
y=$*
IFS=' '
echo "[$x] [$y]"
IFS=,
set p q
case $* in p,q) echo "case word joined" ;; *) echo "case word not joined" ;; esac
