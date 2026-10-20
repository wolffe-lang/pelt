# the command's redirections around the call
command_not_found_handle() { echo "out: $*"; echo "err: $*" >&2; }
nosuch a b >"$TMPDIR/p04.out" 2>"$TMPDIR/p04.err"; echo "st=$?"
echo "file out: $(cat "$TMPDIR/p04.out")"; echo "file err: $(cat "$TMPDIR/p04.err")"
nosuch c </dev/null >&2 2>/dev/null; echo "st=$?"
