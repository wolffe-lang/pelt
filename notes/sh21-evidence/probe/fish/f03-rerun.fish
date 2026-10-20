# a handler that runs the name again: re-entered?
set -g n 0
function fish_command_not_found; set -g n (math $n + 1); echo "depth $n: $argv[1]"; test $n -lt 4; or return 9; $argv; end
nosuch a 2>$TMPDIR/f03.err; echo "st=$status n=$n err="(wc -c <$TMPDIR/f03.err)
