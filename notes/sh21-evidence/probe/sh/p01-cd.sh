# a handler that cds: does the shell move?
mkdir -p "$TMPDIR/p01/there" && cd "$TMPDIR/p01"
command_not_found_handle() { cd there; echo "in: ${PWD##*/} args=$# 1=$1 2=${2-}"; }
nosuch a
echo "after: ${PWD##*/} st=$?"
