# the command's redirections around the call
function fish_command_not_found; echo "out: $argv"; echo "err: $argv" >&2; end
nosuch a b >$TMPDIR/f04.out 2>$TMPDIR/f04.err; echo "st=$status"
echo "file out: "(cat $TMPDIR/f04.out); echo "file err: "(cat $TMPDIR/f04.err)
