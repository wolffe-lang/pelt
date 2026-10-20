# command, a slash, type, exec in a subshell
command_not_found_handle() { echo "handler: $1"; return 5; }
command nosuch1; echo "command st=$?"
./nosuch2; echo "slash st=$?"
type nosuch3 >/dev/null 2>&1; echo "type st=$?"
(exec nosuch4); echo "exec st=$?"
