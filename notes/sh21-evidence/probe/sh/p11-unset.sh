# defined, then unset: the plain not-found
command_not_found_handle() { echo handler; }
unset -f command_not_found_handle
nosuch; echo "st=$?"
