# return 0, 3, 127: the command's status, and is anything said?
function fish_command_not_found; return $RET; end
set RET 0; nosuch; echo "ret0 st=$status"
set RET 3; nosuch; echo "ret3 st=$status"
set RET 127; nosuch 2>$TMPDIR/f02.err; echo "ret127 st=$status err="(wc -c <$TMPDIR/f02.err)
