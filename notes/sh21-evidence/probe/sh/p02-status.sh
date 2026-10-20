# return 0, 3, 127: the command's status, and is anything said?
command_not_found_handle() { return "$RET"; }
RET=0; nosuch; echo "ret0 st=$?"
RET=3; nosuch; echo "ret3 st=$?"
RET=127; nosuch 2>"$TMPDIR/p02.err"; echo "ret127 st=$? err=$(wc -c <"$TMPDIR/p02.err")"
command_not_found_handle() { :; }
nosuch; echo "fall-off st=$?"
command_not_found_handle() { false; }
nosuch; echo "last-false st=$?"
