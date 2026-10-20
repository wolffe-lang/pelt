# in the background
command_not_found_handle() { echo "bg handler: $1"; return 6; }
nosuch & wait $!; echo "wait st=$?"
