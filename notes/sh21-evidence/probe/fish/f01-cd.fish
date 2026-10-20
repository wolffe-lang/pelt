# a handler that cds: does the shell move?
mkdir -p $TMPDIR/f01/there; cd $TMPDIR/f01
function fish_command_not_found; cd there; echo "in: "(basename $PWD)" args="(count $argv)" 1=$argv[1] 2=$argv[2]"; end
nosuch a
echo "after: "(basename $PWD)" st=$status"
