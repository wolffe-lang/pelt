# a pipeline, a substitution, a function
function fish_command_not_found; echo "handler: $argv[1] args="(count $argv); return 4; end
nosuch1 | cat; echo "pipe st=$status"
set v (nosuch2); echo "sub: [$v] st=$status"
function f; nosuch3 x y; echo "in f st=$status"; end; f F
command nosuch4; echo "command st=$status"
./nosuch5; echo "slash st=$status"
