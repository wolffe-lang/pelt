# a handler that runs the name again: re-entered?
n=0
command_not_found_handle() { n=$((n+1)); echo "depth $n: $1"; [ "$n" -lt 4 ] || return 9; "$@"; }
nosuch a 2>"$TMPDIR/p03.err"; echo "st=$? n=$n err=$(wc -c <"$TMPDIR/p03.err")"
